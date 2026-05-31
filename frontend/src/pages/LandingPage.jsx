export default function LandingPage({ onStart }) {
  const conversionImage = `data:image/svg+xml,${encodeURIComponent(`
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="100%" height="100%">
      <rect width="800" height="400" fill="#f8fafc" rx="20"/>
      <rect x="30" y="60" width="320" height="280" fill="#fff7ed" stroke="#fed7aa" stroke-width="2" rx="16"/>
      <text x="190" y="90" font-family="Arial" font-size="16" font-weight="bold" fill="#c2410c" text-anchor="middle">📄 German Official Letter</text>
      <line x1="50" y1="105" x2="330" y2="105" stroke="#fed7aa" stroke-width="1"/>
      <text x="50" y="130" font-family="monospace" font-size="12" fill="#9a3412">
        <tspan x="50" dy="0">Betreff: Zahlungserinnerung</tspan>
        <tspan x="50" dy="20">Sehr geehrter Kunde,</tspan>
        <tspan x="50" dy="20">Sie haben noch 89,90 € offen.</tspan>
        <tspan x="50" dy="20">Bitte zahlen Sie bis zum</tspan>
        <tspan x="50" dy="20">14.06.2026. Bei verspäteter</tspan>
        <tspan x="50" dy="20">Zahlung fallen Mahngebühren</tspan>
        <tspan x="50" dy="20">in Höhe von 15 € an.</tspan>
        <tspan x="50" dy="20">Mit freundlichen Grüßen,</tspan>
        <tspan x="50" dy="20">VitaPlus Krankenkasse</tspan>
      </text>
      <text x="370" y="210" font-family="Arial" font-size="40" fill="#7c3aed" text-anchor="middle">→</text>
      <rect x="420" y="60" width="350" height="280" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="2" rx="16"/>
      <text x="595" y="90" font-family="Arial" font-size="16" font-weight="bold" fill="#166534" text-anchor="middle">✨ Structured Summary</text>
      <line x1="440" y1="105" x2="750" y2="105" stroke="#bbf7d0" stroke-width="1"/>
      <rect x="440" y="125" width="310" height="40" fill="white" rx="8"/>
      <text x="455" y="150" font-family="Arial" font-size="13" fill="#14532d">✅ Pay 89.90 EUR by June 14, 2026</text>
      <rect x="440" y="175" width="310" height="40" fill="white" rx="8"/>
      <text x="455" y="200" font-family="Arial" font-size="13" fill="#14532d">📅 Deadline: June 14, 2026</text>
      <rect x="440" y="225" width="310" height="40" fill="white" rx="8"/>
      <text x="455" y="250" font-family="Arial" font-size="13" fill="#14532d">⚠️ Late fee: 15 EUR after deadline</text>
      <rect x="440" y="275" width="310" height="40" fill="white" rx="8"/>
      <text x="455" y="300" font-family="Arial" font-size="13" fill="#14532d">🏦 IBAN: DE12 3705 0299 1234 5678 90</text>
    </svg>
  `)}`;

  return (
    <div style={styles.page}>
      <div style={styles.content}>
        <div style={styles.left}>
          <div style={styles.logoRow}>
            <div style={styles.logo}>MS</div>
            <h1 style={styles.title}>German Official Letter Assistant</h1>
          </div>
          <div style={styles.line}></div>
          <h2 style={styles.heading}>
            Turn complex German official letters into clear actions, deadlines, and risks.
          </h2>
          <p style={styles.text}>
            Imagine receiving a health insurance reminder in German – with payment rules, multiple deadlines, and possible consequences. Our app tells you what to do, what to watch out for, and what happens if you miss a deadline.
          </p>
          <button style={styles.button} onClick={onStart}>Analyze My Letter</button>
          <div style={styles.features}>
            <span>📋 What to do</span>
            <span>📅 Deadlines</span>
            <span>💶 Payment</span>
            <span>⚠️ Risks</span>
          </div>
        </div>
        <div style={styles.right}>
          <img src={conversionImage} alt="Conversion preview" style={styles.heroImage} />
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    width: "100vw",
    background: "linear-gradient(135deg, #faf7ff, #f4f0ff)",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    overflow: "hidden",
    boxSizing: "border-box",
  },
  content: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    width: "90%",
    maxWidth: 1300,
    gap: 40,
    padding: "20px",
    flexWrap: "wrap",
  },
  left: { flex: 1, minWidth: 280 },
  logoRow: { display: "flex", alignItems: "center", gap: 12, marginBottom: 20 },
  logo: {
    width: 48, height: 48, borderRadius: 16,
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "white", display: "flex", alignItems: "center", justifyContent: "center",
    fontWeight: 700, fontSize: 24,
  },
  title: { fontSize: 28, fontWeight: 700, color: "#1e1b4b", margin: 0 },
  line: { width: 60, height: 4, background: "#7c3aed", borderRadius: 4, margin: "20px 0 20px 0" },
  heading: { fontSize: 42, lineHeight: 1.2, fontWeight: 800, color: "#4c1d95", marginBottom: 16 },
  text: { fontSize: 18, lineHeight: 1.4, color: "#4b5563", marginBottom: 28 },
  button: {
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "white", border: "none", padding: "14px 28px", borderRadius: 40,
    fontSize: 16, fontWeight: 600, cursor: "pointer",
  },
  features: { display: "flex", gap: 24, marginTop: 36, fontSize: 15, fontWeight: 600, color: "#4c1d95", flexWrap: "wrap" },
  right: { flex: 1, display: "flex", justifyContent: "center", minWidth: 300 },
  heroImage: { width: "100%", maxWidth: 650, height: "auto", borderRadius: 24, boxShadow: "0 20px 35px -10px rgba(0,0,0,0.15)" },
};