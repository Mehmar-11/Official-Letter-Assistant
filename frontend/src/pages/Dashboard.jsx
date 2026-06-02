import { useState, useEffect, useRef } from "react";

export default function Dashboard({ onBack }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("text");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");
  const [activeDetail, setActiveDetail] = useState("payment");
  const [showAbout, setShowAbout] = useState(false);
  const typewriterRef = useRef(null);
  const fileInputRef = useRef(null);

  const startTypewriter = (fullText) => {
    if (typewriterRef.current) clearInterval(typewriterRef.current);
    setAnimatedSummary("");
    if (!fullText) return;
    let pos = 0;
    const interval = setInterval(() => {
      if (pos <= fullText.length) {
        setAnimatedSummary(fullText.substring(0, pos));
        pos++;
      } else {
        clearInterval(interval);
        typewriterRef.current = null;
      }
    }, 25);
    typewriterRef.current = interval;
  };

  const handleFileSelect = (e) => {
    const f = e.target.files[0];
    if (f && f.type === "application/pdf") setFile(f);
    else alert("Please select a valid PDF file");
  };

  const handleDropZoneClick = () => fileInputRef.current?.click();
  const handleDragOver = (e) => { e.preventDefault(); e.stopPropagation(); };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const f = e.dataTransfer.files[0];
    if (f && f.type === "application/pdf") setFile(f);
    else alert("Please drop a valid PDF");
  };

  const analyzeLetter = async () => {
    if (mode === "text" && !text.trim()) return alert("Please paste your letter text");
    if (mode === "pdf" && !file) return alert("Please upload a PDF file");

    setLoading(true);
    setResult(null);
    setAnimatedSummary("");

    try {
      let response;
      if (mode === "text") {
        // ✅ Send JSON for text analysis
        response = await fetch("http://localhost:8000/analyze-text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ letter_text: text }),
        });
      } else {
        // ✅ Send FormData for PDF
        const formData = new FormData();
        formData.append("file", file);
        response = await fetch("http://localhost:8000/analyze-pdf", {
          method: "POST",
          body: formData,
        });
      }

      if (!response.ok) throw new Error("Backend error");
      const data = await response.json();
      setResult(data);
      startTypewriter(data.tldr || data.summary || "No summary available");
    } catch (err) {
      console.error(err);
      alert("Backend connection failed. Make sure the server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    if (typewriterRef.current) clearInterval(typewriterRef.current);
    setResult(null);
    setAnimatedSummary("");
    setText("");
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const detailSections = {
    payment: { title: "Payment details", content: result?.payment_information || [] },
    documents: { title: "Documents needed", content: result?.required_documents || [] },
    consequences: { title: "What happens if I ignore this?", content: result?.possible_consequences || [] },
    careful: { title: "Things to be careful about", content: result?.unclear_or_risky_parts || [] },
  };

  return (
    <div style={styles.page}>
      <div style={styles.topBar}>
        <div style={styles.brandRow}>
          <div style={styles.logo}>MS</div>
          <div style={styles.brand}>German Official Letter Assistant</div>
        </div>
        <div style={styles.topRight}>
          <button style={styles.backBtn} onClick={onBack}>← Back to Home</button>
          <button style={styles.aboutBtn} onClick={() => setShowAbout(true)}>About</button>
        </div>
      </div>

      <div style={styles.mainContainer}>
        {/* Left Panel */}
        <div style={styles.leftPanel}>
          <div style={styles.sectionNumber}>1. Add your letter</div>
          <div style={styles.switchRow}>
            <button onClick={() => setMode("text")} style={mode === "text" ? styles.activeTab : styles.tab}>📄 Paste Text</button>
            <button onClick={() => setMode("pdf")} style={mode === "pdf" ? styles.activeTab : styles.tab}>📑 Upload PDF</button>
          </div>

          {mode === "text" ? (
            <>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your official letter here..."
                style={styles.textarea}
                rows={8}
              />
              <div style={styles.counter}>{text.length.toLocaleString()} characters</div>
            </>
          ) : (
            <div style={styles.dropZone} onClick={handleDropZoneClick} onDragOver={handleDragOver} onDrop={handleDrop}>
              <input type="file" ref={fileInputRef} accept="application/pdf" style={styles.hiddenInput} onChange={handleFileSelect} />
              <div style={styles.dropIcon}>📄</div>
              <div style={styles.dropText}>Drop PDF here or click to upload</div>
              <div style={styles.dropSubtext}>Supported format: PDF (Max 10MB)</div>
              {file && <div style={styles.fileName}>✓ Selected: {file.name}</div>}
            </div>
          )}

          <button style={styles.analyzeBtn} onClick={analyzeLetter} disabled={loading}>
            {loading ? "⏳ Analyzing..." : "✨ Analyze Letter"}
          </button>

          {loading && (
            <div style={styles.loadingCard}>
              <div style={styles.spinner}></div>
              <div style={styles.loadingText}>Analyzing your letter...</div>
            </div>
          )}

          <div style={styles.infoCard}>
            <div style={styles.infoTitle}>🔒 Your data is private</div>
            <div style={styles.infoText}>Document processed temporarily, not stored.</div>
            <div style={styles.infoText}><span style={{ color: "#ef4444" }}>⚠️ AI can make mistakes.</span> Not legal advice.</div>
          </div>
        </div>

        {/* Right Panel */}
        <div style={styles.rightPanel}>
          <div style={styles.sectionNumber}>2. Analysis Result</div>

          {!result && !loading && (
            <div style={styles.emptyState}>
              <div>📄 No letter analyzed yet</div>
              <div style={{ fontSize: 13, marginTop: 8, color: "#94a3b8" }}>Paste or upload a letter to see analysis</div>
            </div>
          )}

          {loading && !result && (
            <div>
              <div style={styles.heroSkeleton}></div>
              <div style={styles.skeletonCard}></div>
            </div>
          )}

          {result && (
            <div style={styles.resultContent}>
              <div style={styles.heroCard}>
                <div style={styles.heroTitle}>✨ Bottom line</div>
                <div style={styles.heroText}>{animatedSummary || result.tldr}</div>
                <div style={styles.metaSection}>
                  <div><div style={styles.metaLabel}>Urgency</div><div style={styles.orangeBadge}>{result.urgency_level || "Medium"}</div></div>
                  <div><div style={styles.metaLabel}>Sender</div><div style={styles.metaValue}>{result.sender || "—"}</div></div>
                  <div><div style={styles.metaLabel}>Topic</div><div style={styles.metaValue}>{result.letter_topic || "—"}</div></div>
                </div>
              </div>

              {/* What you need to do – without checkboxes */}
              <div style={styles.card}>
                <div style={styles.cardTitle}>✅ What you need to do</div>
                {(result.required_actions || []).map((action, i) => (
                  <div key={i} style={styles.actionItemPlain}>
                    {i+1}. {action}
                  </div>
                ))}
              </div>

              <div style={styles.specificDetailsSection}>
                <div style={styles.specificDetailsTitle}>🔍 Check specific details</div>
                <div style={styles.specificDetailsSub}>Explore key aspects of this letter.</div>
                <div style={styles.detailButtons}>
                  <button onClick={() => setActiveDetail("payment")} style={activeDetail === "payment" ? styles.detailBtnActive : styles.detailBtn}>💳 Payment details</button>
                  <button onClick={() => setActiveDetail("documents")} style={activeDetail === "documents" ? styles.detailBtnActive : styles.detailBtn}>📄 Documents needed</button>
                  <button onClick={() => setActiveDetail("consequences")} style={activeDetail === "consequences" ? styles.detailBtnActive : styles.detailBtn}>⚠️ What happens if I ignore this?</button>
                  <button onClick={() => setActiveDetail("careful")} style={activeDetail === "careful" ? styles.detailBtnActive : styles.detailBtn}>🛡 Things to be careful about</button>
                </div>
                <div style={styles.detailContent}>
                  <div style={styles.detailContentTitle}>{detailSections[activeDetail].title}</div>
                  {detailSections[activeDetail].content.map((item, i) => (
                    <div key={i} style={styles.detailContentItem}>• {item}</div>
                  ))}
                </div>
              </div>

              {/* Additional details (duplicate section removed) */}
              <div style={styles.additionalDetailsCard}>
                <div style={styles.additionalDetailsTitle}>📌 Additional details</div>
                <div style={styles.additionalDetailsContent}>
                  Reference numbers and other extra details from the letter.<br /><br />
                  • {result.useful_details?.[0] || "None"}
                </div>
              </div>

              <div style={styles.safetyCard}>🛡 {result.safety_note || "This is AI-generated help, not legal advice."}</div>

              <button style={styles.newAnalysisBtn} onClick={resetAnalysis}>🔄 Analyze Another Letter</button>
            </div>
          )}
        </div>
      </div>

      {/* About Modal */}
      {showAbout && (
        <div style={styles.modalOverlay} onClick={() => setShowAbout(false)}>
          <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <h3>ℹ️ German Official Letter Assistant</h3>
            <p><strong>Version:</strong> 1.0</p>
            <p><strong>How it works:</strong> AI extracts key information from official German letters – deadlines, payment details, risks – and presents them in a clear, actionable format.</p>
            <p><strong>Privacy:</strong> Your documents are processed temporarily and not stored.</p>
            <p><strong>Disclaimer:</strong> This is AI‑generated help, not legal advice. Always verify with the issuing organization.</p>
            <button style={styles.modalClose} onClick={() => setShowAbout(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  page: { height: "100vh", width: "100vw", background: "#f3f6fb", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", color: "#111827", display: "flex", flexDirection: "column", overflow: "hidden", boxSizing: "border-box" },
  topBar: { height: 56, background: "white", borderBottom: "1px solid #e5e7eb", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 20px", flexShrink: 0 },
  brandRow: { display: "flex", alignItems: "center", gap: 8 },
  logo: { width: 32, height: 32, borderRadius: 8, background: "linear-gradient(135deg, #2563eb, #1d4ed8)", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700, fontSize: 16 },
  brand: { fontWeight: 700, fontSize: 16 },
  topRight: { display: "flex", alignItems: "center", gap: 12 },
  backBtn: { border: "1px solid #2563eb", background: "#eff6ff", color: "#2563eb", padding: "4px 10px", borderRadius: 6, cursor: "pointer", fontSize: 11, fontWeight: 500 },
  aboutBtn: { border: "1px solid #e5e7eb", background: "white", padding: "4px 10px", borderRadius: 6, cursor: "pointer", fontSize: 11 },
  mainContainer: { display: "flex", gap: 12, padding: 12, flex: 1, minHeight: 0, overflow: "hidden" },
  leftPanel: { width: 360, background: "white", borderRadius: 16, border: "1px solid #e5e7eb", padding: 14, display: "flex", flexDirection: "column", overflowY: "auto", gap: 10, flexShrink: 0 },
  rightPanel: { flex: 1, background: "white", borderRadius: 16, border: "1px solid #e5e7eb", padding: 14, overflowY: "auto" },
  sectionNumber: { fontSize: 15, fontWeight: 700, marginBottom: 8 },
  switchRow: { display: "flex", gap: 8, marginBottom: 10 },
  tab: { flex: 1, padding: "6px 0", borderRadius: 40, border: "1px solid #e5e7eb", background: "#f8fafc", cursor: "pointer", textAlign: "center", fontSize: 11, fontWeight: 500 },
  activeTab: { flex: 1, padding: "6px 0", borderRadius: 40, border: "1px solid #2563eb", background: "#eff6ff", color: "#2563eb", fontWeight: 600, cursor: "pointer", textAlign: "center", fontSize: 11 },
  textarea: { width: "100%", minHeight: 160, border: "1px solid #dbe3ee", borderRadius: 12, padding: 10, fontSize: 12, outline: "none", background: "#fafcff", fontFamily: "monospace", resize: "vertical" },
  counter: { textAlign: "right", marginTop: 4, fontSize: 10, color: "#9ca3af" },
  dropZone: { border: "2px dashed #c7d2fe", borderRadius: 12, padding: 20, textAlign: "center", background: "#f8fbff", cursor: "pointer", minHeight: 160, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 6 },
  dropIcon: { fontSize: 32 }, dropText: { fontSize: 12, color: "#4b5563", fontWeight: 500 }, dropSubtext: { fontSize: 10, color: "#9ca3af" }, hiddenInput: { display: "none" }, fileName: { marginTop: 6, color: "#2563eb", fontSize: 11, fontWeight: 500 },
  analyzeBtn: { width: "100%", marginTop: 10, padding: 10, borderRadius: 40, border: "none", background: "linear-gradient(135deg, #2563eb, #1d4ed8)", color: "white", fontWeight: 600, fontSize: 13, cursor: "pointer" },
  loadingCard: { marginTop: 10, padding: 12, background: "#f8fafc", borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center", gap: 10, border: "1px solid #e2e8f0" },
  spinner: { width: 20, height: 20, border: "3px solid #e2e8f0", borderTop: "3px solid #2563eb", borderRadius: "50%", animation: "spin 1s linear infinite" },
  loadingText: { fontSize: 12, color: "#475569", fontWeight: 500 },
  infoCard: { marginTop: 10, border: "1px solid #fef3c7", borderRadius: 12, padding: 10, background: "#fffbeb" }, infoTitle: { fontWeight: 600, marginBottom: 4, fontSize: 11 }, infoText: { fontSize: 9, color: "#6b7280", marginTop: 2 },
  emptyState: { height: 250, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: "#94a3b8", textAlign: "center" },
  resultContent: { display: "flex", flexDirection: "column", gap: 10 },
  heroCard: { background: "#fefce8", border: "1px solid #fef08a", borderRadius: 14, padding: 12, marginBottom: 2 }, heroTitle: { fontSize: 10, fontWeight: 700, color: "#ca8a04", textTransform: "uppercase" }, heroText: { marginTop: 6, fontSize: 15, fontWeight: 700, lineHeight: 1.3, color: "#1e293b" },
  metaSection: { display: "flex", gap: 16, marginTop: 12, flexWrap: "wrap" }, metaLabel: { fontSize: 9, color: "#6b7280", marginBottom: 2 }, metaValue: { fontWeight: 600, fontSize: 11 }, orangeBadge: { display: "inline-flex", background: "#ffedd5", color: "#ea580c", padding: "2px 8px", borderRadius: 40, fontWeight: 600, fontSize: 9 },
  card: { background: "white", border: "1px solid #e2e8f0", borderRadius: 12, padding: 12, marginBottom: 2 }, cardTitle: { fontWeight: 700, marginBottom: 8, fontSize: 12 },
  actionItemPlain: { padding: "6px 0", borderBottom: "1px solid #f1f5f9", fontSize: 11, color: "#1e293b" },
  specificDetailsSection: { background: "#f8fafc", borderRadius: 12, padding: 12, marginBottom: 2 }, specificDetailsTitle: { fontWeight: 700, fontSize: 13, marginBottom: 2 }, specificDetailsSub: { fontSize: 10, color: "#64748b", marginBottom: 10 },
  detailButtons: { display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 10 }, detailBtn: { padding: "4px 10px", borderRadius: 40, border: "1px solid #e2e8f0", background: "white", cursor: "pointer", fontSize: 10, fontWeight: 500 }, detailBtnActive: { padding: "4px 10px", borderRadius: 40, border: "1px solid #2563eb", background: "#eff6ff", color: "#2563eb", cursor: "pointer", fontSize: 10, fontWeight: 600 },
  detailContent: { background: "white", borderRadius: 10, padding: 10, border: "1px solid #e2e8f0" }, detailContentTitle: { fontWeight: 700, marginBottom: 8, fontSize: 11 }, detailContentItem: { padding: "4px 0", fontSize: 10, color: "#475569", borderBottom: "1px solid #f1f5f9" },
  additionalDetailsCard: { background: "#f3e8ff", borderRadius: 12, padding: 12, marginBottom: 2 }, additionalDetailsTitle: { fontWeight: 700, fontSize: 11, marginBottom: 8, color: "#6b21a5" }, additionalDetailsContent: { fontSize: 10, color: "#4c1d95", lineHeight: 1.5 },
  safetyCard: { background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 12, padding: 10, fontSize: 10, color: "#166534" },
  newAnalysisBtn: { width: "100%", marginTop: 12, padding: 8, borderRadius: 40, border: "1px solid #2563eb", background: "white", color: "#2563eb", fontWeight: 600, fontSize: 12, cursor: "pointer" },
  heroSkeleton: { height: 120, borderRadius: 14, background: "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)", backgroundSize: "200% 100%", marginBottom: 10 },
  skeletonCard: { height: 140, borderRadius: 12, background: "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)", backgroundSize: "200% 100%" },
  modalOverlay: { position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 },
  modalContent: { background: "white", padding: 24, borderRadius: 24, maxWidth: 450, width: "90%", boxShadow: "0 20px 35px -10px black" },
  modalClose: { marginTop: 16, padding: "8px 16px", background: "#2563eb", color: "white", border: "none", borderRadius: 40, cursor: "pointer" },
};

// Add keyframe animation for spinner
const styleSheet = document.createElement("style");
styleSheet.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
document.head.appendChild(styleSheet);