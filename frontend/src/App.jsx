import { useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [mode, setMode] = useState("text");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");

  // TYPEWRITER EFFECT
  const typeText = (text, setter) => {
    setter("");
    let i = 0;

    const interval = setInterval(() => {
      setter((prev) => prev + (text[i] || ""));
      i++;
      if (i >= text.length) clearInterval(interval);
    }, 15);
  };

  // ANALYZE FUNCTION (backend ready)
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
        <div style={styles.brand}>Official Letter Intelligence</div>
        <div style={styles.status}>● System Ready</div>
      </div>

      {/* GRID */}
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

          {/* INPUT */}
          {mode === "text" ? (
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste German official letter..."
              style={styles.textarea}
            />
          ) : (
            <div
              style={styles.dropZone}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                alert("PDF drop detected (backend connect next step)");
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
              />
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

          {/* SCANNING */}
          {loading && (
            <div style={styles.scanning}>
              📡 Scanning document...
            </div>
          )}

          {/* TIMELINE */}
          <div style={styles.timeline}>
            <div>📄 Document received</div>
            <div>🔍 Extracting text</div>
            <div>🧹 Cleaning sensitive data</div>
            <div>🧠 AI analysis running</div>
          </div>

          {/* CONFIDENCE */}
          <div style={styles.card}>
            <div style={styles.label}>AI Confidence</div>
            <div style={styles.barBg}>
              <div style={styles.barFill}></div>
            </div>
          </div>

          {/* RESULTS */}
          <div style={styles.card}>
            <div style={styles.label}>Summary</div>
            <div>{animatedSummary || "Waiting for analysis..."}</div>
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
            <div style={styles.label}>Risk Signals</div>
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
    display: "flex",
    flexDirection: "column",
  },

  topBar: {
    display: "flex",
    justifyContent: "space-between",
    padding: "16px 30px",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
  },

  brand: {
    fontSize: "16px",
    fontWeight: "600",
  },

  status: {
    color: "#22c55e",
    fontSize: "12px",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
    padding: "20px",
    flex: 1,
  },

  leftPanel: {
    background: "rgba(17, 25, 40, 0.7)",
    backdropFilter: "blur(12px)",
    border: "1px solid rgba(255,255,255,0.08)",
    padding: "20px",
    borderRadius: "16px",
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },

  rightPanel: {
    background: "rgba(17, 25, 40, 0.6)",
    backdropFilter: "blur(12px)",
    border: "1px solid rgba(255,255,255,0.08)",
    padding: "20px",
    borderRadius: "16px",
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },

  panelTitle: {
    fontSize: "12px",
    color: "#9ca3af",
  },

  switchRow: {
    display: "flex",
    gap: "10px",
  },

  tab: {
    flex: 1,
    padding: "8px",
    background: "#1f2937",
    border: "none",
    color: "white",
    borderRadius: "8px",
  },

  activeTab: {
    flex: 1,
    padding: "8px",
    background: "#4f46e5",
    border: "none",
    color: "white",
    borderRadius: "8px",
  },

  textarea: {
    height: "250px",
    background: "#0b1220",
    border: "1px solid #374151",
    color: "white",
    padding: "12px",
    borderRadius: "10px",
  },

  dropZone: {
    border: "2px dashed rgba(99,102,241,0.6)",
    padding: "20px",
    borderRadius: "12px",
    textAlign: "center",
    cursor: "pointer",
    background: "rgba(255,255,255,0.02)",
  },

  hiddenFile: {
    opacity: 0,
    position: "absolute",
    width: "100%",
    height: "100%",
  },

  analyzeBtn: {
    padding: "12px",
    background: "#6366f1",
    border: "none",
    color: "white",
    borderRadius: "10px",
    cursor: "pointer",
  },

  scanning: {
    padding: "10px",
    borderRadius: "10px",
    background: "rgba(99,102,241,0.15)",
    border: "1px solid rgba(99,102,241,0.4)",
    animation: "pulse 1.5s infinite",
  },

  timeline: {
    fontSize: "12px",
    color: "#9ca3af",
    lineHeight: "1.8",
    padding: "10px",
    borderLeft: "2px solid #6366f1",
  },

  card: {
    background: "rgba(255,255,255,0.03)",
    padding: "12px",
    borderRadius: "10px",
  },

  label: {
    fontSize: "12px",
    color: "#9ca3af",
    marginBottom: "6px",
  },

  barBg: {
    width: "100%",
    height: "8px",
    background: "#1f2937",
    borderRadius: "10px",
    overflow: "hidden",
  },

  barFill: {
    width: "78%",
    height: "100%",
    background: "linear-gradient(90deg, #6366f1, #22c55e)",
  },
};