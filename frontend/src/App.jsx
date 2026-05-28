import { useEffect, useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("text");

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const [result, setResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");

  const typeText = (text, setter) => {
    setter("");
    let i = 0;

    const interval = setInterval(() => {
      setter((prev) => prev + (text[i] || ""));
      i++;

      if (i >= text.length) clearInterval(interval);
    }, 12);
  };

  useEffect(() => {
    let interval;

    if (loading) {
      interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 95) return prev;
          return prev + 5;
        });
      }, 350);
    }

    return () => clearInterval(interval);
  }, [loading]);

  const analyzeLetter = async () => {
    setLoading(true);
    setProgress(10);
    setResult(null);
    setAnimatedSummary("");

    try {
      let response;

      if (mode === "text") {
        response = await fetch("http://localhost:8000/analyze-text", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            letter_text: text,
          }),
        });
      } else {
        if (!file) {
          alert("Please upload PDF");
          setLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append("file", file);

        response = await fetch("http://localhost:8000/analyze-pdf", {
          method: "POST",
          body: formData,
        });
      }

      const data = await response.json();

      setProgress(100);

      setTimeout(() => {
        setResult(data);

        typeText(
          data.tldr || data.summary || "No summary available",
          setAnimatedSummary
        );

        setLoading(false);
      }, 700);
    } catch (err) {
      console.log(err);
      alert("Backend connection failed");
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      {/* HEADER */}

      <div style={styles.topBar}>
        <div style={styles.brandRow}>
          <div style={styles.logo}>MS</div>

          <div>
            <div style={styles.brand}>Official Letter Assistant</div>
          </div>
        </div>

        <div style={styles.topRight}>
          <div style={styles.systemReady}>
            <span style={styles.greenDot}></span>
            System ready
          </div>

          <button style={styles.aboutBtn}>About</button>
        </div>
      </div>

      {/* MAIN GRID */}

      <div style={styles.grid}>
        {/* LEFT */}

        <div style={styles.leftPanel}>
          <div style={styles.sectionNumber}>1. Input Document</div>

          <div style={styles.switchRow}>
            <button
              onClick={() => setMode("text")}
              style={mode === "text" ? styles.activeTab : styles.tab}
            >
              📄 Text
            </button>

            <button
              onClick={() => setMode("pdf")}
              style={mode === "pdf" ? styles.activeTab : styles.tab}
            >
              📑 PDF
            </button>
          </div>

          {mode === "text" ? (
            <>
              <div style={styles.inputLabel}>
                Paste German official letter
              </div>

              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste or type the letter text here..."
                style={styles.textarea}
              />

              <div style={styles.counter}>
                {text.length} / 100000
              </div>
            </>
          ) : (
            <div style={styles.dropZone}>
              <input
                type="file"
                accept="application/pdf"
                style={styles.hiddenInput}
                onChange={(e) => setFile(e.target.files[0])}
              />

              <div style={styles.dropText}>
                📄 Drop PDF here or click
              </div>

              {file && (
                <div style={styles.fileName}>{file.name}</div>
              )}
            </div>
          )}

          <button
            style={styles.analyzeBtn}
            onClick={analyzeLetter}
          >
            ✨ Analyze Document
          </button>

          {/* SECURITY */}

          <div style={styles.infoCard}>
            <div style={styles.infoTitle}>🔒 Your data is not stored.</div>

            <div style={styles.infoText}>
              Analysis is done securely and privately.
            </div>
          </div>

          {/* PROGRESS */}

          <div style={styles.progressCard}>
            <div style={styles.progressTitle}>
              Analysis progress
            </div>

            <ProgressItem
              done={progress >= 20}
              label="Document received"
            />

            <ProgressItem
              done={progress >= 45}
              label="Preparing document text"
            />

            <ProgressItem
              done={progress >= 70}
              label="Structured analysis running"
            />

            <ProgressItem
              done={progress >= 100}
              label="Generating response"
            />
          </div>

          <div style={styles.howCard}>
            <div style={styles.howTitle}>💡 How it works</div>

            <div style={styles.howText}>
              We analyze your letter and extract important
              information in an easy-to-understand way.
            </div>
          </div>
        </div>

        {/* RIGHT */}

        <div style={styles.rightPanel}>
          <div style={styles.sectionNumber}>
            2. Analysis Result
          </div>

          {!result && !loading && (
            <div style={styles.emptyState}>
              Upload a document to see structured analysis
            </div>
          )}

          {loading && (
            <div>
              <div style={styles.heroSkeleton}></div>

              <div style={styles.skeletonGrid}>
                <div style={styles.skeletonCard}></div>
                <div style={styles.skeletonCard}></div>
                <div style={styles.skeletonCard}></div>
                <div style={styles.skeletonCard}></div>
              </div>
            </div>
          )}

          {result && (
            <>
              {/* HERO */}

              <div style={styles.heroCard}>
                <div style={styles.heroTop}>
                  <div style={styles.heroTitle}>
                    ✨ Bottom line
                  </div>
                </div>

                <div style={styles.heroText}>
                  {animatedSummary}
                </div>

                <div style={styles.metaSection}>
                  <div style={styles.metaBox}>
                    <div style={styles.metaLabel}>
                      Urgency
                    </div>

                    <div style={styles.orangeBadge}>
                      {result?.urgency_level || "Medium"}
                    </div>
                  </div>

                  <div style={styles.metaBox}>
                    <div style={styles.metaLabel}>
                      Sender
                    </div>

                    <div style={styles.metaValue}>
                      {result?.sender || "—"}
                    </div>
                  </div>

                  <div style={styles.metaBox}>
                    <div style={styles.metaLabel}>
                      Topic
                    </div>

                    <div style={styles.metaValue}>
                      {result?.letter_topic || "—"}
                    </div>
                  </div>
                </div>
              </div>

              {/* ACTIONS */}

              <Card title="✅ What you need to do">
                {(result?.required_actions || []).map(
                  (a, i) => (
                    <div key={i} style={styles.actionItem}>
                      <div style={styles.checkbox}></div>
                      {a}
                    </div>
                  )
                )}
              </Card>

              {/* GRID */}

              <div style={styles.grid2}>
                <Card title="📅 Dates and deadlines">
                  {(result?.deadlines || []).map((d, i) => (
                    <div key={i} style={styles.listItem}>
                      {d}
                    </div>
                  ))}
                </Card>

                <Card title="💳 Payment details">
                  {(result?.payment_information || []).map(
                    (p, i) => (
                      <div
                        key={i}
                        style={styles.listItem}
                      >
                        {p}
                      </div>
                    )
                  )}
                </Card>
              </div>

              <div style={styles.grid2}>
                <Card title="📄 Documents needed">
                  {(result?.required_documents || []).map(
                    (d, i) => (
                      <div
                        key={i}
                        style={styles.listItem}
                      >
                        {d}
                      </div>
                    )
                  )}
                </Card>

                <Card title="ℹ️ Useful details">
                  {(result?.useful_details || []).map(
                    (u, i) => (
                      <div
                        key={i}
                        style={styles.listItem}
                      >
                        {u}
                      </div>
                    )
                  )}
                </Card>
              </div>

              <div style={styles.grid2}>
                <div style={styles.warningCard}>
                  <div style={styles.cardTitle}>
                    ⚠️ Possible consequences
                  </div>

                  {(result?.possible_consequences || []).map(
                    (c, i) => (
                      <div
                        key={i}
                        style={styles.listItem}
                      >
                        {c}
                      </div>
                    )
                  )}
                </div>

                <div style={styles.purpleCard}>
                  <div style={styles.cardTitle}>
                    🛡 Things to double-check
                  </div>

                  {(result?.unclear_or_risky_parts || []).map(
                    (c, i) => (
                      <div
                        key={i}
                        style={styles.listItem}
                      >
                        {c}
                      </div>
                    )
                  )}
                </div>
              </div>

              <div style={styles.safetyCard}>
                🛡{" "}
                {result?.safety_note ||
                  "This analysis is informational only."}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

/* REUSABLE */

function Card({ title, children }) {
  return (
    <div style={styles.card}>
      <div style={styles.cardTitle}>{title}</div>
      {children}
    </div>
  );
}

function ProgressItem({ done, label }) {
  return (
    <div style={styles.progressItem}>
      <div
        style={{
          ...styles.progressCircle,
          background: done ? "#2563eb" : "white",
          border: done
            ? "2px solid #2563eb"
            : "2px solid #cbd5e1",
        }}
      >
        {done && "✓"}
      </div>

      <div style={styles.progressLabel}>{label}</div>
    </div>
  );
}

/* STYLES */

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f3f6fb",
    fontFamily:
      "-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
    color: "#111827",
  },

  topBar: {
    height: 72,
    background: "white",
    borderBottom: "1px solid #e5e7eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 28px",
  },

  brandRow: {
    display: "flex",
    alignItems: "center",
    gap: 12,
  },

  logo: {
    width: 36,
    height: 36,
    borderRadius: 12,
    background:
      "linear-gradient(135deg,#2563eb,#1d4ed8)",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 700,
  },

  brand: {
    fontWeight: 700,
    fontSize: 22,
  },

  topRight: {
    display: "flex",
    alignItems: "center",
    gap: 16,
  },

  systemReady: {
    display: "flex",
    alignItems: "center",
    gap: 8,
    fontSize: 14,
    color: "#374151",
  },

  greenDot: {
    width: 10,
    height: 10,
    borderRadius: 999,
    background: "#22c55e",
  },

  aboutBtn: {
    border: "1px solid #e5e7eb",
    background: "white",
    padding: "8px 14px",
    borderRadius: 10,
    cursor: "pointer",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "360px 1fr",
    gap: 22,
    padding: 22,
  },

  leftPanel: {
    background: "white",
    borderRadius: 20,
    padding: 24,
    border: "1px solid #e5e7eb",
  },

  rightPanel: {
    background: "white",
    borderRadius: 20,
    padding: 24,
    border: "1px solid #e5e7eb",
  },

  sectionNumber: {
    fontSize: 24,
    fontWeight: 700,
    marginBottom: 18,
  },

  switchRow: {
    display: "flex",
    gap: 10,
    marginBottom: 16,
  },

  tab: {
    flex: 1,
    padding: 12,
    borderRadius: 12,
    border: "1px solid #e5e7eb",
    background: "#f8fafc",
    cursor: "pointer",
  },

  activeTab: {
    flex: 1,
    padding: 12,
    borderRadius: 12,
    border: "1px solid #2563eb",
    background: "#eff6ff",
    color: "#2563eb",
    fontWeight: 600,
    cursor: "pointer",
  },

  inputLabel: {
    fontSize: 14,
    marginBottom: 10,
    color: "#374151",
  },

  textarea: {
    width: "100%",
    height: 280,
    resize: "none",
    border: "1px solid #dbe3ee",
    borderRadius: 16,
    padding: 16,
    fontSize: 14,
    outline: "none",
    background: "#fafcff",
  },

  counter: {
    textAlign: "right",
    marginTop: 8,
    fontSize: 12,
    color: "#9ca3af",
  },

  dropZone: {
    border: "2px dashed #c7d2fe",
    borderRadius: 18,
    padding: 40,
    textAlign: "center",
    position: "relative",
    background: "#f8fbff",
  },

  hiddenInput: {
    position: "absolute",
    inset: 0,
    opacity: 0,
    cursor: "pointer",
  },

  dropText: {
    fontSize: 15,
    color: "#4b5563",
  },

  fileName: {
    marginTop: 10,
    color: "#2563eb",
  },

  analyzeBtn: {
    width: "100%",
    marginTop: 18,
    padding: 16,
    borderRadius: 14,
    border: "none",
    background:
      "linear-gradient(135deg,#2563eb,#1d4ed8)",
    color: "white",
    fontWeight: 700,
    fontSize: 15,
    cursor: "pointer",
    transition: "0.2s",
  },

  infoCard: {
    marginTop: 18,
    border: "1px solid #e5e7eb",
    borderRadius: 16,
    padding: 16,
  },

  infoTitle: {
    fontWeight: 600,
    marginBottom: 4,
  },

  infoText: {
    fontSize: 13,
    color: "#6b7280",
  },

  progressCard: {
    marginTop: 18,
    border: "1px solid #e5e7eb",
    borderRadius: 16,
    padding: 18,
  },

  progressTitle: {
    fontWeight: 600,
    marginBottom: 18,
  },

  progressItem: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 16,
  },

  progressCircle: {
    width: 24,
    height: 24,
    borderRadius: 999,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 12,
    color: "white",
    transition: "0.3s",
  },

  progressLabel: {
    fontSize: 14,
  },

  howCard: {
    marginTop: 18,
    background: "#f8fafc",
    padding: 18,
    borderRadius: 16,
  },

  howTitle: {
    fontWeight: 600,
    marginBottom: 8,
  },

  howText: {
    fontSize: 14,
    color: "#6b7280",
    lineHeight: 1.6,
  },

  emptyState: {
    height: 400,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#94a3b8",
  },

  heroCard: {
    background:
      "linear-gradient(135deg,#f8fbff,#eef4ff)",
    border: "1px solid #dbeafe",
    borderRadius: 22,
    padding: 24,
    marginBottom: 18,
  },

  heroTop: {
    display: "flex",
    justifyContent: "space-between",
  },

  heroTitle: {
    fontSize: 15,
    fontWeight: 700,
    color: "#1d4ed8",
  },

  heroText: {
    marginTop: 14,
    fontSize: 34,
    fontWeight: 700,
    lineHeight: 1.35,
  },

  metaSection: {
    display: "flex",
    gap: 24,
    marginTop: 24,
    flexWrap: "wrap",
  },

  metaBox: {},

  metaLabel: {
    fontSize: 12,
    color: "#6b7280",
    marginBottom: 6,
  },

  metaValue: {
    fontWeight: 600,
  },

  orangeBadge: {
    display: "inline-flex",
    background: "#ffedd5",
    color: "#ea580c",
    padding: "6px 12px",
    borderRadius: 999,
    fontWeight: 700,
    fontSize: 12,
  },

  card: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: 18,
    padding: 20,
    marginBottom: 16,
  },

  warningCard: {
    background: "#fff7ed",
    border: "1px solid #fed7aa",
    borderRadius: 18,
    padding: 20,
  },

  purpleCard: {
    background: "#faf5ff",
    border: "1px solid #e9d5ff",
    borderRadius: 18,
    padding: 20,
  },

  cardTitle: {
    fontWeight: 700,
    marginBottom: 16,
  },

  actionItem: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    padding: "12px 0",
    borderBottom: "1px solid #f1f5f9",
  },

  checkbox: {
    width: 18,
    height: 18,
    borderRadius: 6,
    border: "2px solid #cbd5e1",
  },

  listItem: {
    padding: "8px 0",
    color: "#475569",
    lineHeight: 1.6,
  },

  grid2: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 16,
    marginBottom: 16,
  },

  safetyCard: {
    background: "#f0fdf4",
    border: "1px solid #bbf7d0",
    borderRadius: 18,
    padding: 18,
    marginTop: 10,
  },

  heroSkeleton: {
    height: 220,
    borderRadius: 20,
    background:
      "linear-gradient(90deg,#f1f5f9,#e2e8f0,#f1f5f9)",
    backgroundSize: "200% 100%",
    animation: "pulse 1.5s infinite",
    marginBottom: 18,
  },

  skeletonGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 16,
  },

  skeletonCard: {
    height: 180,
    borderRadius: 18,
    background:
      "linear-gradient(90deg,#f1f5f9,#e2e8f0,#f1f5f9)",
    backgroundSize: "200% 100%",
    animation: "pulse 1.5s infinite",
  },
};