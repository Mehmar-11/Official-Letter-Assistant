import image123 from "../assets/image123.png";

export default function LandingPage({ onStart }) {
  return (
    <div style={styles.page}>
      <div style={styles.content}>
        {/* Left Section */}
        <div style={styles.left}>
          <div style={styles.logoRow}>
            <div style={styles.logo}>MS</div>
            <h1 style={styles.title}>
              German Official Letter Assistant
            </h1>
          </div>

          <div style={styles.line}></div>

          <h2 style={styles.heading}>
            Turn complex German official letters into clear actions,
            deadlines, and risks.
          </h2>

          <p style={styles.text}>
            Health insurance, bank notices, government letters – any official German letter can be confusing. Our app tells you what to do, what to watch out for, and what happens if you miss a deadline.
          </p>

          <button style={styles.button} onClick={onStart}>
            Analyze My Letter
          </button>

          <div style={styles.features}>
            <div style={styles.featureCard}>
              <span style={styles.icon}>📋</span>
              <span>What to do</span>
            </div>

            <div style={styles.featureCard}>
              <span style={styles.icon}>📅</span>
              <span>Deadlines</span>
            </div>

            <div style={styles.featureCard}>
              <span style={styles.icon}>💶</span>
              <span>Payment</span>
            </div>

            <div style={styles.featureCard}>
              <span style={styles.icon}>⚠️</span>
              <span>Risks</span>
            </div>
          </div>
        </div>

        {/* Right Section */}
        <div style={styles.right}>
          <img
            src={image123}
            alt="German Official Letter Assistant"
            style={styles.heroImage}
          />
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    width: "100%",
    background: "linear-gradient(135deg, #faf7ff, #f4f0ff)",
    fontFamily:
      "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    boxSizing: "border-box",
    overflow: "hidden",
  },

  content: {
    width: "100%",
    maxWidth: "1400px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: "40px",
    flexWrap: "wrap",
  },

  left: {
    flex: 1,
    minWidth: "300px",
    maxWidth: "550px",
  },

  right: {
    flex: 1,
    minWidth: "350px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },

  heroImage: {
    width: "100%",
    maxWidth: "700px",
    height: "auto",
    objectFit: "contain",
  },

  logoRow: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "20px",
  },

  logo: {
    width: "48px",
    height: "48px",
    borderRadius: "14px",
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "22px",
    fontWeight: "700",
  },

  title: {
    fontSize: "28px",
    fontWeight: "700",
    color: "#1e1b4b",
    margin: 0,
  },

  line: {
    width: "60px",
    height: "4px",
    background: "#7c3aed",
    borderRadius: "20px",
    marginBottom: "24px",
  },

  heading: {
    fontSize: "40px",
    fontWeight: "800",
    lineHeight: "1.2",
    color: "#5b21b6",
    marginBottom: "16px",
  },

  text: {
    fontSize: "16px",
    lineHeight: "1.6",
    color: "#4b5563",
    marginBottom: "24px",
  },

  button: {
    background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
    color: "#fff",
    border: "none",
    borderRadius: "999px",
    padding: "12px 28px",
    fontSize: "15px",
    fontWeight: "600",
    cursor: "pointer",
    boxShadow: "0 10px 20px rgba(124,58,237,0.25)",
  },

  features: {
    display: "flex",
    gap: "14px",
    flexWrap: "wrap",
    marginTop: "30px",
  },

  featureCard: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "8px",
    background: "#fff",
    padding: "14px",
    borderRadius: "16px",
    minWidth: "85px",
    boxShadow: "0 6px 15px rgba(0,0,0,0.05)",
    fontWeight: "600",
    color: "#4c1d95",
    fontSize: "13px",
  },

  icon: {
    fontSize: "24px",
  },
};