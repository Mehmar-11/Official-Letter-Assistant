import { useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("text");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");

  // Typewriter effect
  const typeText = (text, setter) => {
    setter("");
    let i = 0;

    const interval = setInterval(() => {
      setter((prev) => prev + (text[i] || ""));
      i++;
      if (i >= text.length) clearInterval(interval);
    }, 15);
  };

  // API call (text only for now)
  const analyzeLetter = async () => {
    setLoading(true);
    setResult(null);
    setAnimatedSummary("");

    try {
      const response = await fetch("http://localhost:8000/analyze-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ letter_text: text }),
      });

      const data = await response.json();
      setResult(data);
      typeText(data.summary || "", setAnimatedSummary);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>

      {/* TOP BAR */}
      <div style={styles.topBar}>
        <div style={styles.brand}>Official Letter Assistant</div>
        <div style={styles.status}>● System Ready</div>
      </div>

      <div style={styles.grid}>

        {/* LEFT PANEL */}
        <div style={styles.leftPanel}>
          <div style={styles.panelTitle}>Input Document</div>

          {/* MODE SWITCH */}
          <div style={styles.switchRow}>
            <button
              onClick={() => setMode("text")}
              style={mode === "text" ? styles.activeTab : styles.tab}
            >
              Text
            </button>

            <button
              onClick={() => setMode("pdf")}
              style={mode === "pdf" ? styles.activeTab : styles.tab}
            >
              PDF
            </button>
          </div>

          {/* TEXT INPUT */}
          {mode === "text" ? (
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste German official letter..."
              style={styles.textarea}
            />
          ) : (
            /* PDF UPLOAD */
            <div
              style={styles.dropZone}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const droppedFile = e.dataTransfer.files[0];
                setFile(droppedFile);
              }}
            >
              <div>📁 Drag & Drop PDF here</div>

              <div style={{ fontSize: "12px", color: "#9ca3af" }}>
                or click to select file
              </div>

              <input
                type="file"
                accept="application/pdf"
                style={styles.hiddenFile}
                onChange={(e) => setFile(e.target.files[0])}
              />

              {file && (
                <div style={{ marginTop: "10px", color: "#22c55e" }}>
                  Selected: {file.name}
                </div>
              )}
            </div>
          )}

          {/* BUTTON */}
          <button onClick={analyzeLetter} style={styles.analyzeBtn}>
            {loading ? "Analyzing..." : "Analyze Document"}
          </button>
        </div>

        {/* RIGHT PANEL */}
        <div style={styles.rightPanel}>
          <div style={styles.panelTitle}>Analysis Output</div>

          {loading && (
            <div style={styles.scanning}>
              Scanning document...
            </div>
          )}

          <div style={styles.timeline}>
            <div>Document received</div>
            <div>Extracting text</div>
            <div>Cleaning data</div>
            <div>AI analysis running</div>
          </div>

          <div style={styles.card}>
            <div style={styles.label}>Summary</div>
            <div>{animatedSummary || "Waiting..."}</div>
          </div>

          <div style={styles.card}>
            <div style={styles.label}>Deadlines</div>
            <div>{result?.deadlines?.join(", ") || "—"}</div>
          </div>

          <div style={styles.card}>
            <div style={styles.label}>Required Actions</div>
            <div>{result?.required_actions?.join(", ") || "—"}</div>
          </div>

          <div style={styles.card}>
            <div style={styles.label}>Risky Parts</div>
            <div>{result?.unclear_or_risky_parts?.join(", ") || "—"}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ================= STYLES ================= */
const styles = {
  page: {
    height: "100vh",
    background: "radial-gradient(circle at 20% 20%, #1e1b4b, #0b0f19 60%)",
    color: "white",
    fontFamily: "Arial",
  },

  topBar: {
    display: "flex",
    justifyContent: "space-between",
    padding: "16px 30px",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
  },

  brand: { fontWeight: "600" },

  status: { color: "#22c55e", fontSize: "12px" },

  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
    padding: "20px",
  },

  leftPanel: {
    background: "rgba(17, 25, 40, 0.7)",
    padding: "20px",
    borderRadius: "16px",
  },

  rightPanel: {
    background: "rgba(17, 25, 40, 0.6)",
    padding: "20px",
    borderRadius: "16px",
  },

  panelTitle: {
    fontSize: "12px",
    color: "#9ca3af",
    marginBottom: "10px",
  },

  switchRow: { display: "flex", gap: "10px" },

  tab: {
    flex: 1,
    padding: "8px",
    background: "#1f2937",
    color: "white",
    border: "none",
  },

  activeTab: {
    flex: 1,
    padding: "8px",
    background: "#4f46e5",
    color: "white",
    border: "none",
  },

  textarea: {
    width: "100%",
    height: "250px",
    marginTop: "10px",
    background: "#0b1220",
    color: "white",
    padding: "10px",
  },

  dropZone: {
    marginTop: "10px",
    padding: "20px",
    border: "2px dashed #6366f1",
    textAlign: "center",
    position: "relative",
    cursor: "pointer",
  },

  hiddenFile: {
    opacity: 0,
    position: "absolute",
    width: "100%",
    height: "100%",
    top: 0,
    left: 0,
    cursor: "pointer",
  },

  analyzeBtn: {
    marginTop: "10px",
    width: "100%",
    padding: "10px",
    background: "#6366f1",
    color: "white",
    border: "none",
  },

  scanning: {
    padding: "10px",
    background: "rgba(99,102,241,0.2)",
    marginBottom: "10px",
  },

  timeline: {
    fontSize: "12px",
    color: "#9ca3af",
    marginBottom: "10px",
  },

  card: {
    background: "rgba(255,255,255,0.05)",
    padding: "10px",
    marginBottom: "10px",
  },

  label: {
    fontSize: "12px",
    color: "#9ca3af",
    marginBottom: "5px",
  },
};