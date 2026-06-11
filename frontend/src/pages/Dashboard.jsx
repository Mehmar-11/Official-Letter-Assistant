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
  const [showPreview, setShowPreview] = useState(false);
  const [sessionLetterCount, setSessionLetterCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState(""); // ← NEW: Search state
  const [analyzedLetters, setAnalyzedLetters] = useState([]); // ← NEW: Store analyzed letters
  const [chatMessages, setChatMessages] = useState([
    { role: "assistant", content: "Hey! I've read your letter. Ask me anything — I'll keep it simple. 👋" }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState("");
  
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

  const steps = ["📄 Extracting text...", "🤖 AI analyzing...", "📊 Processing data...", "✨ Generating summary..."];

  useEffect(() => {
    let interval, stepIndex = 0;
    if (loading) {
      setLoadingStep(steps[0]);
      interval = setInterval(() => {
        stepIndex++;
        if (stepIndex < steps.length) setLoadingStep(steps[stepIndex]);
      }, 1200);
    }
    return () => clearInterval(interval);
  }, [loading]);

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

  // ========== SEARCH FUNCTION ==========
  const getFilteredLetters = () => {
    if (!searchQuery.trim()) return analyzedLetters;
    return analyzedLetters.filter(letter => 
      letter.sender?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      letter.letter_topic?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      letter.tldr?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      letter.required_actions?.some(a => a.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  };

  // ========== COPY FUNCTION ==========
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

✅ WHAT YOU NEED TO DO
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

  // ========== FIXED EXPORT TO PDF - Captures ALL sections ==========
  const exportToPDF = async () => {
    if (!result) return;
    
    // Create a temporary div with all content expanded for PDF
    const pdfContainer = document.createElement('div');
    pdfContainer.style.padding = '20px';
    pdfContainer.style.background = 'white';
    pdfContainer.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    pdfContainer.style.width = '800px';
    pdfContainer.style.color = '#111827';
    
    pdfContainer.innerHTML = `
      <div style="text-align: center; margin-bottom: 20px; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
        <h1 style="color: #2563eb;">German Letter Assistant</h1>
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
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">✅ What you need to do</h3>
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
    if (mode === "pdf" && !file) return alert("Please upload a PDF file");

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
      setResult(data);
      
      // Store analyzed letter for search
      setAnalyzedLetters(prev => [...prev, { 
        id: Date.now(),
        ...data,
        timestamp: new Date().toLocaleString()
      }]);
      setSessionLetterCount(prev => prev + 1);
      startTypewriter(data.tldr || data.summary || "No summary available");
    } catch (err) {
      console.error(err);
      alert("Backend connection failed. Make sure the server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim() || isStreaming) return;
    
    const userMessage = chatInput;
    setChatInput("");
    setChatMessages(prev => [...prev, { role: "user", content: userMessage }]);
    
    setIsStreaming(true);
    setStreamingMessage("");
    
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          letter_context: result,
          language: outputLanguage
        }),
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = "";
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.reply) {
                fullResponse += data.reply;
                setStreamingMessage(fullResponse);
              }
            } catch (e) {
              fullResponse += line;
              setStreamingMessage(fullResponse);
            }
          }
        }
      }
      
      setIsStreaming(false);
      setChatMessages(prev => [...prev, { role: "assistant", content: fullResponse }]);
    } catch (err) {
      console.error(err);
      setChatMessages(prev => [...prev, { role: "assistant", content: "Sorry, something went wrong. Please try again." }]);
    } finally {
      setIsStreaming(false);
      setStreamingMessage("");
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setChatInput(suggestion);
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
    setAnalyzedLetters([]);
    setSearchQuery("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const toggleAccordion = (id) => {
    setActiveAccordion(activeAccordion === id ? null : id);
  };

  const daysLeft = (() => {
    if (!result?.deadlines?.[0]) return null;
    const match = result.deadlines[0].match(/(\d{2})\.(\d{2})\.(\d{4})/);
    if (!match) return null;
    const deadline = new Date(match[3], match[2] - 1, match[1]);
    const diff = Math.ceil((deadline - new Date()) / (1000 * 60 * 60 * 24));
    return diff > 0 ? diff : 0;
  })();

  const filteredLetters = getFilteredLetters();

  return (
    <div style={styles.page}>
      {/* Top Bar */}
      <div style={styles.topbar}>
        <div style={styles.brand}>
          <div style={styles.brandIcon}>📄</div>
          <div style={styles.brandName}>German <span style={{ color: "#2563eb" }}>Letter Assistant</span></div>
        </div>
        <div style={styles.topRight}>
          <select value={outputLanguage} onChange={(e) => setOutputLanguage(e.target.value)} style={styles.langSel}>
            <option value="en">🇬🇧 English</option>
            <option value="de">🇩🇪 Deutsch</option>
            <option value="tr">🇹🇷 Türkçe</option>
            <option value="ar">🇸🇦 العربية</option>
          </select>
          <button style={styles.backBtn} onClick={onBack}>← Back</button>
          <button style={styles.aboutBtn} onClick={() => setShowAbout(true)}>About</button>
        </div>
      </div>

      {/* Main Grid */}
      <div style={styles.main}>
        {/* Left Panel */}
        <div style={styles.leftPanel}>
          <div style={styles.card}>
            <div style={styles.cardHd}>
              <div style={styles.stepBadge}>1</div>
              <div style={styles.cardTitle}>Your letter</div>
            </div>
            
            <div style={styles.modeToggle}>
              <button onClick={() => setMode("text")} style={mode === "text" ? {...styles.modeBtn, ...styles.modeBtnActive} : styles.modeBtn}>
                📄 Paste Text
              </button>
              <button onClick={() => setMode("pdf")} style={mode === "pdf" ? {...styles.modeBtn, ...styles.modeBtnActive} : styles.modeBtn}>
                📑 Upload PDF
              </button>
            </div>

            {mode === "text" ? (
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your official German letter here..."
                style={styles.fakeTextarea}
                rows={6}
              />
            ) : (
              <div style={styles.dropZone} onClick={handleDropZoneClick}>
                <input type="file" ref={fileInputRef} accept="application/pdf" style={{ display: "none" }} onChange={handleFileSelect} />
                <div style={styles.dropIcon}>📄</div>
                <div style={styles.dropText}>Click to upload PDF</div>
                <div style={styles.dropSubtext}>or drag and drop</div>
                {file && <div style={styles.fileName}>✓ {file.name}</div>}
              </div>
            )}

            <button style={styles.btnNew} onClick={analyzeLetter} disabled={loading}>
              ✨ {loading ? " Analyzing..." : " New Analysis"}
            </button>

            {loading && (
              <div style={styles.loadingCard}>
                <div style={styles.spinner}></div>
                <div style={styles.loadingStep}>{loadingStep}</div>
              </div>
            )}

            <div style={styles.previewToggle} onClick={() => setShowPreview(!showPreview)}>
              <div style={styles.previewLabel}>📄 Letter preview</div>
              <span>{showPreview ? "▲" : "▼"}</span>
            </div>
            
            {showPreview && (
              <div style={styles.previewText}>
                {mode === "text" ? (text.substring(0, 200) + (text.length > 200 ? "..." : "") || "No text pasted yet...") : (file ? file.name : "No PDF selected...")}
              </div>
            )}
          </div>

          {/* Search Section - NOW FUNCTIONAL */}
          <div style={{ ...styles.card, marginTop: 0 }}>
            <div style={{ ...styles.cardHd, marginBottom: "10px" }}>
              <span style={{ fontSize: "15px" }}>🔍</span>
              <div style={{ ...styles.cardTitle, color: "#6b7280" }}>Search your letters</div>
            </div>
            <div style={styles.searchInput}>
              <span>🔍</span>
              <input 
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by sender, topic, action..."
                style={styles.searchInputField}
              />
            </div>
            
            {/* Search Results */}
            {searchQuery && filteredLetters.length > 0 && (
              <div style={styles.searchResults}>
                {filteredLetters.map(letter => (
                  <div key={letter.id} style={styles.searchResultItem}>
                    <div style={styles.searchResultSender}>📧 {letter.sender}</div>
                    <div style={styles.searchResultTopic}>🏷️ {letter.letter_topic}</div>
                  </div>
                ))}
              </div>
            )}
            
            {searchQuery && filteredLetters.length === 0 && (
              <div style={styles.searchNoResults}>No matching letters found</div>
            )}
            
            <div style={styles.sessionNote}>
              {sessionLetterCount} letter{sessionLetterCount !== 1 ? 's' : ''} in this session
            </div>
          </div>
        </div>

        {/* Right Panel */}
        <div style={styles.rightPanel}>
          <div id="resultsArea" style={styles.resultsArea}>
            <div style={{ ...styles.cardHd, marginBottom: "8px" }}>
              <div style={styles.stepBadge}>2</div>
              <div style={styles.cardTitle}>Analysis Result</div>
            </div>

            {!result && !loading && (
              <div style={styles.emptyState}>
                <div style={{ fontSize: "48px", marginBottom: "12px" }}>📄</div>
                <div>No letter analyzed yet</div>
                <div style={{ fontSize: "11px", marginTop: "6px", color: "#9ca3af" }}>Paste or upload a letter to see analysis</div>
              </div>
            )}

            {loading && !result && (
              <div><div style={styles.skeletonCard}></div><div style={styles.skeletonCard}></div></div>
            )}

            {result && (
              <>
                {/* Bottom Line Card */}
                <div style={styles.bottomLineCard}>
                  <div style={styles.blLabel}>✨ Bottom line</div>
                  <div style={styles.blText}>"{animatedSummary || result.tldr}"</div>
                </div>

                {/* Meta Row */}
                <div style={styles.metaRow}>
                  <span>📧 {result.sender || "Unknown sender"}</span>
                  <span>🏷️ {result.letter_topic || "Official letter"}</span>
                  <span style={styles.urgencyBadge}>⚠️ {result.urgency_level || "Medium"} urgency</span>
                </div>

                {/* Deadline Badge */}
                {daysLeft && (
                  <div style={styles.deadlineBadge}>
                    ⏰ {daysLeft} days left to act
                  </div>
                )}

                {/* Reliability Card */}
                <div style={styles.reliability}>
                  <div style={styles.relTitle}>🛡️ {result.confidence_score > 80 ? "Reliable analysis" : "Analysis with caution"}</div>
                  <div style={styles.relSub}>
                    {result.confidence_score > 80 ? "Text was clear — all fields extracted successfully." :
                     result.confidence_score > 50 ? "Some information may be incomplete. Verify key details." :
                     "Low confidence — please verify all information with the original letter."}
                  </div>
                </div>

                {/* Accordions */}
                <div style={styles.accordionWrap}>
                  {[
                    { id: "whatToDo", icon: "✅", title: "What to do", items: result.required_actions },
                    { id: "payment", icon: "💳", title: "Payment details", items: result.payment_information },
                    { id: "documents", icon: "📄", title: "Documents needed", items: result.required_documents },
                    { id: "risks", icon: "⚠️", title: "Risks if ignored", items: result.possible_consequences }
                  ].map(section => (
                    <div key={section.id} style={styles.accordionItem}>
                      <div style={styles.accordionHd} onClick={() => toggleAccordion(section.id)}>
                        <div style={{ ...styles.accordionTitle, color: activeAccordion === section.id ? "#2563eb" : "#374151" }}>
                          {section.icon} {section.title}
                        </div>
                        <span>{activeAccordion === section.id ? "▲" : "▼"}</span>
                      </div>
                      {activeAccordion === section.id && (
                        <div style={styles.accordionBody}>
                          {(section.items || []).map((item, i) => (
                            <div key={i} style={styles.accItem}>▶ {item}</div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Things to be careful about */}
                {result.unclear_or_risky_parts && result.unclear_or_risky_parts.length > 0 && (
                  <div style={styles.accordionItem}>
                    <div style={styles.accordionHd} onClick={() => toggleAccordion("careful")}>
                      <div style={{ ...styles.accordionTitle, color: activeAccordion === "careful" ? "#2563eb" : "#374151" }}>
                        🛡️ Things to be careful about
                      </div>
                      <span>{activeAccordion === "careful" ? "▲" : "▼"}</span>
                    </div>
                    {activeAccordion === "careful" && (
                      <div style={styles.accordionBody}>
                        {result.unclear_or_risky_parts.map((item, i) => (
                          <div key={i} style={styles.accItem}>▶ {item}</div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Additional Details */}
                {result.useful_details && result.useful_details.length > 0 && (
                  <div style={styles.additionalDetailsCard}>
                    <div style={styles.additionalDetailsTitle}>📌 Additional details</div>
                    <div style={styles.additionalDetailsContent}>
                      {(result.useful_details || []).map((detail, i) => (
                        <div key={i}>• {detail}</div>
                      ))}
                    </div>
                  </div>
                )}

                <div style={styles.safetyCard}>🛡️ {result.safety_note || "This is AI-generated help, not legal advice."}</div>

                {/* Action Buttons */}
                <div style={{ display: "flex", gap: "8px", marginTop: "12px" }}>
                  <button style={styles.iconBtn} onClick={copyToClipboard}>📋 {copied ? "Copied!" : "Copy All"}</button>
                  <button style={styles.iconBtn} onClick={exportToPDF}>📄 Export PDF</button>
                  <button style={styles.iconBtn} onClick={resetAnalysis}>🔄 New Analysis</button>
                </div>
              </>
            )}
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
              <input type="text" value={chatInput} onChange={(e) => setChatInput(e.target.value)} onKeyPress={(e) => e.key === "Enter" && sendChatMessage()} placeholder="Ask anything about this letter..." style={styles.chatInput} disabled={isStreaming} />
              <button style={styles.sendBtn} onClick={sendChatMessage} disabled={isStreaming}>➤</button>
            </div>

            <div style={styles.privacyRow}>
              🔒 Nothing is saved — your data disappears when you close this tab.
            </div>
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

// ========== STYLES ==========
const styles = {
  page: {
    background: "#f3f6fb",
    minHeight: "100vh",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
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
  brandName: { fontSize: "16px", fontWeight: 600, color: "#1e293b" },
  topRight: { display: "flex", alignItems: "center", gap: "12px" },
  langSel: {
    background: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    padding: "5px 12px",
    fontSize: "12px",
    cursor: "pointer",
  },
  backBtn: {
    border: "1px solid #e5e7eb",
    background: "white",
    padding: "5px 12px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "12px",
  },
  aboutBtn: {
    border: "1px solid #e5e7eb",
    background: "white",
    padding: "5px 12px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "12px",
  },
  main: {
    display: "grid",
    gridTemplateColumns: "300px 1fr",
    minHeight: "calc(100vh - 55px)",
  },
  leftPanel: { padding: "16px", borderRight: "1px solid #e5e7eb", display: "flex", flexDirection: "column", gap: "12px", background: "#fafcff" },
  rightPanel: { display: "flex", flexDirection: "column" },
  card: { background: "white", border: "1px solid #e5e7eb", borderRadius: "16px", padding: "16px" },
  cardHd: { display: "flex", alignItems: "center", gap: "8px", marginBottom: "14px" },
  stepBadge: {
    width: "22px", height: "22px", borderRadius: "50%", background: "#2563eb", color: "white",
    fontSize: "10px", fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center",
  },
  cardTitle: { fontSize: "13px", fontWeight: 600, color: "#1e293b" },
  modeToggle: { display: "flex", gap: "8px", marginBottom: "12px" },
  modeBtn: { flex: 1, padding: "8px", borderRadius: "40px", fontSize: "12px", fontWeight: 500, cursor: "pointer", border: "1px solid #e5e7eb", background: "#f8fafc", color: "#6b7280" },
  modeBtnActive: { background: "#eff6ff", border: "1px solid #2563eb", color: "#2563eb" },
  fakeTextarea: {
    width: "100%", minHeight: "140px", border: "1px solid #e5e7eb", borderRadius: "12px",
    padding: "12px", fontSize: "12px", outline: "none", background: "white", fontFamily: "monospace", resize: "vertical",
  },
  dropZone: {
    border: "2px dashed #c7d2fe", borderRadius: "12px", padding: "24px", textAlign: "center",
    background: "#f8fbff", cursor: "pointer", minHeight: "140px", display: "flex", flexDirection: "column",
    alignItems: "center", justifyContent: "center", gap: "6px",
  },
  dropIcon: { fontSize: "32px" }, dropText: { fontSize: "12px", color: "#4b5563" }, dropSubtext: { fontSize: "10px", color: "#9ca3af" },
  fileName: { marginTop: "6px", color: "#2563eb", fontSize: "11px", fontWeight: 500 },
  btnNew: { width: "100%", marginTop: "12px", padding: "10px", borderRadius: "40px", background: "#2563eb", color: "white", border: "none", fontSize: "13px", fontWeight: 600, cursor: "pointer" },
  loadingCard: { marginTop: "12px", padding: "12px", background: "#f8fafc", borderRadius: "12px", textAlign: "center", border: "1px solid #e5e7eb" },
  spinner: { width: "20px", height: "20px", border: "2px solid #e5e7eb", borderTop: "2px solid #2563eb", borderRadius: "50%", animation: "spin 1s linear infinite", margin: "0 auto 8px" },
  loadingStep: { fontSize: "10px", color: "#2563eb" },
  previewToggle: { display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 10px", background: "#f8fafc", border: "1px solid #e5e7eb", borderRadius: "8px", cursor: "pointer", marginTop: "8px", fontSize: "10px" },
  previewLabel: { display: "flex", alignItems: "center", gap: "5px", color: "#6b7280" },
  previewText: { background: "#f8fafc", border: "1px solid #e5e7eb", borderRadius: "8px", padding: "10px", fontSize: "10px", marginTop: "6px", maxHeight: "100px", overflowY: "auto", color: "#6b7280" },
  searchInput: { display: "flex", gap: "6px", alignItems: "center", background: "#f8fafc", border: "1px solid #e5e7eb", borderRadius: "8px", padding: "8px 10px", marginBottom: "6px" },
  searchInputField: { flex: 1, border: "none", outline: "none", background: "transparent", fontSize: "11px" },
  searchResults: { marginTop: "8px", maxHeight: "150px", overflowY: "auto" },
  searchResultItem: { padding: "8px", borderBottom: "1px solid #e5e7eb", fontSize: "10px" },
  searchResultSender: { fontWeight: 600, color: "#2563eb" },
  searchResultTopic: { color: "#6b7280", marginTop: "2px" },
  searchNoResults: { fontSize: "10px", color: "#9ca3af", textAlign: "center", padding: "12px" },
  sessionNote: { fontSize: "10px", color: "#9ca3af", marginTop: "6px" },
  resultsArea: { flex: 1, padding: "16px", display: "flex", flexDirection: "column", gap: "12px", overflowY: "auto", maxHeight: "calc(100vh - 380px)" },
  emptyState: { textAlign: "center", padding: "48px 20px", color: "#9ca3af", background: "white", borderRadius: "16px", border: "1px solid #e5e7eb" },
  bottomLineCard: { background: "#fefce8", border: "1px solid #fef08a", borderRadius: "16px", padding: "16px" },
  blLabel: { fontSize: "10px", color: "#ca8a04", fontWeight: 700, textTransform: "uppercase", marginBottom: "6px" },
  blText: { fontSize: "15px", fontWeight: 600, lineHeight: 1.4, color: "#1e293b" },
  metaRow: { display: "flex", gap: "16px", flexWrap: "wrap", fontSize: "11px", color: "#6b7280", alignItems: "center" },
  urgencyBadge: { display: "inline-flex", alignItems: "center", gap: "4px", color: "#ea580c", fontWeight: 600 },
  deadlineBadge: { display: "inline-flex", alignItems: "center", gap: "6px", background: "#fef3c7", border: "1px solid #fed7aa", borderRadius: "8px", padding: "5px 12px", fontSize: "11px", color: "#ea580c", fontWeight: 600, width: "fit-content" },
  reliability: { background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: "12px", padding: "10px 14px" },
  relTitle: { fontSize: "12px", fontWeight: 600, color: "#166534", marginBottom: "3px" },
  relSub: { fontSize: "10px", color: "#6b7280" },
  accordionWrap: { display: "flex", flexDirection: "column", gap: "6px" },
  accordionItem: { border: "1px solid #e5e7eb", borderRadius: "12px", overflow: "hidden" },
  accordionHd: { display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 14px", cursor: "pointer", background: "white" },
  accordionTitle: { fontSize: "12px", fontWeight: 600, display: "flex", alignItems: "center", gap: "7px" },
  accordionBody: { padding: "10px 14px", background: "#f8fafc", borderTop: "1px solid #e5e7eb" },
  accItem: { fontSize: "11px", color: "#4b5563", lineHeight: 1.5, marginBottom: "6px" },
  additionalDetailsCard: { background: "#f3e8ff", borderRadius: "12px", padding: "12px", border: "1px solid #e9d5ff" },
  additionalDetailsTitle: { fontWeight: 700, fontSize: "11px", marginBottom: "8px", color: "#6b21a5" },
  additionalDetailsContent: { fontSize: "10px", color: "#4c1d95", lineHeight: 1.5 },
  safetyCard: { background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: "12px", padding: "10px", fontSize: "10px", color: "#166534" },
  iconBtn: { background: "white", border: "1px solid #e5e7eb", borderRadius: "8px", padding: "6px 12px", fontSize: "11px", cursor: "pointer", display: "flex", alignItems: "center", gap: "6px" },
  chatSection: { borderTop: "1px solid #e5e7eb", background: "white" },
  chatHeader: { padding: "12px 20px", borderBottom: "1px solid #e5e7eb", display: "flex", alignItems: "center", gap: "10px" },
  onlineDot: { width: "8px", height: "8px", borderRadius: "50%", background: "#22c55e" },
  chatTitle: { fontSize: "13px", fontWeight: 600 }, chatSub: { fontSize: "10px", color: "#9ca3af" },
  chatMessages: { padding: "14px 20px", display: "flex", flexDirection: "column", gap: "8px", maxHeight: "240px", overflowY: "auto", background: "#fafcff" },
  msg: { display: "flex" },
  bubble: { padding: "8px 12px", borderRadius: "12px", fontSize: "12px", lineHeight: 1.5, maxWidth: "70%" },
  userBubble: { background: "#2563eb", color: "white", borderBottomRightRadius: "4px" },
  assistantBubble: { background: "#f1f5f9", color: "#1e293b", borderBottomLeftRadius: "4px" },
  cursor: { display: "inline-block", width: "2px", height: "12px", background: "#2563eb", marginLeft: "2px", animation: "blink 1s infinite" },
  suggestions: { padding: "8px 20px", display: "flex", gap: "6px", flexWrap: "wrap", borderTop: "1px solid #e5e7eb", background: "white" },
  sug: { padding: "4px 10px", borderRadius: "20px", border: "1px solid #e5e7eb", fontSize: "11px", cursor: "pointer", background: "#f8fafc" },
  chatInputRow: { padding: "10px 20px", borderTop: "1px solid #e5e7eb", display: "flex", gap: "8px", alignItems: "center", background: "white" },
  chatInput: { flex: 1, background: "#f8fafc", border: "1px solid #e5e7eb", borderRadius: "24px", padding: "10px 16px", fontSize: "12px", outline: "none" },
  sendBtn: { width: "36px", height: "36px", borderRadius: "50%", background: "#2563eb", border: "none", color: "white", cursor: "pointer", fontSize: "16px" },
  privacyRow: { padding: "8px 20px", borderTop: "1px solid #e5e7eb", fontSize: "10px", color: "#9ca3af", display: "flex", alignItems: "center", gap: "6px", background: "#fafcff" },
  skeletonCard: { height: "100px", borderRadius: "12px", background: "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)", backgroundSize: "200% 100%", marginBottom: "10px" },
  modalOverlay: { position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 },
  modalContent: { background: "white", padding: "24px", borderRadius: "24px", maxWidth: "450px", width: "90%" },
  modalClose: { marginTop: "16px", padding: "8px 16px", background: "#2563eb", color: "white", border: "none", borderRadius: "40px", cursor: "pointer" },
};

// Add animations
const styleSheet = document.createElement("style");
styleSheet.textContent = `@keyframes spin { to { transform: rotate(360deg); } } @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }`;
document.head.appendChild(styleSheet);