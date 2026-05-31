import { useState, useEffect, useRef } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("text");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");
  const [activeDetail, setActiveDetail] = useState("payment");
  const typewriterRef = useRef(null);
  const fileInputRef = useRef(null);

  // Fixed typewriter effect - shows first character correctly
  const typeText = (fullText, setter) => {
    if (typewriterRef.current) {
      clearInterval(typewriterRef.current);
      typewriterRef.current = null;
    }
    
    setter("");
    if (!fullText) return;
    
    let i = 0;
    const interval = setInterval(() => {
      if (i < fullText.length) {
        setter(prev => prev + fullText[i]);
        i++;
      } else {
        clearInterval(interval);
        typewriterRef.current = null;
      }
    }, 15);
    
    typewriterRef.current = interval;
  };

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setProgress(prev => Math.min(prev + 5, 95));
      }, 350);
    }
    return () => clearInterval(interval);
  }, [loading]);

  // Handle file selection
  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
    } else {
      alert("Please select a valid PDF file");
      setFile(null);
    }
  };

  // Trigger file input click
  const handleDropZoneClick = () => {
    fileInputRef.current.click();
  };

  // Handle drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
    } else {
      alert("Please drop a valid PDF file");
    }
  };

  const analyzeLetter = async () => {
    if (mode === "text" && !text.trim()) {
      alert("Please paste your letter text");
      return;
    }
    if (mode === "pdf" && !file) {
      alert("Please upload a PDF file");
      return;
    }

    setLoading(true);
    setProgress(10);
    setResult(null);
    setAnimatedSummary("");

    // Simulate API call
    setTimeout(() => {
      setProgress(100);

      const mockResult = {
        tldr: "You need to pay 89.90 EUR by June 14, 2026 to avoid additional fees.",
        urgency_level: "Medium",
        sender: "VitaPlus Krankenkasse",
        letter_topic: "Reminder for unpaid insurance contribution and return debit fee",
        required_actions: [
          "Pay 89.90 EUR before June 14, 2026.",
          "Upload proof of payment if payment was made after May 20, 2026 by June 10, 2026.",
          "Contact customer service if the payment reference was incorrect."
        ],
        deadlines: ["Payment deadline: June 14, 2026", "Proof upload deadline: June 10, 2026"],
        payment_information: [
          "Amount: 89.90 EUR",
          "Recipient: VitaPlus Krankenkasse",
          "IBAN: DE12 3705 0299 1234 5678 90",
          "Payment deadline: June 14, 2026"
        ],
        required_documents: ["Proof of payment receipt"],
        useful_details: ["Reference number: VPK-45632-2026"],
        possible_consequences: [
          "Additional late fees up to 15 EUR",
          "Possible referral to collection agency"
        ],
        unclear_or_risky_parts: [
          "Verify the IBAN matches your insurance letters",
          "Proof-of-payment condition is strict – upload before June 10"
        ],
        safety_note: "This is AI-generated help, not legal advice. Please verify important decisions with the responsible office or a qualified advisor."
      };

      setResult(mockResult);
      typeText(mockResult.tldr, setAnimatedSummary);
      setLoading(false);
    }, 2000);
  };

  const resetAnalysis = () => {
    setResult(null);
    setAnimatedSummary("");
    setText("");
    setFile(null);
    setProgress(0);
    if (typewriterRef.current) {
      clearInterval(typewriterRef.current);
      typewriterRef.current = null;
    }
  };

  const progressSteps = [
    { label: "Document received", threshold: 20 },
    { label: "Preparing document text", threshold: 45 },
    { label: "Structured analysis running", threshold: 70 },
    { label: "Generating response", threshold: 100 }
  ];

  const detailSections = {
    payment: {
      title: "Payment details",
      content: [
        "Amount: 89.90 EUR",
        "Recipient: VitaPlus Krankenkasse",
        "IBAN: DE12 3705 0299 1234 5678 90",
        "Payment deadline: June 14, 2026",
        "Proof of payment: If paid after May 20, 2026, upload proof by June 10, 2026."
      ]
    },
    documents: {
      title: "Documents needed",
      content: ["Proof of payment receipt"]
    },
    consequences: {
      title: "What happens if I ignore this?",
      content: [
        "Additional late fees up to 15 EUR",
        "Possible referral to collection agency",
        "Reminder fee of 5.00 EUR"
      ]
    },
    careful: {
      title: "Things to be careful about",
      content: [
        "Verify the IBAN matches your insurance letters",
        "Proof-of-payment condition is strict – upload before June 10",
        "Payment reference must be correct"
      ]
    }
  };

  return (
    <div style={styles.page}>
      {/* Header */}
      <div style={styles.topBar}>
        <div style={styles.brandRow}>
          <div style={styles.logo}>📄</div>
          <div style={styles.brand}>MS Letter Assistant</div>
        </div>
        <div style={styles.topRight}>
          <div style={styles.systemReady}>
            <span style={styles.greenDot}></span>
            System ready
          </div>
          <button style={styles.aboutBtn}>About</button>
        </div>
      </div>

      {/* Main Content - Single Page */}
      <div style={styles.mainContainer}>
        {/* Left Column - Input */}
        <div style={styles.leftPanel}>
          <div style={styles.sectionNumber}>1. Add your letter</div>

          <div style={styles.switchRow}>
            <button onClick={() => setMode("text")} style={mode === "text" ? styles.activeTab : styles.tab}>
              📄 Paste Text
            </button>
            <button onClick={() => setMode("pdf")} style={mode === "pdf" ? styles.activeTab : styles.tab}>
              📑 Upload PDF
            </button>
          </div>

          {mode === "text" ? (
            <>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your official letter here..."
                style={styles.textarea}
                rows={10}
              />
              <div style={styles.counter}>{text.length.toLocaleString()} characters</div>
            </>
          ) : (
            <div 
              style={styles.dropZone}
              onClick={handleDropZoneClick}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <input 
                type="file" 
                ref={fileInputRef}
                accept="application/pdf" 
                style={styles.hiddenInput} 
                onChange={handleFileSelect}
              />
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
            <div style={styles.progressCard}>
              <div style={styles.progressTitle}>Analysis progress</div>
              {progressSteps.map((step, idx) => (
                <div key={idx} style={styles.progressItem}>
                  <div style={{
                    ...styles.progressCircle,
                    background: progress >= step.threshold ? "#2563eb" : "white",
                    border: progress >= step.threshold ? "2px solid #2563eb" : "2px solid #cbd5e1",
                    color: progress >= step.threshold ? "white" : "#94a3b8"
                  }}>
                    {progress >= step.threshold && "✓"}
                  </div>
                  <div style={styles.progressLabel}>{step.label}</div>
                </div>
              ))}
            </div>
          )}

          <div style={styles.infoCard}>
            <div style={styles.infoTitle}>🔒 Your data is private</div>
            <div style={styles.infoText}>Document processed temporarily, not stored.</div>
            <div style={styles.infoText}><span style={{ color: "#ef4444" }}>⚠️ AI can make mistakes.</span> Not legal advice.</div>
          </div>
        </div>

        {/* Right Column - Results */}
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
              {/* Bottom Line */}
              <div style={styles.heroCard}>
                <div style={styles.heroTitle}>✨ Bottom line</div>
                <div style={styles.heroText}>{animatedSummary || result.tldr}</div>
                <div style={styles.metaSection}>
                  <div>
                    <div style={styles.metaLabel}>Urgency</div>
                    <div style={styles.orangeBadge}>{result.urgency_level}</div>
                  </div>
                  <div>
                    <div style={styles.metaLabel}>Sender</div>
                    <div style={styles.metaValue}>{result.sender}</div>
                  </div>
                  <div>
                    <div style={styles.metaLabel}>Topic</div>
                    <div style={styles.metaValue}>{result.letter_topic}</div>
                  </div>
                </div>
              </div>

              {/* What you need to do */}
              <div style={styles.card}>
                <div style={styles.cardTitle}>✅ What you need to do</div>
                {result.required_actions.map((action, i) => (
                  <div key={i} style={styles.actionItem}>
                    <div style={styles.checkbox}></div>
                    <div>{i+1}. {action}</div>
                  </div>
                ))}
              </div>

              {/* Check specific details */}
              <div style={styles.specificDetailsSection}>
                <div style={styles.specificDetailsTitle}>🔍 Check specific details</div>
                <div style={styles.specificDetailsSub}>Explore key aspects of this letter.</div>
                
                <div style={styles.detailButtons}>
                  <button onClick={() => setActiveDetail("payment")} style={activeDetail === "payment" ? styles.detailBtnActive : styles.detailBtn}>
                    💳 Payment details
                  </button>
                  <button onClick={() => setActiveDetail("documents")} style={activeDetail === "documents" ? styles.detailBtnActive : styles.detailBtn}>
                    📄 Documents needed
                  </button>
                  <button onClick={() => setActiveDetail("consequences")} style={activeDetail === "consequences" ? styles.detailBtnActive : styles.detailBtn}>
                    ⚠️ What happens if I ignore this?
                  </button>
                  <button onClick={() => setActiveDetail("careful")} style={activeDetail === "careful" ? styles.detailBtnActive : styles.detailBtn}>
                    🛡 Things to be careful about
                  </button>
                </div>

                <div style={styles.detailContent}>
                  <div style={styles.detailContentTitle}>{detailSections[activeDetail].title}</div>
                  {detailSections[activeDetail].content.map((item, i) => (
                    <div key={i} style={styles.detailContentItem}>• {item}</div>
                  ))}
                </div>
              </div>

              {/* Letter includes note */}
              <div style={styles.extraNoteCard}>
                <div style={styles.extraNoteTitle}>📋 The letter includes a payment request and an extra proof-of-payment condition.</div>
                <div style={styles.extraNoteContent}>
                  • Amount: 89.90 EUR<br />
                  • Recipient: VitaPlus Krankenkasse<br />
                  • IBAN: DE12 3705 0299 1234 5678 90<br />
                  • Payment deadline: June 14, 2026<br />
                  • Proof of payment: If paid after May 20, 2026, upload proof by June 10, 2026.
                </div>
              </div>

              {/* Additional details */}
              <div style={styles.additionalDetailsCard}>
                <div style={styles.additionalDetailsTitle}>📌 Additional details</div>
                <div style={styles.additionalDetailsContent}>
                  Reference numbers and other extra details from the letter.<br /><br />
                  • Reference number: VPK-45632-2026
                </div>
              </div>

              {/* Safety note */}
              <div style={styles.safetyCard}>
                🛡 {result.safety_note}
              </div>

              {/* New analysis button */}
              <button style={styles.newAnalysisBtn} onClick={resetAnalysis}>
                🔄 Analyze Another Letter
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    width: "100vw",
    background: "#f3f6fb",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    color: "#111827",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden"
  },
  
  topBar: {
    height: 60,
    background: "white",
    borderBottom: "1px solid #e5e7eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    flexShrink: 0
  },
  
  brandRow: { display: "flex", alignItems: "center", gap: 10 },
  logo: {
    width: 34, height: 34, borderRadius: 10,
    background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
    color: "white", display: "flex", alignItems: "center", justifyContent: "center",
    fontWeight: 700, fontSize: 16
  },
  brand: { fontWeight: 700, fontSize: 18 },
  topRight: { display: "flex", alignItems: "center", gap: 16 },
  systemReady: { display: "flex", alignItems: "center", gap: 8, fontSize: 13, color: "#374151" },
  greenDot: { width: 8, height: 8, borderRadius: 999, background: "#22c55e" },
  aboutBtn: { border: "1px solid #e5e7eb", background: "white", padding: "5px 12px", borderRadius: 8, cursor: "pointer", fontSize: 12 },
  
  mainContainer: {
    display: "flex",
    gap: 16,
    padding: 16,
    flex: 1,
    minHeight: 0,
    overflow: "hidden"
  },
  
  leftPanel: {
    width: 380,
    background: "white",
    borderRadius: 20,
    border: "1px solid #e5e7eb",
    padding: 18,
    display: "flex",
    flexDirection: "column",
    overflowY: "auto",
    flexShrink: 0,
    gap: 12
  },
  
  rightPanel: {
    flex: 1,
    background: "white",
    borderRadius: 20,
    border: "1px solid #e5e7eb",
    padding: 18,
    overflowY: "auto"
  },
  
  sectionNumber: { fontSize: 16, fontWeight: 700, marginBottom: 10 },
  switchRow: { display: "flex", gap: 8, marginBottom: 12 },
  tab: { flex: 1, padding: "8px 0", borderRadius: 40, border: "1px solid #e5e7eb", background: "#f8fafc", cursor: "pointer", textAlign: "center", fontSize: 12, fontWeight: 500 },
  activeTab: { flex: 1, padding: "8px 0", borderRadius: 40, border: "1px solid #2563eb", background: "#eff6ff", color: "#2563eb", fontWeight: 600, cursor: "pointer", textAlign: "center", fontSize: 12 },
  
  textarea: { 
    width: "100%", 
    minHeight: 200,
    border: "1px solid #dbe3ee", 
    borderRadius: 14, 
    padding: 12, 
    fontSize: 13, 
    outline: "none", 
    background: "#fafcff", 
    fontFamily: "monospace",
    resize: "vertical"
  },
  
  counter: { textAlign: "right", marginTop: 4, fontSize: 11, color: "#9ca3af" },
  
  dropZone: { 
    border: "2px dashed #c7d2fe", 
    borderRadius: 14, 
    padding: 30, 
    textAlign: "center", 
    background: "#f8fbff", 
    cursor: "pointer",
    transition: "all 0.2s",
    minHeight: 200,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: 8
  },
  
  dropIcon: { fontSize: 40 },
  dropText: { fontSize: 13, color: "#4b5563", fontWeight: 500 },
  dropSubtext: { fontSize: 11, color: "#9ca3af" },
  hiddenInput: { display: "none" },
  fileName: { marginTop: 8, color: "#2563eb", fontSize: 12, fontWeight: 500 },
  
  analyzeBtn: { 
    width: "100%", 
    marginTop: 12, 
    padding: 12, 
    borderRadius: 40, 
    border: "none", 
    background: "linear-gradient(135deg, #2563eb, #1d4ed8)", 
    color: "white", 
    fontWeight: 600, 
    fontSize: 14, 
    cursor: "pointer",
    transition: "opacity 0.2s"
  },
  
  progressCard: { marginTop: 12, border: "1px solid #e5e7eb", borderRadius: 14, padding: 12 },
  progressTitle: { fontWeight: 600, marginBottom: 10, fontSize: 12 },
  progressItem: { display: "flex", alignItems: "center", gap: 10, marginBottom: 8 },
  progressCircle: { width: 18, height: 18, borderRadius: 999, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 9, fontWeight: "bold" },
  progressLabel: { fontSize: 11 },
  
  infoCard: { marginTop: 12, border: "1px solid #fef3c7", borderRadius: 14, padding: 12, background: "#fffbeb" },
  infoTitle: { fontWeight: 600, marginBottom: 4, fontSize: 12 },
  infoText: { fontSize: 10, color: "#6b7280", marginTop: 2 },
  
  emptyState: { 
    height: 300, 
    display: "flex", 
    flexDirection: "column",
    alignItems: "center", 
    justifyContent: "center", 
    color: "#94a3b8",
    textAlign: "center"
  },
  
  resultContent: { display: "flex", flexDirection: "column", gap: 12 },
  
  heroCard: { background: "#fefce8", border: "1px solid #fef08a", borderRadius: 16, padding: 16, marginBottom: 4 },
  heroTitle: { fontSize: 11, fontWeight: 700, color: "#ca8a04", textTransform: "uppercase" },
  heroText: { marginTop: 8, fontSize: 16, fontWeight: 700, lineHeight: 1.4, color: "#1e293b" },
  metaSection: { display: "flex", gap: 20, marginTop: 16, flexWrap: "wrap" },
  metaLabel: { fontSize: 10, color: "#6b7280", marginBottom: 3 },
  metaValue: { fontWeight: 600, fontSize: 12 },
  orangeBadge: { display: "inline-flex", background: "#ffedd5", color: "#ea580c", padding: "2px 10px", borderRadius: 40, fontWeight: 600, fontSize: 10 },
  
  card: { background: "white", border: "1px solid #e2e8f0", borderRadius: 14, padding: 14, marginBottom: 4 },
  cardTitle: { fontWeight: 700, marginBottom: 10, fontSize: 13 },
  actionItem: { display: "flex", alignItems: "center", gap: 10, padding: "8px 0", borderBottom: "1px solid #f1f5f9", fontSize: 12 },
  checkbox: { width: 14, height: 14, borderRadius: 4, border: "2px solid #cbd5e1", flexShrink: 0 },
  
  specificDetailsSection: { background: "#f8fafc", borderRadius: 14, padding: 14, marginBottom: 4 },
  specificDetailsTitle: { fontWeight: 700, fontSize: 14, marginBottom: 3 },
  specificDetailsSub: { fontSize: 11, color: "#64748b", marginBottom: 12 },
  detailButtons: { display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 12 },
  detailBtn: { padding: "5px 12px", borderRadius: 40, border: "1px solid #e2e8f0", background: "white", cursor: "pointer", fontSize: 11, fontWeight: 500 },
  detailBtnActive: { padding: "5px 12px", borderRadius: 40, border: "1px solid #2563eb", background: "#eff6ff", color: "#2563eb", cursor: "pointer", fontSize: 11, fontWeight: 600 },
  detailContent: { background: "white", borderRadius: 12, padding: 14, border: "1px solid #e2e8f0" },
  detailContentTitle: { fontWeight: 700, marginBottom: 10, fontSize: 12 },
  detailContentItem: { padding: "5px 0", fontSize: 12, color: "#475569", borderBottom: "1px solid #f1f5f9" },
  
  extraNoteCard: { background: "#fef3c7", borderRadius: 14, padding: 14, marginBottom: 4 },
  extraNoteTitle: { fontWeight: 700, fontSize: 12, marginBottom: 10, color: "#92400e" },
  extraNoteContent: { fontSize: 11, color: "#78350f", lineHeight: 1.6 },
  
  additionalDetailsCard: { background: "#f3e8ff", borderRadius: 14, padding: 14, marginBottom: 4 },
  additionalDetailsTitle: { fontWeight: 700, fontSize: 12, marginBottom: 10, color: "#6b21a5" },
  additionalDetailsContent: { fontSize: 11, color: "#4c1d95", lineHeight: 1.6 },
  
  safetyCard: { background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 14, padding: 12, fontSize: 11, color: "#166534" },
  
  newAnalysisBtn: {
    width: "100%",
    marginTop: 16,
    padding: 10,
    borderRadius: 40,
    border: "1px solid #2563eb",
    background: "white",
    color: "#2563eb",
    fontWeight: 600,
    fontSize: 13,
    cursor: "pointer",
    transition: "all 0.2s"
  },
  
  heroSkeleton: { height: 140, borderRadius: 16, background: "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)", backgroundSize: "200% 100%", marginBottom: 12 },
  skeletonCard: { height: 160, borderRadius: 14, background: "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)", backgroundSize: "200% 100%" }
};