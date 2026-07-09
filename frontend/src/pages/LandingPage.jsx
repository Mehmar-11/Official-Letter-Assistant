import { useState } from "react";
import image123 from "../assets/image123.png";

// ========== LANGUAGE NAMES WITH FLAGS ==========
const LANGUAGE_NAMES = {
  English: "🇬🇧 English",
  German: "🇩🇪 Deutsch",
  Turkish: "🇹🇷 Türkçe",
  Arabic: "🇸🇦 العربية",
  Hindi: "🇮🇳 हिन्दी",
  French: "🇫🇷 Français",
  Spanish: "🇪🇸 Español",
  Italian: "🇮🇹 Italiano",
  Portuguese: "🇵🇹 Português",
  Dutch: "🇳🇱 Nederlands",
  Polish: "🇵🇱 Polski",
  Russian: "🇷🇺 Русский",
  Japanese: "🇯🇵 日本語",
  Korean: "🇰🇷 한국어",
  Chinese: "🇨🇳 中文",
};

// ========== LANDING PAGE TRANSLATIONS ==========
const LANDING_LABELS = {
  English: {
    title: "German Official Letter Assistant",
    heading: "Turn complex German official letters into clear actions, deadlines, and risks.",
    text: "Health insurance, bank notices, government letters – any official German letter can be confusing. Our app tells you what to do, what to watch out for, and what happens if you miss a deadline.",
    button: "Analyze My Letter",
    features: {
      whatToDo: "What to do",
      deadlines: "Deadlines",
      payment: "Payment",
      risks: "Risks",
    },
  },
  German: {
    title: "Deutscher Offizieller Briefassistent",
    heading: "Verwandeln Sie komplexe deutsche offizielle Briefe in klare Handlungen, Fristen und Risiken.",
    text: "Krankenversicherung, Bankmitteilungen, Behördenbriefe – jeder offizielle deutsche Brief kann verwirrend sein. Unsere App sagt Ihnen, was zu tun ist, worauf Sie achten müssen und was passiert, wenn Sie eine Frist verpassen.",
    button: "Meinen Brief analysieren",
    features: {
      whatToDo: "Was tun",
      deadlines: "Fristen",
      payment: "Zahlung",
      risks: "Risiken",
    },
  },
  Turkish: {
    title: "Alman Resmi Mektup Asistanı",
    heading: "Karmaşık Alman resmi mektuplarını net eylemlere, son tarihlere ve risklere dönüştürün.",
    text: "Sağlık sigortası, banka bildirimleri, devlet mektupları – her resmi Alman mektubu kafa karıştırıcı olabilir. Uygulamamız size ne yapmanız gerektiğini, nelere dikkat etmeniz gerektiğini ve bir son tarihi kaçırırsanız ne olacağını söyler.",
    button: "Mektubumu Analiz Et",
    features: {
      whatToDo: "Ne yapmalı",
      deadlines: "Son tarihler",
      payment: "Ödeme",
      risks: "Riskler",
    },
  },
  Arabic: {
    title: "مساعد الرسائل الألمانية الرسمية",
    heading: "حوّل الرسائل الألمانية الرسمية المعقدة إلى إجراءات واضحة ومواعيد نهائية ومخاطر.",
    text: "التأمين الصحي، إشعارات البنك، رسائل الحكومة – أي رسالة ألمانية رسمية يمكن أن تكون مربكة. يخبرك تطبيقنا بما يجب القيام به، وما يجب الحذر منه، وما يحدث إذا فاتك موعد نهائي.",
    button: "تحليل رسالتي",
    features: {
      whatToDo: "ما العمل",
      deadlines: "المواعيد النهائية",
      payment: "الدفع",
      risks: "المخاطر",
    },
  },
  Hindi: {
    title: "जर्मन आधिकारिक पत्र सहायक",
    heading: "जटिल जर्मन आधिकारिक पत्रों को स्पष्ट कार्यों, समय-सीमाओं और जोखिमों में बदलें।",
    text: "स्वास्थ्य बीमा, बैंक सूचनाएं, सरकारी पत्र – कोई भी आधिकारिक जर्मन पत्र भ्रमित करने वाला हो सकता है। हमारा ऐप आपको बताता है कि क्या करना है, किस बात का ध्यान रखना है, और यदि आप समय-सीमा चूक जाते हैं तो क्या होता है।",
    button: "मेरे पत्र का विश्लेषण करें",
    features: {
      whatToDo: "क्या करें",
      deadlines: "समय-सीमाएं",
      payment: "भुगतान",
      risks: "जोखिम",
    },
  },
  French: {
    title: "Assistant de Lettres Officielles Allemandes",
    heading: "Transformez les lettres officielles allemandes complexes en actions claires, délais et risques.",
    text: "Assurance maladie, avis bancaires, lettres gouvernementales – toute lettre officielle allemande peut être déroutante. Notre application vous dit quoi faire, à quoi faire attention et ce qui se passe si vous manquez un délai.",
    button: "Analyser Ma Lettre",
    features: {
      whatToDo: "Que faire",
      deadlines: "Délais",
      payment: "Paiement",
      risks: "Risques",
    },
  },
  Spanish: {
    title: "Asistente de Cartas Oficiales Alemanas",
    heading: "Convierte cartas oficiales alemanas complejas en acciones claras, plazos y riesgos.",
    text: "Seguro médico, avisos bancarios, cartas gubernamentales – cualquier carta oficial alemana puede ser confusa. Nuestra aplicación te dice qué hacer, a qué prestar atención y qué sucede si pierdes un plazo.",
    button: "Analizar Mi Carta",
    features: {
      whatToDo: "Qué hacer",
      deadlines: "Plazos",
      payment: "Pago",
      risks: "Riesgos",
    },
  },
  Italian: {
    title: "Assistente per Lettere Ufficiali Tedesche",
    heading: "Trasforma complesse lettere ufficiali tedesche in azioni chiare, scadenze e rischi.",
    text: "Assicurazione sanitaria, avvisi bancari, lettere governative – qualsiasi lettera ufficiale tedesca può creare confusione. La nostra app ti dice cosa fare, a cosa stare attento e cosa succede se perdi una scadenza.",
    button: "Analizza La Mia Lettera",
    features: {
      whatToDo: "Cosa fare",
      deadlines: "Scadenze",
      payment: "Pagamento",
      risks: "Rischi",
    },
  },
  Portuguese: {
    title: "Assistente de Cartas Oficiais Alemãs",
    heading: "Transforme cartas oficiais alemãs complexas em ações claras, prazos e riscos.",
    text: "Seguro de saúde, avisos bancários, cartas governamentais – qualquer carta oficial alemã pode ser confusa. Nosso aplicativo diz o que fazer, no que prestar atenção e o que acontece se você perder um prazo.",
    button: "Analisar Minha Carta",
    features: {
      whatToDo: "O que fazer",
      deadlines: "Prazos",
      payment: "Pagamento",
      risks: "Riscos",
    },
  },
  Dutch: {
    title: "Duitse Officiële Brievenassistent",
    heading: "Zet complexe Duitse officiële brieven om in duidelijke acties, deadlines en risico's.",
    text: "Zorgverzekering, bankberichten, overheidsbrieven – elke officiële Duitse brief kan verwarrend zijn. Onze app vertelt u wat u moet doen, waar u op moet letten en wat er gebeurt als u een deadline mist.",
    button: "Analyseer Mijn Brief",
    features: {
      whatToDo: "Wat te doen",
      deadlines: "Deadlines",
      payment: "Betaling",
      risks: "Risico's",
    },
  },
  Polish: {
    title: "Asystent Niemieckich Listów Urzędowych",
    heading: "Zamień złożone niemieckie listy urzędowe na jasne działania, terminy i ryzyko.",
    text: "Ubezpieczenie zdrowotne, powiadomienia bankowe, listy rządowe – każdy oficjalny niemiecki list może być mylący. Nasza aplikacja mówi ci, co robić, na co uważać i co się stanie, jeśli przegapisz termin.",
    button: "Przeanalizuj Mój List",
    features: {
      whatToDo: "Co robić",
      deadlines: "Terminy",
      payment: "Płatność",
      risks: "Ryzyko",
    },
  },
  Russian: {
    title: "Помощник по Немецким Официальным Письмам",
    heading: "Превратите сложные немецкие официальные письма в четкие действия, сроки и риски.",
    text: "Медицинская страховка, банковские уведомления, правительственные письма – любое официальное немецкое письмо может сбивать с толку. Наше приложение говорит вам, что делать, на что обращать внимание и что произойдет, если вы пропустите срок.",
    button: "Проанализировать Мое Письмо",
    features: {
      whatToDo: "Что делать",
      deadlines: "Сроки",
      payment: "Оплата",
      risks: "Риски",
    },
  },
  Japanese: {
    title: "ドイツ語公式レターアシスタント",
    heading: "複雑なドイツ語の公式レターを明確な行動、期限、リスクに変換します。",
    text: "健康保険、銀行通知、政府のレター – 公式のドイツ語レターはどれも混乱を招く可能性があります。私たちのアプリは、何をすべきか、何に注意すべきか、期限を過ぎたらどうなるかを教えます。",
    button: "私の手紙を分析",
    features: {
      whatToDo: "何をすべきか",
      deadlines: "期限",
      payment: "支払い",
      risks: "リスク",
    },
  },
  Korean: {
    title: "독일어 공식 편지 어시스턴트",
    heading: "복잡한 독일어 공식 편지를 명확한 행동, 마감일 및 위험으로 전환하세요.",
    text: "건강 보험, 은행 통지, 정부 편지 – 공식 독일어 편지는 모두 혼란스러울 수 있습니다. 우리 앱은 무엇을 해야 하는지, 무엇을 주의해야 하는지, 마감일을 놓치면 어떻게 되는지 알려줍니다.",
    button: "내 편지 분석하기",
    features: {
      whatToDo: "해야 할 일",
      deadlines: "마감일",
      payment: "결제",
      risks: "위험",
    },
  },
  Chinese: {
    title: "德语官方信件助手",
    heading: "将复杂的德语官方信件转化为清晰的操作、截止日期和风险。",
    text: "健康保险、银行通知、政府信件 – 任何官方的德语信件都可能令人困惑。我们的应用程序会告诉您该做什么、要注意什么以及如果错过截止日期会发生什么。",
    button: "分析我的信件",
    features: {
      whatToDo: "该做什么",
      deadlines: "截止日期",
      payment: "付款",
      risks: "风险",
    },
  },
};

export default function LandingPage({ onStart }) {
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState("English");

  const labels = LANDING_LABELS[language] || LANDING_LABELS.English;

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    localStorage.setItem("landingDarkMode", !darkMode);
  };

  // Check for saved dark mode preference
  useState(() => {
    const saved = localStorage.getItem("landingDarkMode");
    if (saved === "true") setDarkMode(true);
  }, []);

  const styles = {
    page: {
      height: "100vh",
      width: "100%",
      background: darkMode 
        ? "linear-gradient(135deg, #0f172a, #1e293b)" 
        : "linear-gradient(135deg, #faf7ff, #f4f0ff)",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "20px",
      boxSizing: "border-box",
      overflow: "hidden",
      transition: "all 0.3s ease",
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
      color: darkMode ? "#e2e8f0" : "#1e1b4b",
      margin: 0,
      transition: "color 0.3s ease",
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
      color: darkMode ? "#a78bfa" : "#5b21b6",
      marginBottom: "16px",
      transition: "color 0.3s ease",
    },

    text: {
      fontSize: "16px",
      lineHeight: "1.6",
      color: darkMode ? "#94a3b8" : "#4b5563",
      marginBottom: "24px",
      transition: "color 0.3s ease",
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
      transition: "transform 0.2s ease, box-shadow 0.2s ease",
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
      background: darkMode ? "#1e293b" : "#fff",
      padding: "14px",
      borderRadius: "16px",
      minWidth: "85px",
      boxShadow: darkMode 
        ? "0 6px 15px rgba(0,0,0,0.3)" 
        : "0 6px 15px rgba(0,0,0,0.05)",
      fontWeight: "600",
      color: darkMode ? "#a78bfa" : "#4c1d95",
      fontSize: "13px",
      border: darkMode ? "1px solid #334155" : "none",
      transition: "all 0.3s ease",
    },

    icon: {
      fontSize: "24px",
    },

    topBar: {
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      padding: "12px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "flex-end",
      gap: "12px",
      background: darkMode ? "rgba(15, 23, 42, 0.9)" : "rgba(255, 255, 255, 0.9)",
      backdropFilter: "blur(10px)",
      borderBottom: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      zIndex: 100,
      transition: "all 0.3s ease",
    },

    langSel: {
      background: darkMode ? "#334155" : "white",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "8px",
      padding: "6px 12px",
      fontSize: "12px",
      cursor: "pointer",
      color: darkMode ? "#e2e8f0" : "#374151",
      transition: "all 0.3s ease",
    },

    themeBtn: {
      background: darkMode ? "#334155" : "white",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "8px",
      padding: "6px 12px",
      cursor: "pointer",
      fontSize: "16px",
      transition: "all 0.3s ease",
    },

    brandSmall: {
      display: "flex",
      alignItems: "center",
      gap: "8px",
      marginRight: "auto",
      color: darkMode ? "#e2e8f0" : "#1e1b4b",
      fontWeight: 600,
      fontSize: "14px",
    },

    brandIcon: {
      fontSize: "18px",
    },
  };

  return (
    <div style={styles.page}>
      {/* Top Bar with Language and Dark Mode */}
      <div style={styles.topBar}>
        <div style={styles.brandSmall}>
          <span style={styles.brandIcon}>📄</span>
          <span>German Letter Assistant</span>
        </div>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)} 
          style={styles.langSel}
        >
          {Object.keys(LANGUAGE_NAMES).map(lang => (
            <option key={lang} value={lang}>{LANGUAGE_NAMES[lang]}</option>
          ))}
        </select>
        <button style={styles.themeBtn} onClick={toggleDarkMode}>
          {darkMode ? "☀️" : "🌙"}
        </button>
      </div>

      <div style={styles.content}>
        {/* Left Section */}
        <div style={styles.left}>
          <div style={styles.logoRow}>
            <div style={styles.logo}>MS</div>
            <h1 style={styles.title}>
              {labels.title}
            </h1>
          </div>

          <div style={styles.line}></div>

          <h2 style={styles.heading}>
            {labels.heading}
          </h2>

          <p style={styles.text}>
            {labels.text}
          </p>

          <button 
            style={styles.button} 
            onClick={onStart}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "scale(1.05)";
              e.currentTarget.style.boxShadow = "0 15px 30px rgba(124,58,237,0.35)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "scale(1)";
              e.currentTarget.style.boxShadow = "0 10px 20px rgba(124,58,237,0.25)";
            }}
          >
            {labels.button}
          </button>

          <div style={styles.features}>
            <div style={styles.featureCard}>
              <span style={styles.icon}>📋</span>
              <span>{labels.features.whatToDo}</span>
            </div>

            <div style={styles.featureCard}>
              <span style={styles.icon}>📅</span>
              <span>{labels.features.deadlines}</span>
            </div>

            <div style={styles.featureCard}>
              <span style={styles.icon}>💶</span>
              <span>{labels.features.payment}</span>
            </div>

            <div style={styles.featureCard}>
              <span style={styles.icon}>⚠️</span>
              <span>{labels.features.risks}</span>
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