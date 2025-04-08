import React, { useEffect, useState } from 'react';
import { Streamlit, withStreamlitConnection, ComponentProps } from 'streamlit-component-lib';
import { Tldraw, Editor, TldrawEditor } from '@tldraw/tldraw';
import '@tldraw/tldraw/tldraw.css';

interface TldrawComponentProps extends ComponentProps {
  args: {
    height: number;
    width: number;
    readOnly: boolean;
    darkMode: boolean;
    showUI: boolean;
    initialData: any;
  };
}

const TldrawComponent: React.FC<TldrawComponentProps> = (props) => {
  const { height, width, readOnly, darkMode, showUI, initialData } = props.args;
  const [isFocused, setIsFocused] = useState(false);
  const [editor, setEditor] = useState<Editor | null>(null);
  const [editorError, setEditorError] = useState<string | null>(null);
  
  // Apply dark mode
  useEffect(() => {
    try {
      // Set the frame height
      Streamlit.setFrameHeight(height || 600);
      
      // Set dark mode on the document and editor
      const theme = darkMode ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', theme);
      
      // Also set a CSS class for additional styling
      if (darkMode) {
        document.body.classList.add('tldraw-dark');
      } else {
        document.body.classList.remove('tldraw-dark');
      }
      
      // Log for debugging
      console.log(`Theme set to: ${theme}`);
    } catch (error) {
      console.error('Error setting dark mode:', error);
      if (error instanceof Error) {
        setEditorError(`Error setting dark mode: ${error.message}`);
      } else {
        setEditorError('Error setting dark mode: Unknown error');
      }
    }
  }, [height, darkMode]);
  
  // Apply read-only mode
  useEffect(() => {
    try {
      if (editor) {
        // Toggle read-only mode based on the prop
        editor.updateInstanceState({ isReadonly: readOnly });
        console.log(`Read-only mode set to: ${readOnly}`);
      }
    } catch (error: unknown) {
      console.error('Error setting read-only mode:', error);
      if (error instanceof Error) {
        setEditorError(`Error setting read-only mode: ${error.message}`);
      } else {
        setEditorError('Error setting read-only mode: Unknown error');
      }
    }
  }, [editor, readOnly]);
  
  // Handle UI visibility
  useEffect(() => {
    try {
      if (editor && !showUI) {
        // Find UI elements to hide/show
        const uiElements = document.querySelectorAll('.tlui-menu, .tlui-toolbar, .tlui-style-panel');
        uiElements.forEach(el => {
          if (el instanceof HTMLElement) {
            el.style.display = showUI ? 'flex' : 'none';
          }
        });
        console.log(`UI visibility set to: ${showUI}`);
      }
    } catch (error) {
      console.error('Error setting UI visibility:', error);
      if (error instanceof Error) {
        setEditorError(`Error setting UI visibility: ${error.message}`);
      } else {
        setEditorError('Error setting UI visibility: Unknown error');
      }
    }
  }, [editor, showUI]);

  // Handle when the editor is ready
  const handleMount = (editor: Editor) => {
    try {
      console.log('Editor mounted successfully');
      setEditor(editor);
      
      // Load initial data if provided
      if (initialData) {
        try {
          console.log('Loading initial data');
          
          // The format may need adjustment based on the data structure
          if (typeof initialData === 'object') {
            if (initialData.snapshot) {
              // If the data has a snapshot property, use that
              editor.store.loadSnapshot(initialData.snapshot);
            } else if (initialData.document) {
              // If the data has a document property, try to load that
              editor.store.loadSnapshot(initialData);
            } else {
              // Otherwise, try to load it directly
              editor.store.loadSnapshot(initialData);
            }
            console.log('Initial data loaded successfully');
          } else {
            throw new Error('Initial data is not an object');
          }
        } catch (e) {
          console.error('Failed to load initial data:', e);
          console.error('Initial data structure:', JSON.stringify(initialData, null, 2));
          if (e instanceof Error) {
            setEditorError(`Failed to load initial data: ${e.message}`);
          } else {
            setEditorError('Failed to load initial data: Unknown error');
          }
        }
      }
      
      // Listen for changes to send back to Streamlit
      // const unsubscribe = editor.store.listen(() => {
      //   try {
      //     const snapshot = editor.store.serialize();
      //     Streamlit.setComponentValue({
      //       snapshot: snapshot,
      //       type: 'document_change'
      //     });
      //   } catch (e) {
      //     console.error('Error sending data to Streamlit:', e);
      //     if (e instanceof Error) {
      //       setEditorError(`Error sending data to Streamlit: ${e.message}`);
      //     } else {
      //       setEditorError('Error sending data to Streamlit: Unknown error');
      //     }
      //   }
      // });
      
      // Send initial state
      try {
        const snapshot = editor.store.serialize();
        Streamlit.setComponentValue({
          snapshot: snapshot,
          type: 'mounted'
        });
        console.log('Initial state sent to Streamlit');
      } catch (e) {
        console.error('Error sending initial state to Streamlit:', e);
        if (e instanceof Error) {
          setEditorError(`Error sending initial state to Streamlit: ${e.message}`);
        } else {
          setEditorError('Error sending initial state to Streamlit: Unknown error');
        }
      }
      
      // We're not cleaning up the listener here since we keep it for the component's lifetime
    } catch (error) {
      console.error('Error in editor mount handler:', error);
      if (error instanceof Error) {
        setEditorError(`Error in editor mount handler: ${error.message}`);
      } else {
        setEditorError('Error in editor mount handler: Unknown error');
      }
    }
  };

  // Reset editor error after 5 seconds
  useEffect(() => {
    if (editorError) {
      const timer = setTimeout(() => {
        setEditorError(null);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [editorError]);

  return (
    <div
      style={{
        width: width || '100%',
        height: height || 600,
        border: isFocused ? '2px solid #00ff00' : '1px solid #ccc',
        borderRadius: '4px',
        overflow: 'hidden',
        position: 'relative'
      }}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
    >
      {/* Error message overlay */}
      {editorError && (
        <div style={{
          position: 'absolute',
          top: '10px',
          left: '10px',
          right: '10px',
          backgroundColor: 'rgba(255, 0, 0, 0.8)',
          color: 'white',
          padding: '10px',
          borderRadius: '4px',
          zIndex: 1000,
          fontFamily: 'sans-serif',
          fontSize: '14px'
        }}>
          {editorError}
        </div>
      )}
      
      <TldrawEditor onMount={handleMount}>
        <Tldraw />
      </TldrawEditor>
    </div>
  );
};

export default withStreamlitConnection(TldrawComponent);