import AceEditor from "react-ace";  // Import AceEditor component
import "ace-builds/src-noconflict/mode-c_cpp";  // Import Python syntax highlighting
import "ace-builds/src-noconflict/theme-tomorrow_night";  // Import monokai theme
import "./Editor.css";  // Import Editor.css styles

function Editor({ code, setCode, width, setWidth }) {
    // Function to handle mouse move events and update the editor's width
    const handleMouseMove = (e) => {
        setWidth(Math.min(Math.max(300, e.pageX), window.innerWidth - 300));
    };

    // Function to remove event listeners when the mouse button is released
    const handleMouseUp = () => {
        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", handleMouseUp);
    };

    // Render the editor with a draggable divider for adjusting the width
    return (
        <div style={{ display: "flex" }}>
            <AceEditor
                mode="c_cpp"
                theme="tomorrow_night"
                name="code-editor"
                value={code}
                onChange={setCode}
                fontSize={16}
                width={`${width}px`}
                height="100%"
                showPrintMargin={false}
                showGutter={true}
                highlightActiveLine={true}
                editorProps={{ $blockScrolling: Infinity }}
                setOptions={{
                    useWorker: false,
                    showLineNumbers: true,
                    tabSize: 2,
                }}
            />
            <div
                className="divider"
                style={{ float: "right" }}
                onMouseDown={(e) => {
                    e.preventDefault();
                    document.addEventListener("mousemove", handleMouseMove);
                    document.addEventListener("mouseup", handleMouseUp);
                }}
            ></div>
        </div>
    );
}

export default Editor;