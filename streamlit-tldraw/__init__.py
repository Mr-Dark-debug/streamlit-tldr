import streamlit.components.v1 as components
import json
from typing import Optional, Dict, Any, Union, List
import os
import warnings

# Determine if the component is being run in development or production mode
_RELEASE = True

if not _RELEASE:
    # Development mode
    _component_func = components.declare_component(
        "streamlit_tldraw",
        url="http://localhost:3001",
    )
else:
    # Production mode
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit-tldraw", path=build_dir)

def st_tldraw(
    key: Optional[str] = None,
    width: Optional[int] = None,
    height: int = 600,
    read_only: bool = False,
    dark_mode: bool = False,
    show_ui: bool = True,
    initial_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a new instance of the TLDraw component.
    
    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    width: int or None
        The width of the canvas in pixels. Default is the container width.
    height: int
        The height of the canvas in pixels. Default is 600.
    read_only: bool
        Whether the canvas is read-only. Default is False.
    dark_mode: bool
        Whether to use dark mode. Default is False.
    show_ui: bool
        Whether to show the UI elements (toolbar, menu). Default is True.
    initial_data: dict or None
        Initial canvas data to load. This should be a valid TLDraw document.
        
    Returns
    -------
    dict
        The current state of the canvas, including all shapes and their properties.
    """
    # Validate and clean input parameters
    if height < 100:
        warnings.warn("Height is too small, setting to minimum of 100px")
        height = 100
    
    if width is not None and width < 100:
        warnings.warn("Width is too small, setting to minimum of 100px")
        width = 100
    
    # Validate initial_data if provided
    if initial_data is not None:
        if not isinstance(initial_data, dict):
            raise TypeError("initial_data must be a dictionary")
        
        # Normalize initial data structure if needed
        # This helps handle different formats the user might provide
        if 'document' in initial_data and isinstance(initial_data['document'], dict):
            # Format is likely already correct
            pass
        elif 'snapshot' in initial_data and isinstance(initial_data['snapshot'], dict):
            # Extract the snapshot
            initial_data = initial_data['snapshot']
        
        # Add basic validation to prevent obvious errors
        if not any(key in initial_data for key in ['document', 'shapes', 'pages']):
            warnings.warn(
                "initial_data doesn't appear to be in a valid TLDraw format. "
                "It should contain one of these keys: 'document', 'shapes', or 'pages'."
            )
    
    try:
        # Call the component function with the validated arguments
        component_value = _component_func(
            key=key,
            width=width,
            height=height,
            readOnly=read_only,
            darkMode=dark_mode,
            showUI=show_ui,
            initialData=initial_data,
        )
        
        return component_value or {}
    except Exception as e:
        # Handle any unexpected errors
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in st_tldraw component: {str(e)}\n{error_details}")
        
        # Return an error state that the app can handle
        return {
            "error": str(e),
            "type": "error"
        }

# Alias for backward compatibility
tldraw = st_tldraw

# Example function
def example():
    import streamlit as st
    
    st.title("Streamlit tldraw Example")
    st.markdown("Use the canvas below to create a diagram. The data is sent back to Streamlit in real-time.")
    
    try:
        result = st_tldraw(
            key="tldraw_example",
            height=700,
        )
        
        if result:
            if "error" in result:
                st.error(f"Component Error: {result['error']}")
            else:
                st.subheader("Canvas Data")
                st.write(f"Event Type: {result.get('type', 'N/A')}")
                st.json(result)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error("Please check your browser console for more details.")

if __name__ == "__main__":
    example()