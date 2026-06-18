import { useState, useEffect, useRef } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default function Dashboard({ onBack }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("text");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");
  const [activeAccordion, setActiveAccordion] = useState("whatToDo");
  const [showAbout, setShowAbout] = useState(false);
  const [copied, setCopied] = useState(false);
  const [loadingStep, setLoadingStep] = useState("");
  const [outputLanguage, setOutputLanguage] = useState("en");
  const [sessionLetterCount, setSessionLetterCount] = useState(0);
  const [chatMessages, setChatMessages] = useState([
    { role: "assistant", content: "Hey! I've read your letter. Ask me anything — I'll keep it simple. 👋" }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState("");
  const [replyOptions, setReplyOptions] = useState(null);
  const [replyIntent, setReplyIntent] = useState(null);

  const typewriterRef = useRef(null);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const suggestions = [
    "Help me draft a reply",
    "What should I do first?",
    "Is this urgent?",
    "Explain in simpler words"
  ];

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, streamingMessage]);

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
    if (f && (f.type === "application/pdf" || f.type.startsWith("image/"))) {
      setFile(f);
    } else {
      alert("Please select a valid PDF or image file");
    }
  };

  const handleDropZoneClick = () => fileInputRef.current?.click();
  const handleDragOver = (e) => { e.preventDefault(); e.stopPropagation(); };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const f = e.dataTransfer.files[0];
    if (f && (f.type === "application/pdf" || f.type.startsWith("image/"))) {
      setFile(f);
    } else {
      alert("Please drop a valid PDF or image file");
    }
  };

  const copyToClipboard = () => {
    if (!result) return;
    
    const textToCopy = `
═══════════════════════════════════════════════════════════
           GERMAN LETTER ASSISTANT - ANALYSIS
═══════════════════════════════════════════════════════════

📌 BOTTOM LINE
───────────────────────────────────────────────────────────
${result.tldr || "No summary available"}

📋 LETTER INFORMATION
───────────────────────────────────────────────────────────
Sender:      ${result.sender || "Unknown"}
Topic:       ${result.letter_topic || "Official letter"}
Urgency:     ${result.urgency_level || "Medium"}
Quality:     ${result.confidence_level || "Medium"}

✅ WHAT TO DO
───────────────────────────────────────────────────────────
${(result.required_actions || []).map((action, i) => `${i+1}. ${action}`).join('\n') || "None"}

⏰ DEADLINES
───────────────────────────────────────────────────────────
${(result.deadlines || []).map(d => `• ${d}`).join('\n') || "None"}

💳 PAYMENT INFORMATION
───────────────────────────────────────────────────────────
${(result.payment_information || []).map(p => `• ${p}`).join('\n') || "None"}

📄 DOCUMENTS NEEDED
───────────────────────────────────────────────────────────
${(result.required_documents || []).map(d => `• ${d}`).join('\n') || "None"}

⚠️ POSSIBLE CONSEQUENCES
───────────────────────────────────────────────────────────
${(result.possible_consequences || []).map(c => `• ${c}`).join('\n') || "None"}

🛡️ THINGS TO BE CAREFUL ABOUT
───────────────────────────────────────────────────────────
${(result.unclear_or_risky_parts || []).map(r => `• ${r}`).join('\n') || "None"}

📌 ADDITIONAL DETAILS
───────────────────────────────────────────────────────────
${(result.useful_details || []).map(u => `• ${u}`).join('\n') || "None"}

═══════════════════════════════════════════════════════════
⚠️ This is AI-generated help, not legal advice.
   Please verify important information with the original letter.
═══════════════════════════════════════════════════════════
    `.trim();
    
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const exportToPDF = async () => {
    if (!result) return;
    
    const pdfContainer = document.createElement('div');
    pdfContainer.style.padding = '20px';
    pdfContainer.style.background = 'white';
    pdfContainer.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    pdfContainer.style.width = '800px';
    pdfContainer.style.color = '#111827';
    
    pdfContainer.innerHTML = `
      <div style="text-align: center; margin-bottom: 20px; border-bottom: 2px solid #7c3aed; padding-bottom: 10px;">
        <h1 style="color: #7c3aed;">German Letter Assistant</h1>
        <p style="color: #6b7280;">Analysis Report - ${new Date().toLocaleString()}</p>
      </div>
      
      <div style="background: #fefce8; border: 1px solid #fef08a; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="color: #ca8a04; margin: 0 0 8px 0;">✨ Bottom line</h3>
        <p style="font-size: 16px; font-weight: 600; margin: 0;">"${result.tldr || "No summary available"}"</p>
      </div>
      
      <div style="margin-bottom: 16px;">
        <p><strong>📧 Sender:</strong> ${result.sender || "Unknown"}</p>
        <p><strong>🏷️ Topic:</strong> ${result.letter_topic || "Official letter"}</p>
        <p><strong>⚠️ Urgency:</strong> ${result.urgency_level || "Medium"}</p>
        <p><strong>📊 Analysis Quality:</strong> ${result.confidence_level || "Medium"}</p>
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">✅ What to do</h3>
        ${(result.required_actions || []).map((action, i) => `<p style="margin: 8px 0;">${i+1}. ${action}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">⏰ Deadlines</h3>
        ${(result.deadlines || []).map(d => `<p style="margin: 8px 0;">• ${d}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">💳 Payment information</h3>
        ${(result.payment_information || []).map(p => `<p style="margin: 8px 0;">• ${p}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">📄 Documents needed</h3>
        ${(result.required_documents || []).map(d => `<p style="margin: 8px 0;">• ${d}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">⚠️ Possible consequences</h3>
        ${(result.possible_consequences || []).map(c => `<p style="margin: 8px 0;">• ${c}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">🛡️ Things to be careful about</h3>
        ${(result.unclear_or_risky_parts || []).map(r => `<p style="margin: 8px 0;">• ${r}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f3e8ff; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">📌 Additional details</h3>
        ${(result.useful_details || []).map(u => `<p style="margin: 8px 0;">• ${u}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f0fdf4; border-radius: 12px; padding: 12px; margin-top: 16px; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #166534;">⚠️ This is AI-generated help, not legal advice. Please verify important information with the original letter.</p>
      </div>
      
      <div style="text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #e5e7eb; font-size: 10px; color: #9ca3af;">
        Generated by German Letter Assistant
      </div>
    `;
    
    document.body.appendChild(pdfContainer);
    
    const canvas = await html2canvas(pdfContainer, {
      scale: 2,
      backgroundColor: 'white'
    });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const imgWidth = 190;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
    pdf.save("letter-analysis.pdf");
    
    document.body.removeChild(pdfContainer);
  };

  const analyzeLetter = async () => {
    if (mode === "text" && !text.trim()) return alert("Please paste your letter text");
    if (mode === "pdf" && !file) return alert("Please upload a PDF or image file");

    setLoading(true);
    setResult(null);
    setAnimatedSummary("");
    setChatMessages([{ role: "assistant", content: "Hey! I've read your letter. Ask me anything — I'll keep it simple. 👋" }]);

    try {
      let response;
      if (mode === "text") {
        response = await fetch("http://localhost:8000/analyze-text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ letter_text: text, language: outputLanguage }),
        });
      } else {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("language", outputLanguage);
        response = await fetch("http://localhost:8000/analyze-pdf", {
          method: "POST",
          body: formData,
        });
      }

      if (!response.ok) throw new Error("Backend error");
      const data = await response.json();
      console.log("📥 Analysis response:", data);
      
      // ✅ Store complete result with ALL required fields for chat
      setResult({
        is_valid_letter: data.is_valid_letter !== undefined ? data.is_valid_letter : true,
        letter_text: data.letter_text || text || "",
        confidence_level: data.confidence_level || "medium",
        confidence_reason: data.confidence_reason || "Analysis completed based on the letter content.",
        letter_involves_payment: data.letter_involves_payment || false,
        sender: data.sender || "Unknown sender",
        sender_type: data.sender_type || "Other",
        urgency_level: data.urgency_level || "Medium",
        urgency_reason: data.urgency_reason || "Action required based on the letter content.",
        letter_topic: data.letter_topic || "Official letter",
        tldr: data.tldr || data.summary || "",
        useful_details: data.useful_details || [],
        deadlines: data.deadlines || [],
        required_actions: data.required_actions || [],
        required_documents: data.required_documents || [],
        payment_information: data.payment_information || [],
        possible_consequences: data.possible_consequences || [],
        unclear_or_risky_parts: data.unclear_or_risky_parts || [],
        safety_note: data.safety_note || "This is AI-generated help, not legal advice. Please verify important decisions with the responsible office or a qualified advisor.",
      });
      
      setSessionLetterCount(prev => prev + 1);
      startTypewriter(data.tldr || data.summary || "No summary available");
    } catch (err) {
      console.error(err);
      alert("Backend connection failed. Make sure the server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  // ========== FIXED CHAT - COMPLETE ANALYSIS OBJECT ==========
  const sendChatMessage = async () => {
    if (!chatInput.trim() || isStreaming) return;
    
    const userMessage = chatInput;
    setChatInput("");
    
    const messagesHistory = chatMessages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
    messagesHistory.push({ role: "user", content: userMessage });
    
    setChatMessages(prev => [...prev, { role: "user", content: userMessage }]);
    
    setIsStreaming(true);
    setStreamingMessage("");
    
    try {
      // ✅ COMPLETE analysis object with ALL required fields
      const analysisData = {
        is_valid_letter: result?.is_valid_letter !== undefined ? result.is_valid_letter : true,
        letter_text: result?.letter_text || text || "",
        confidence_level: result?.confidence_level || "medium",
        confidence_reason: result?.confidence_reason || "Analysis completed based on the letter content.",
        letter_involves_payment: result?.letter_involves_payment || false,
        sender: result?.sender || "Unknown sender",
        sender_type: result?.sender_type || "Other",
        urgency_level: result?.urgency_level || "Medium",
        urgency_reason: result?.urgency_reason || "Action required based on the letter content.",
        letter_topic: result?.letter_topic || "Official letter",
        tldr: result?.tldr || "",
        useful_details: result?.useful_details || [],
        deadlines: result?.deadlines || [],
        required_actions: result?.required_actions || [],
        required_documents: result?.required_documents || [],
        payment_information: result?.payment_information || [],
        possible_consequences: result?.possible_consequences || [],
        unclear_or_risky_parts: result?.unclear_or_risky_parts || [],
        safety_note: result?.safety_note || "This is AI-generated help, not legal advice. Please verify important decisions with the responsible office or a qualified advisor.",
      };

      const requestBody = {
        letter_text: result?.letter_text || text || "",
        analysis: analysisData,
        messages: messagesHistory,
        reply_intent: replyIntent || null,
      };

      console.log("📤 Sending to chat:", JSON.stringify(requestBody, null, 2));

      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        let errorMessage = "";
        try {
          const errorData = await response.json();
          console.error("❌ Backend error details:", errorData);
          
          if (errorData.detail) {
            if (Array.isArray(errorData.detail)) {
              errorMessage = errorData.detail.map(err => {
                const field = err.loc?.join('.') || 'unknown';
                return `${field}: ${err.msg || 'invalid'}`;
              }).join('; ');
            } else {
              errorMessage = errorData.detail;
            }
          } else {
            errorMessage = JSON.stringify(errorData);
          }
        } catch (e) {
          errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      console.log("✅ Chat response:", data);
      
      setIsStreaming(false);
      setReplyIntent(null);
      setReplyOptions(null);
      
      if (data.ui_action === "show_reply_options") {
        setReplyOptions(data.options);
        setChatMessages(prev => [...prev, { 
          role: "assistant", 
          content: data.reply || "How would you like me to write the reply?",
          isOptions: true,
          options: data.options
        }]);
      } else if (data.reply) {
        setChatMessages(prev => [...prev, { role: "assistant", content: data.reply }]);
      } else {
        setChatMessages(prev => [...prev, { role: "assistant", content: "I couldn't generate a response. Please try again." }]);
      }
      
    } catch (err) {
      console.error("❌ Chat error:", err);
      setIsStreaming(false);
      
      let errorMsg = err.message || "Unknown error";
      if (errorMsg.length > 150) {
        errorMsg = errorMsg.substring(0, 150) + "...";
      }
      
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        content: `⚠️ ${errorMsg}` 
      }]);
    } finally {
      setIsStreaming(false);
      setStreamingMessage("");
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setChatInput(suggestion);
    setTimeout(() => sendChatMessage(), 100);
  };

  const handleReplyOptionClick = (option) => {
    setReplyIntent(option);
    setChatInput(option);
    setTimeout(() => sendChatMessage(), 100);
  };

  const resetAnalysis = () => {
    if (typewriterRef.current) clearInterval(typewriterRef.current);
    setResult(null);
    setAnimatedSummary("");
    setText("");
    setFile(null);
    setChatMessages([{ role: "assistant", content: "Hey! I've read your letter. Ask me anything — I'll keep it simple. 👋" }]);
    setSessionLetterCount(0);
    setReplyOptions(null);
    setReplyIntent(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const toggleAccordion = (id) => {
    setActiveAccordion(activeAccordion === id ? null : id);
  };

  const getConfidenceDisplay = () => {
    const level = result?.confidence_level || "medium";
    const labels = {
      high: { label: "High", color: "#065f46", bg: "#ecfdf5", border: "#a7f3d0" },
      medium: { label: "Medium", color: "#92400e", bg: "#fffbeb", border: "#fcd34d" },
      low: { label: "Low", color: "#991b1b", bg: "#fef2f2", border: "#fca5a5" }
    };
    return labels[level.toLowerCase()] || labels.medium;
  };

  const confidenceInfo = getConfidenceDisplay();

  const daysLeft = (() => {
    if (!result?.deadlines?.[0]) return null;
    const match = result.deadlines[0].match(/(\d{2})\.(\d{2})\.(\d{4})/);
    if (!match) return null;
    const deadline = new Date(match[3], match[2] - 1, match[1]);
    const diff = Math.ceil((deadline - new Date()) / (1000 * 60 * 60 * 24));
    return diff > 0 ? diff : 0;
  })();

  const accordionSections = [
    { id: "whatToDo", icon: "✅", title: "What to do", items: result?.required_actions || [] },
    { id: "howToPay", icon: "💳", title: "How to pay", items: result?.payment_information || [] },
    { id: "documents", icon: "📄", title: "Documents you may need", items: result?.required_documents || [] },
    { id: "consequences", icon: "⚠️", title: "What happens if you ignore this", items: result?.possible_consequences || [] },
    { id: "careful", icon: "🛡️", title: "Things to be careful about", items: result?.unclear_or_risky_parts || [] }
  ];

  return (
    <div style={styles.page}>
      {/* Top Bar */}
      <div style={styles.topbar}>
        <div style={styles.brand}>
          <div style={styles.brandIcon}>📄</div>
          <div style={styles.brandName}>German <span style={{ color: "#7c3aed" }}>Letter Assistant</span></div>
        </div>
        <div style={styles.topRight}>
          <select 
            value={outputLanguage} 
            onChange={(e) => setOutputLanguage(e.target.value)} 
            style={styles.langSel}
          >
            <option value="en">🇬🇧 English</option>
            <option value="de">🇩🇪 Deutsch</option>
            <option value="tr">🇹🇷 Türkçe</option>
            <option value="ar">🇸🇦 العربية</option>
            <option value="fr">🇫🇷 Français</option>
            <option value="es">🇪🇸 Español</option>
            <option value="it">🇮🇹 Italiano</option>
            <option value="pt">🇵🇹 Português</option>
            <option value="nl">🇳🇱 Nederlands</option>
            <option value="pl">🇵🇱 Polski</option>
            <option value="ru">🇷🇺 Русский</option>
            <option value="ja">🇯🇵 日本語</option>
            <option value="ko">🇰🇷 한국어</option>
            <option value="zh">🇨🇳 中文</option>
            <option value="hi">🇮🇳 हिन्दी</option>
          </select>
          <button style={styles.backBtn} onClick={onBack}>← Back</button>
          <button style={styles.aboutBtn} onClick={() => setShowAbout(true)}>About</button>
        </div>
      </div>

      {/* Main Grid */}
      <div style={styles.main}>
        {/* Left Panel - Sidebar */}
        <div style={styles.leftPanel}>
          <div style={styles.sidebarSection}>
            <div style={styles.stepBadge}>1</div>
            <div style={styles.sidebarTitle}>Your letter</div>
          </div>
          
          <div style={styles.modeToggle}>
            <button onClick={() => setMode("text")} style={mode === "text" ? {...styles.modeBtn, ...styles.modeBtnActive} : styles.modeBtn}>
              📄 Paste Text
            </button>
            <button onClick={() => setMode("pdf")} style={mode === "pdf" ? {...styles.modeBtn, ...styles.modeBtnActive} : styles.modeBtn}>
              📑 Upload PDF / Image
            </button>
          </div>

          {mode === "text" ? (
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste your official German letter here..."
              style={styles.textarea}
              rows={10}
            />
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
                accept=".pdf,image/*" 
                style={{ display: "none" }} 
                onChange={handleFileSelect} 
              />
              <div style={styles.dropIcon}>📄</div>
              <div style={styles.dropText}>Click to upload PDF or image</div>
              <div style={styles.dropSubtext}>or drag and drop</div>
              {file && <div style={styles.fileName}>✓ {file.name}</div>}
            </div>
          )}

          <button style={styles.analyzeBtn} onClick={analyzeLetter} disabled={loading}>
            {loading ? "⏳ Analyzing..." : "✨ Analyze Letter"}
          </button>

          {loading && (
            <div style={styles.loadingCard}>
              <div style={styles.loadingDot}></div>
              <div style={styles.loadingText}>Processing your letter...</div>
            </div>
          )}

          <div style={styles.privacyNote}>
            <span>🔒</span>
            <span>Your data is private — nothing is stored</span>
          </div>

          <div style={styles.sessionNote}>
            {sessionLetterCount} letter{sessionLetterCount !== 1 ? 's' : ''} analyzed
          </div>
        </div>

        {/* Right Panel - Results */}
        <div style={styles.rightPanel}>
          <div style={styles.resultsArea}>
            <div style={styles.stepBadgeRow}>
              <div style={styles.stepBadge}>2</div>
              <div style={styles.stepBadgeLabel}>Analysis Result</div>
            </div>

            {!result && !loading && (
              <div style={styles.emptyState}>
                <div style={styles.emptyIcon}>📄</div>
                <div style={styles.emptyTitle}>No letter analyzed yet</div>
                <div style={styles.emptySub}>Paste or upload a letter to see analysis</div>
              </div>
            )}

            {loading && !result && (
              <div>
                <div style={styles.skeletonCard}></div>
                <div style={styles.skeletonCard}></div>
              </div>
            )}

            {result && (
              <>
                {/* Bottom Line */}
                <div style={styles.bottomLineCard}>
                  <div style={styles.blLabel}>✨ Bottom line</div>
                  <div style={styles.blText}>"{animatedSummary || result.tldr}"</div>
                </div>

                {/* Meta Row */}
                <div style={styles.metaRow}>
                  <span style={styles.metaItem}>📧 {result.sender || "Unknown sender"}</span>
                  <span style={styles.metaItem}>🏷️ {result.letter_topic || "Official letter"}</span>
                  <span style={styles.urgencyBadge}>● {result.urgency_level || "Medium"} urgency</span>
                  {result.letter_involves_payment && (
                    <span style={styles.paymentBadge}>💳 Payment involved</span>
                  )}
                  {result.is_valid_letter === false && (
                    <span style={styles.warningBadge}>⚠️ May not be official</span>
                  )}
                </div>

                {/* Deadline Bar */}
                {daysLeft && (
                  <div style={styles.deadlineBar}>
                    ⏰ {daysLeft} days left to act
                  </div>
                )}

                {/* Analysis Quality */}
                <div style={{ ...styles.qualityBar, background: confidenceInfo.bg, border: `1px solid ${confidenceInfo.border}` }}>
                  <div style={{ ...styles.qualityTitle, color: confidenceInfo.color }}>
                    ✓ Analysis Quality: {confidenceInfo.label}
                  </div>
                  <div style={styles.qualityText}>
                    {result.confidence_reason || "Analysis completed based on the letter content."}
                  </div>
                </div>

                {/* Accordions */}
                <div style={styles.accordionWrap}>
                  {accordionSections.map(section => (
                    section.items && section.items.length > 0 && (
                      <details 
                        key={section.id} 
                        style={styles.accordion}
                        open={activeAccordion === section.id}
                        onClick={() => toggleAccordion(section.id)}
                      >
                        <summary style={styles.accordionSummary}>
                          {section.icon} {section.title}
                        </summary>
                        <div style={styles.accordionBody}>
                          {section.items.map((item, i) => (
                            <div key={i} style={styles.accordionItem}>▶ {item}</div>
                          ))}
                        </div>
                      </details>
                    )
                  ))}
                </div>

                {/* Additional Details */}
                {result.useful_details && result.useful_details.length > 0 && (
                  <div style={styles.additionalDetails}>
                    <div style={styles.additionalTitle}>📌 Additional details</div>
                    {(result.useful_details || []).map((detail, i) => (
                      <div key={i} style={styles.additionalItem}>• {detail}</div>
                    ))}
                  </div>
                )}

                <div style={styles.safetyNote}>
                  🛡️ {result.safety_note || "This is AI-generated help, not legal advice."}
                </div>

                {/* Action Buttons */}
                <div style={styles.actionRow}>
                  <button style={styles.actionBtn} onClick={copyToClipboard}>📋 {copied ? "Copied!" : "Copy"}</button>
                  <button style={styles.actionBtn} onClick={exportToPDF}>📄 PDF</button>
                  <button style={styles.actionBtn} onClick={resetAnalysis}>🔄 New</button>
                </div>

                {/* Chat Section */}
                <div style={styles.chatSection}>
                  <div style={styles.chatHeader}>
                    <div style={styles.onlineDot}></div>
                    <div>
                      <div style={styles.chatTitle}>💬 Chat with Assistant</div>
                      <div style={styles.chatSub}>Ask anything about this letter</div>
                    </div>
                  </div>

                  <div style={styles.chatMessages}>
                    {chatMessages.map((msg, idx) => (
                      <div key={idx} style={{ ...styles.msg, justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
                        <div style={{ ...styles.bubble, ...(msg.role === "user" ? styles.userBubble : styles.assistantBubble) }}>
                          {msg.content}
                          {msg.isOptions && (
                            <div style={styles.optionButtons}>
                              {msg.options?.map(opt => (
                                <button key={opt} style={styles.optionBtn} onClick={() => handleReplyOptionClick(opt)}>
                                  {opt}
                                </button>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                    {isStreaming && streamingMessage && (
                      <div style={{ ...styles.msg, justifyContent: "flex-start" }}>
                        <div style={{ ...styles.bubble, ...styles.assistantBubble }}>{streamingMessage}<span style={styles.cursor}>|</span></div>
                      </div>
                    )}
                    <div ref={chatEndRef} />
                  </div>

                  <div style={styles.suggestions}>
                    {suggestions.map((sug, i) => (
                      <div key={i} style={styles.sug} onClick={() => handleSuggestionClick(sug)}>{sug}</div>
                    ))}
                  </div>

                  <div style={styles.chatInputRow}>
                    <input 
                      type="text" 
                      value={chatInput} 
                      onChange={(e) => setChatInput(e.target.value)} 
                      onKeyPress={(e) => e.key === "Enter" && sendChatMessage()} 
                      placeholder="Ask anything about this letter..." 
                      style={styles.chatInput} 
                      disabled={isStreaming}
                    />
                    <button style={styles.sendBtn} onClick={sendChatMessage} disabled={isStreaming}>➤</button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* About Modal */}
      {showAbout && (
        <div style={styles.modalOverlay} onClick={() => setShowAbout(false)}>
          <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <h3>ℹ️ German Letter Assistant</h3>
            <p><strong>Version:</strong> 2.0</p>
            <p><strong>Features:</strong> OCR, Smart Chat with Streaming, Reply Draft Assistant, Multi-language Output</p>
            <p><strong>Privacy:</strong> Your documents are processed temporarily and not stored.</p>
            <p><strong>Disclaimer:</strong> This is AI‑generated help, not legal advice.</p>
            <button style={styles.modalClose} onClick={() => setShowAbout(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

// ========== STYLES - PURPLE THEME (Matching Landing Page) ==========
const styles = {
  page: {
    background: "#f3f6fb",
    minHeight: "100vh",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    color: "#111827",
  },
  topbar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "12px 24px",
    background: "white",
    borderBottom: "1px solid #e5e7eb",
  },
  brand: { display: "flex", alignItems: "center", gap: "10px" },
  brandIcon: { fontSize: "24px" },
  brandName: { fontSize: "16px", fontWeight: 600, color: "#1e1b4b" },
  topRight: { display: "flex", alignItems: "center", gap: "12px" },
  langSel: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    padding: "5px 12px",
    fontSize: "12px",
    cursor: "pointer",
    color: "#374151",
  },
  backBtn: {
    border: "1px solid #e5e7eb",
    background: "white",
    padding: "5px 12px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "12px",
    color: "#374151",
  },
  aboutBtn: {
    border: "1px solid #e5e7eb",
    background: "white",
    padding: "5px 12px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "12px",
    color: "#374151",
  },
  main: {
    display: "grid",
    gridTemplateColumns: "320px 1fr",
    minHeight: "calc(100vh - 55px)",
  },
  leftPanel: {
    padding: "24px",
    borderRight: "1px solid #e5e7eb",
    background: "#fafcff",
  },
  rightPanel: {
    background: "#f3f6fb",
    display: "flex",
    flexDirection: "column",
  },
  sidebarSection: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    marginBottom: "16px",
  },
  sidebarTitle: {
    fontSize: "14px",
    fontWeight: 600,
    color: "#1e1b4b",
  },
  stepBadge: {
    width: "24px",
    height: "24px",
    borderRadius: "50%",
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "white",
    fontSize: "11px",
    fontWeight: 700,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  stepBadgeRow: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    marginBottom: "16px",
  },
  stepBadgeLabel: {
    fontSize: "14px",
    fontWeight: 600,
    color: "#1e1b4b",
  },
  modeToggle: {
    display: "flex",
    gap: "8px",
    marginBottom: "12px",
  },
  modeBtn: {
    flex: 1,
    padding: "8px",
    borderRadius: "40px",
    fontSize: "12px",
    fontWeight: 500,
    cursor: "pointer",
    border: "1px solid #e5e7eb",
    background: "white",
    color: "#6b7280",
  },
  modeBtnActive: {
    background: "#ede9fe",
    border: "1px solid #7c3aed",
    color: "#7c3aed",
  },
  textarea: {
    width: "100%",
    minHeight: "180px",
    border: "1px solid #e5e7eb",
    borderRadius: "12px",
    padding: "12px",
    fontSize: "13px",
    outline: "none",
    background: "white",
    fontFamily: "monospace",
    resize: "vertical",
    color: "#111827",
  },
  dropZone: {
    border: "2px dashed #c7d2fe",
    borderRadius: "12px",
    padding: "32px",
    textAlign: "center",
    background: "#f8fbff",
    cursor: "pointer",
    minHeight: "180px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "6px",
  },
  dropIcon: { fontSize: "32px" },
  dropText: { fontSize: "13px", color: "#4b5563" },
  dropSubtext: { fontSize: "11px", color: "#9ca3af" },
  fileName: { marginTop: "6px", color: "#7c3aed", fontSize: "12px", fontWeight: 500 },
  analyzeBtn: {
    width: "100%",
    marginTop: "12px",
    padding: "12px",
    borderRadius: "40px",
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "white",
    border: "none",
    fontSize: "14px",
    fontWeight: 600,
    cursor: "pointer",
    boxShadow: "0 10px 20px rgba(124,58,237,0.25)",
  },
  loadingCard: {
    marginTop: "12px",
    padding: "12px",
    background: "#f8fafc",
    borderRadius: "12px",
    textAlign: "center",
    border: "1px solid #e5e7eb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "10px",
  },
  loadingDot: {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    background: "#7c3aed",
    animation: "pulse 1s infinite",
  },
  loadingText: { fontSize: "13px", color: "#7c3aed", fontWeight: 500 },
  privacyNote: {
    marginTop: "12px",
    padding: "10px",
    fontSize: "11px",
    color: "#6b7280",
    display: "flex",
    alignItems: "center",
    gap: "6px",
    background: "#f8fafc",
    borderRadius: "8px",
    border: "1px solid #e5e7eb",
  },
  sessionNote: {
    fontSize: "11px",
    color: "#9ca3af",
    textAlign: "center",
    marginTop: "8px",
  },
  resultsArea: {
    flex: 1,
    padding: "24px",
    display: "flex",
    flexDirection: "column",
    gap: "14px",
    overflowY: "auto",
    maxHeight: "calc(100vh - 55px)",
  },
  emptyState: {
    textAlign: "center",
    padding: "60px 20px",
    color: "#9ca3af",
  },
  emptyIcon: { fontSize: "48px", marginBottom: "12px" },
  emptyTitle: { fontSize: "16px", color: "#6b7280", marginBottom: "4px" },
  emptySub: { fontSize: "13px", color: "#9ca3af" },
  bottomLineCard: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "14px",
    padding: "20px",
    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
  },
  blLabel: {
    fontSize: "11px",
    color: "#7c3aed",
    fontWeight: 700,
    letterSpacing: "1.2px",
    textTransform: "uppercase",
    marginBottom: "6px",
  },
  blText: {
    fontSize: "16px",
    fontWeight: 600,
    lineHeight: 1.5,
    color: "#1e1b4b",
  },
  metaRow: {
    display: "flex",
    gap: "16px",
    flexWrap: "wrap",
    fontSize: "13px",
    color: "#6b7280",
    alignItems: "center",
    padding: "8px 0",
  },
  metaItem: { display: "flex", alignItems: "center", gap: "4px" },
  urgencyBadge: {
    display: "inline-flex",
    alignItems: "center",
    gap: "6px",
    color: "#f87171",
    fontWeight: 600,
  },
  paymentBadge: {
    display: "inline-flex",
    alignItems: "center",
    gap: "4px",
    color: "#7c3aed",
    fontWeight: 600,
    background: "#ede9fe",
    padding: "2px 8px",
    borderRadius: "20px",
  },
  warningBadge: {
    display: "inline-flex",
    alignItems: "center",
    gap: "4px",
    color: "#dc2626",
    fontWeight: 600,
    background: "#fee2e2",
    padding: "2px 8px",
    borderRadius: "20px",
  },
  deadlineBar: {
    background: "#fef2f2",
    border: "1px solid #fca5a5",
    borderRadius: "10px",
    padding: "12px 16px",
    color: "#dc2626",
    fontWeight: 600,
    fontSize: "14px",
  },
  qualityBar: {
    borderRadius: "10px",
    padding: "14px 16px",
  },
  qualityTitle: {
    fontSize: "14px",
    fontWeight: 600,
    marginBottom: "4px",
  },
  qualityText: {
    fontSize: "12px",
    color: "#6b7280",
  },
  accordionWrap: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },
  accordion: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "10px",
    padding: "4px 0",
  },
  accordionSummary: {
    padding: "12px 16px",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: "13px",
    color: "#4c1d95",
    listStyle: "none",
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  accordionBody: {
    padding: "0 16px 12px 16px",
    borderTop: "1px solid #f1f5f9",
  },
  accordionItem: {
    padding: "6px 0",
    fontSize: "13px",
    color: "#4b5563",
    borderBottom: "1px solid #f1f5f9",
  },
  additionalDetails: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "10px",
    padding: "14px 16px",
  },
  additionalTitle: {
    fontWeight: 600,
    fontSize: "13px",
    color: "#4c1d95",
    marginBottom: "8px",
  },
  additionalItem: {
    fontSize: "12px",
    color: "#6b7280",
    padding: "3px 0",
  },
  safetyNote: {
    background: "#f0fdf4",
    border: "1px solid #bbf7d0",
    borderRadius: "10px",
    padding: "10px 14px",
    fontSize: "12px",
    color: "#166534",
  },
  actionRow: {
    display: "flex",
    gap: "8px",
    marginTop: "4px",
  },
  actionBtn: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    padding: "6px 14px",
    fontSize: "12px",
    cursor: "pointer",
    color: "#374151",
  },
  chatSection: {
    marginTop: "16px",
    borderTop: "1px solid #e5e7eb",
    paddingTop: "12px",
  },
  chatHeader: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    marginBottom: "10px",
  },
  onlineDot: {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    background: "#22c55e",
  },
  chatTitle: { fontSize: "13px", fontWeight: 600, color: "#1e1b4b" },
  chatSub: { fontSize: "11px", color: "#9ca3af" },
  chatMessages: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    maxHeight: "200px",
    overflowY: "auto",
    padding: "4px 0",
  },
  msg: { display: "flex" },
  bubble: {
    padding: "8px 14px",
    borderRadius: "14px",
    fontSize: "13px",
    lineHeight: 1.5,
    maxWidth: "70%",
  },
  userBubble: {
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "white",
    borderBottomRightRadius: "4px",
  },
  assistantBubble: {
    background: "#f1f5f9",
    color: "#1e1b4b",
    borderBottomLeftRadius: "4px",
  },
  cursor: {
    display: "inline-block",
    width: "2px",
    height: "14px",
    background: "#7c3aed",
    marginLeft: "2px",
    animation: "blink 1s infinite",
  },
  suggestions: {
    display: "flex",
    gap: "6px",
    flexWrap: "wrap",
    padding: "8px 0",
  },
  sug: {
    padding: "4px 12px",
    borderRadius: "20px",
    border: "1px solid #e5e7eb",
    fontSize: "12px",
    cursor: "pointer",
    background: "white",
    color: "#374151",
  },
  chatInputRow: {
    display: "flex",
    gap: "8px",
    alignItems: "center",
    paddingTop: "8px",
  },
  chatInput: {
    flex: 1,
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "24px",
    padding: "10px 16px",
    fontSize: "13px",
    outline: "none",
    color: "#111827",
  },
  sendBtn: {
    width: "38px",
    height: "38px",
    borderRadius: "50%",
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    border: "none",
    color: "white",
    cursor: "pointer",
    fontSize: "16px",
  },
  optionButtons: {
    display: "flex",
    gap: "6px",
    marginTop: "8px",
    flexWrap: "wrap",
  },
  optionBtn: {
    padding: "4px 12px",
    borderRadius: "20px",
    border: "1px solid #7c3aed",
    background: "#ede9fe",
    color: "#7c3aed",
    fontSize: "11px",
    cursor: "pointer",
  },
  skeletonCard: {
    height: "80px",
    borderRadius: "12px",
    background: "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)",
    backgroundSize: "200% 100%",
    marginBottom: "10px",
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0,0,0,0.5)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000,
  },
  modalContent: {
    background: "white",
    padding: "24px",
    borderRadius: "24px",
    maxWidth: "450px",
    width: "90%",
  },
  modalClose: {
    marginTop: "16px",
    padding: "8px 16px",
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "white",
    border: "none",
    borderRadius: "40px",
    cursor: "pointer",
  },
};

// Add animations
const styleSheet = document.createElement("style");
styleSheet.textContent = `
  @keyframes pulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
`;
document.head.appendChild(styleSheet);