import streamlit as st
from streamlit_tldraw import st_tldraw
import json
import time

# Set page config for best appearance
st.set_page_config(
    page_title="Streamlit tldraw Demo", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Streamlit tldraw Interactive Whiteboard")
st.markdown("""
This demo showcases the integration of [tldraw](https://tldraw.com) with Streamlit.
Create diagrams, flowcharts, wireframes, and more with this powerful drawing tool.
""")

# Add error handling wrapper
def safe_component(func, *args, **kwargs):
    """Safely execute a component with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc(), language="python")
        return {"error": str(e), "type": "error"}

# Sidebar controls
with st.sidebar:
    st.header("Canvas Settings")
    
    # Canvas dimensions
    height = st.slider("Canvas Height", 300, 1000, 700, help="Set the height of the canvas in pixels")
    width_percent = st.slider("Canvas Width", 50, 100, 100, help="Set the width of the canvas as percentage of container")
    width = int(width_percent * 10)  # Convert to pixels (approximation)
    
    # Appearance options
    appearance_col1, appearance_col2 = st.columns(2)
    with appearance_col1:
        dark_mode = st.toggle("Dark Mode", False, help="Toggle dark theme for the canvas")
    with appearance_col2:
        read_only = st.toggle("Read Only", False, help="Make canvas non-editable")
    
    show_ui = st.toggle("Show UI Elements", True, help="Show or hide toolbar and menu")
    
    # Data management
    st.subheader("Data Management")
    
    # Initialize session state for diagram data if not present
    if 'tldraw_data' not in st.session_state:
        st.session_state.tldraw_data = None
    
    # Clear button
    if st.button("🗑️ Clear Canvas", help="Clear all content from the canvas"):
        st.session_state.tldraw_data = None
        st.success("Canvas cleared! The canvas will refresh when you leave this sidebar.")
    
    # Save/load options
    if st.session_state.get('tldraw_result'):
        # Download button
        btn = st.download_button(
            "💾 Download JSON",
            data=json.dumps(st.session_state.tldraw_result, indent=2),
            file_name=f"tldraw_diagram_{time.strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            help="Download the current diagram as a JSON file"
        )
    
    # Upload option
    uploaded_file = st.file_uploader(
        "📂 Load JSON", 
        type=["json"],
        help="Upload a previously saved tldraw JSON file"
    )
    
    if uploaded_file:
        try:
            # Load data from uploaded file
            initial_data = json.loads(uploaded_file.getvalue().decode())
            st.session_state.tldraw_data = initial_data
            st.success("Diagram loaded successfully! The canvas will update when you leave this sidebar.")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

# Main canvas
st.header("Main Canvas")
st.caption("Draw, create diagrams, or design interfaces in this interactive canvas.")

try:
    # Use our safe wrapper
    result = safe_component(
        st_tldraw,
        key="tldraw_main",
        width=width,
        height=height,
        dark_mode=dark_mode,
        read_only=read_only,
        show_ui=show_ui,
        initial_data=st.session_state.tldraw_data
    )
    
    # Process and store results
    if result and "error" not in result:
        st.session_state.tldraw_result = result
        if 'snapshot' in result:
            st.session_state.tldraw_data = result['snapshot']
except Exception as e:
    st.error(f"Error displaying tldraw component: {str(e)}")

# Canvas data (collapsible)
with st.expander("View Canvas Data"):
    if 'tldraw_result' in st.session_state and st.session_state.tldraw_result:
        event_type = st.session_state.tldraw_result.get('type', 'N/A')
        st.write(f"Event Type: `{event_type}`")
        st.json(st.session_state.tldraw_result)
    else:
        st.info("No data available yet. Start drawing on the canvas to see the data here.")

# Examples section
st.header("Feature Examples")

tab1, tab2, tab3 = st.tabs(["Read-only Mode", "Dark Mode", "Pre-loaded Content"])

with tab1:
    st.subheader("Read-only Canvas Example")
    st.caption("This canvas cannot be edited - perfect for displaying diagrams to users.")
    
    safe_component(
        st_tldraw,
        key="tldraw_readonly",
        height=300,
        read_only=True,
        initial_data=st.session_state.tldraw_data
    )

with tab2:
    st.subheader("Dark Mode Example")
    st.caption("Dark mode provides better visibility in low-light environments.")
    
    safe_component(
        st_tldraw,
        key="tldraw_dark",
        height=300,
        dark_mode=True
    )

with tab3:
    st.subheader("Pre-loaded Content Example")
    st.caption("You can initialize the canvas with pre-defined shapes and content.")
    
    # Example of pre-defined content
    initial_data = {
        "document": {
            "id": "doc",
            "name": "New Document",
            "version": 15.5,
            "pages": {
                "page1": {
                    "id": "page1",
                    "name": "Page 1",
                    "childIndex": 1,
                    "shapes": {
                        "shape1": {
                            "id": "shape1",
                            "type": "geo",
                            "x": 128,
                            "y": 128,
                            "props": {
                                "w": 200,
                                "h": 100,
                                "geo": "rectangle",
                                "color": "blue",
                                "text": "Hello, Streamlit!",
                                "align": "middle",
                                "size": "m"
                            }
                        }
                    }
                }
            },
            "pageStates": {
                "page1": {
                    "id": "page1",
                    "selectedIds": [],
                    "camera": {
                        "point": [0, 0],
                        "zoom": 1
                    }
                }
            }
        }
    }
    
    safe_component(
        st_tldraw,
        key="tldraw_preloaded",
        height=300,
        initial_data=initial_data
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Built with ❤️ using <a href="https://tldraw.com" target="_blank">tldraw</a> and <a href="https://streamlit.io" target="_blank">Streamlit</a></p>
</div>
""", unsafe_allow_html=True)