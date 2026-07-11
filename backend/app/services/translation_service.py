import { useState, useEffect, useRef } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ========== COMPLETE TRANSLATIONS FOR ALL 15 LANGUAGES ==========
const UI_LABELS = {
  English: {
    copy: "📋 Copy",
    pdf: "📄 PDF",
    new: "🔄 New",
    chatTitle: "💬 Chat with Assistant",
    chatSub: "Ask anything about this letter",
    placeholder: "Ask anything about this letter...",
    suggestions: ["Help me draft a reply", "What should I do first?", "Is this urgent?", "Explain in simpler words"],
    welcome: "Hey! I've read your letter. Ask me anything — I'll keep it simple. 👋",
    aboutTitle: "ℹ️ German Letter Assistant",
    aboutFeatures: "Features: OCR, Smart Chat with Streaming, Reply Draft Assistant, Multi-language Output",
    aboutPrivacy: "Privacy: Your documents are processed temporarily and not stored.",
    aboutDisclaimer: "Disclaimer: This is AI‑generated help, not legal advice.",
    close: "Close",
    emptyTitle: "No letter analyzed yet",
    emptySub: "Paste or upload a letter to see analysis",
    bottomLine: "✨ Bottom line",
    bridgeText: "📖 I've read your letter. Anything unclear?",
    bridgeAsk: "Ask below ↓",
    urgency: "urgency",
    paymentInvolved: "💳 Payment involved",
    quality: "✓ Analysis Quality:",
    additionalDetails: "📌 Additional details",
    safety: "🛡️",
    back: "← Back",
    about: "About",
    pasteText: "📄 Paste Text",
    upload: "📑 Upload PDF / Image",
    dropText: "Click to upload PDF or image",
    dropSubtext: "or drag and drop",
    analyzeBtn: "✨ Analyze Letter",
    privacy: "Your data is private — nothing is stored",
    processing: "Processing your letter...",
    accordionWhat: "What to do",
    accordionPay: "How to pay",
    accordionDocs: "Documents you may need",
    accordionCons: "What happens if you ignore this",
    accordionCareful: "Things to be careful about",
    from: "From",
    whatToDo: "What you need to do",
    deadline: "The deadline is",
    consequences: "Possible consequences",
    draftReply: "Here's a draft reply",
    basedOn: "Based on the letter I analyzed:",
    actionsNeeded: "Actions needed",
    payment: "Payment details",
    uploadTitle: "Your letter",
    lettersAnalyzed: "letter analyzed",
    lettersAnalyzedPlural: "letters analyzed",
    copied: "✅ Copied!",
    actBefore: "Make sure to act before this date!",
    analysisResult: "Analysis Result",
    brandName: "German Letter Assistant",
    daysLeft: "days left to act",
    mayNotBeOfficial: "⚠️ May not be official",
    typeMessage: "Type your message...",
    send: "Send",
    translating: "Translating...",
    howToPay: "How to pay",
    documentsNeeded: "Documents you may need",
    whatHappensIfIgnore: "What happens if you ignore this",
    thingsToBeCareful: "Things to be careful about",
    analyzeFirst: "📄 Analyze a letter first to start chatting...",
  },
  German: {
    copy: "📋 Kopieren",
    pdf: "📄 PDF",
    new: "🔄 Neu",
    chatTitle: "💬 Chat mit Assistent",
    chatSub: "Fragen Sie alles zu diesem Brief",
    placeholder: "Fragen Sie alles zu diesem Brief...",
    suggestions: ["Hilf mir einen Antwortentwurf zu erstellen", "Was soll ich zuerst tun?", "Ist das dringend?", "In einfacheren Worten erklären"],
    welcome: "Hallo! Ich habe Ihren Brief gelesen. Fragen Sie mich alles — ich halte es einfach. 👋",
    aboutTitle: "ℹ️ German Letter Assistant",
    aboutFeatures: "Funktionen: OCR, Smart Chat mit Streaming, Antwortentwurf-Assistent, Mehrsprachige Ausgabe",
    aboutPrivacy: "Datenschutz: Ihre Dokumente werden vorübergehend verarbeitet und nicht gespeichert.",
    aboutDisclaimer: "Haftungsausschluss: Dies ist KI-generierte Hilfe, keine Rechtsberatung.",
    close: "Schließen",
    emptyTitle: "Noch kein Brief analysiert",
    emptySub: "Fügen Sie einen Brief ein oder laden Sie ihn hoch, um eine Analyse zu sehen",
    bottomLine: "✨ Fazit",
    bridgeText: "📖 Ich habe Ihren Brief gelesen. Etwas unklar?",
    bridgeAsk: "Fragen Sie unten ↓",
    urgency: "Dringlichkeit",
    paymentInvolved: "💳 Zahlung beteiligt",
    quality: "✓ Analysequalität:",
    additionalDetails: "📌 Zusätzliche Details",
    safety: "🛡️",
    back: "← Zurück",
    about: "Über",
    pasteText: "📄 Text einfügen",
    upload: "📑 PDF / Bild hochladen",
    dropText: "Klicken Sie hier, um PDF oder Bild hochzuladen",
    dropSubtext: "oder per Drag & Drop",
    analyzeBtn: "✨ Brief analysieren",
    privacy: "Ihre Daten sind privat — nichts wird gespeichert",
    processing: "Verarbeite Ihren Brief...",
    accordionWhat: "Was Sie tun müssen",
    accordionPay: "Wie Sie bezahlen",
    accordionDocs: "Dokumente, die Sie benötigen",
    accordionCons: "Was passiert, wenn Sie dies ignorieren",
    accordionCareful: "Worauf Sie achten sollten",
    from: "Von",
    whatToDo: "Was Sie tun müssen",
    deadline: "Die Frist ist",
    consequences: "Mögliche Folgen",
    draftReply: "Hier ist ein Antwortentwurf",
    basedOn: "Basierend auf dem analysierten Brief:",
    actionsNeeded: "Erforderliche Maßnahmen",
    payment: "Zahlungsdetails",
    uploadTitle: "Ihr Brief",
    lettersAnalyzed: "Brief analysiert",
    lettersAnalyzedPlural: "Briefe analysiert",
    copied: "✅ Kopiert!",
    actBefore: "Stellen Sie sicher, dass Sie vor diesem Datum handeln!",
    analysisResult: "Analyseergebnis",
    brandName: "German Letter Assistant",
    daysLeft: "Tage Zeit zu handeln",
    mayNotBeOfficial: "⚠️ Möglicherweise nicht offiziell",
    typeMessage: "Nachricht eingeben...",
    send: "Senden",
    translating: "Übersetzen...",
    howToPay: "Wie Sie bezahlen",
    documentsNeeded: "Dokumente, die Sie benötigen",
    whatHappensIfIgnore: "Was passiert, wenn Sie dies ignorieren",
    thingsToBeCareful: "Worauf Sie achten sollten",
    analyzeFirst: "📄 Analysieren Sie zuerst einen Brief, um mit dem Chatten zu beginnen...",
  },
  Turkish: {
    copy: "📋 Kopyala",
    pdf: "📄 PDF",
    new: "🔄 Yeni",
    chatTitle: "💬 Asistan ile Sohbet",
    chatSub: "Bu mektup hakkında her şeyi sorun",
    placeholder: "Bu mektup hakkında her şeyi sorun...",
    suggestions: ["Bir cevap taslağı hazırlamama yardım et", "Önce ne yapmalıyım?", "Bu acil mi?", "Daha basit kelimelerle açıkla"],
    welcome: "Merhaba! Mektubunuzu okudum. Bana her şeyi sorabilirsiniz — basit tutacağım. 👋",
    aboutTitle: "ℹ️ Alman Mektup Asistanı",
    aboutFeatures: "Özellikler: OCR, Akıllı Sohbet, Yanıt Taslağı, Çoklu Dil Desteği",
    aboutPrivacy: "Gizlilik: Belgeleriniz geçici olarak işlenir ve saklanmaz.",
    aboutDisclaimer: "Uyarı: Bu AI destekli yardımdır, yasal tavsiye değildir.",
    close: "Kapat",
    emptyTitle: "Henüz mektup analiz edilmedi",
    emptySub: "Analiz görmek için bir mektup yapıştırın veya yükleyin",
    bottomLine: "✨ Özet",
    bridgeText: "📖 Mektubunuzu okudum. Anlaşılmayan bir şey mi var?",
    bridgeAsk: "Aşağıya sorun ↓",
    urgency: "aciliyet",
    paymentInvolved: "💳 Ödeme dahil",
    quality: "✓ Analiz Kalitesi:",
    additionalDetails: "📌 Ek detaylar",
    safety: "🛡️",
    back: "← Geri",
    about: "Hakkında",
    pasteText: "📄 Metin Yapıştır",
    upload: "📑 PDF / Görsel Yükle",
    dropText: "PDF veya görsel yüklemek için tıklayın",
    dropSubtext: "veya sürükleyip bırakın",
    analyzeBtn: "✨ Mektubu Analiz Et",
    privacy: "Verileriniz gizli — hiçbir şey saklanmaz",
    processing: "Mektubunuz işleniyor...",
    accordionWhat: "Yapmanız gerekenler",
    accordionPay: "Nasıl ödeme yapılır",
    accordionDocs: "İhtiyacınız olan belgeler",
    accordionCons: "Bunu görmezden gelirseniz ne olur",
    accordionCareful: "Dikkat edilmesi gerekenler",
    from: "Kimden",
    whatToDo: "Yapmanız gerekenler",
    deadline: "Son tarih",
    consequences: "Olası sonuçlar",
    draftReply: "İşte bir taslak cevap",
    basedOn: "Analiz ettiğim mektuba göre:",
    actionsNeeded: "Gerekli eylemler",
    payment: "Ödeme detayları",
    uploadTitle: "Mektubunuz",
    lettersAnalyzed: "mektup analiz edildi",
    lettersAnalyzedPlural: "mektup analiz edildi",
    copied: "✅ Kopyalandı!",
    actBefore: "Bu tarihten önce harekete geçin!",
    analysisResult: "Analiz Sonucu",
    brandName: "Alman Mektup Asistanı",
    daysLeft: "gün kaldı",
    mayNotBeOfficial: "⚠️ Resmi olmayabilir",
    typeMessage: "Mesajınızı yazın...",
    send: "Gönder",
    translating: "Çevriliyor...",
    howToPay: "Nasıl ödeme yapılır",
    documentsNeeded: "İhtiyacınız olan belgeler",
    whatHappensIfIgnore: "Bunu görmezden gelirseniz ne olur",
    thingsToBeCareful: "Dikkat edilmesi gerekenler",
    analyzeFirst: "📄 Sohbete başlamak için önce bir mektup analiz edin...",
  },
  Arabic: {
    copy: "📋 نسخ",
    pdf: "📄 PDF",
    new: "🔄 جديد",
    chatTitle: "💬 الدردشة مع المساعد",
    chatSub: "اسأل أي شيء عن هذه الرسالة",
    placeholder: "اسأل أي شيء عن هذه الرسالة...",
    suggestions: ["ساعدني في صياغة رد", "ما الذي يجب أن أفعله أولاً؟", "هل هذا عاجل؟", "اشرح بكلمات أبسط"],
    welcome: "مرحباً! لقد قرأت رسالتك. اسألني أي شيء — سأبقيه بسيطاً. 👋",
    aboutTitle: "ℹ️ مساعد الرسائل الألمانية",
    aboutFeatures: "الميزات: OCR، دردشة ذكية، مساعد الردود، إخراج متعدد اللغات",
    aboutPrivacy: "الخصوصية: تتم معالجة مستنداتك بشكل مؤقت ولا يتم تخزينها.",
    aboutDisclaimer: "إخلاء المسؤولية: هذه مساعدة مولدة بالذكاء الاصطناعي، ليست نصيحة قانونية.",
    close: "إغلاق",
    emptyTitle: "لم يتم تحليل أي رسالة بعد",
    emptySub: "الصق أو حمل رسالة لرؤية التحليل",
    bottomLine: "✨ الخلاصة",
    bridgeText: "📖 لقد قرأت رسالتك. هناك شيء غير واضح؟",
    bridgeAsk: "اسأل أدناه ↓",
    urgency: "الإلحاح",
    paymentInvolved: "💳 دفع متضمن",
    quality: "✓ جودة التحليل:",
    additionalDetails: "📌 تفاصيل إضافية",
    safety: "🛡️",
    back: "← رجوع",
    about: "حول",
    pasteText: "📄 لصق النص",
    upload: "📑 تحميل PDF / صورة",
    dropText: "انقر لتحميل PDF أو صورة",
    dropSubtext: "أو اسحب وأفلت",
    analyzeBtn: "✨ تحليل الرسالة",
    privacy: "بياناتك خاصة — لا يتم تخزين أي شيء",
    processing: "جاري معالجة رسالتك...",
    accordionWhat: "ما عليك فعله",
    accordionPay: "كيفية الدفع",
    accordionDocs: "المستندات التي قد تحتاجها",
    accordionCons: "ماذا يحدث إذا تجاهلت هذا",
    accordionCareful: "أشياء يجب الحذر منها",
    from: "من",
    whatToDo: "ما عليك فعله",
    deadline: "الموعد النهائي",
    consequences: "العواقب المحتملة",
    draftReply: "إليك مسودة رد",
    basedOn: "بناءً على الرسالة التي حللتها:",
    actionsNeeded: "الإجراءات المطلوبة",
    payment: "تفاصيل الدفع",
    uploadTitle: "رسالتك",
    lettersAnalyzed: "رسالة تم تحليلها",
    lettersAnalyzedPlural: "رسائل تم تحليلها",
    copied: "✅ تم النسخ!",
    actBefore: "تأكد من التصرف قبل هذا التاريخ!",
    analysisResult: "نتيجة التحليل",
    brandName: "مساعد الرسائل الألمانية",
    daysLeft: "أيام متبقية للعمل",
    mayNotBeOfficial: "⚠️ قد لا تكون رسمية",
    typeMessage: "اكتب رسالتك...",
    send: "إرسال",
    translating: "جاري الترجمة...",
    howToPay: "كيفية الدفع",
    documentsNeeded: "المستندات التي قد تحتاجها",
    whatHappensIfIgnore: "ماذا يحدث إذا تجاهلت هذا",
    thingsToBeCareful: "أشياء يجب الحذر منها",
    analyzeFirst: "📄 قم بتحليل رسالة أولاً لبدء الدردشة...",
  },
  Hindi: {
    copy: "📋 कॉपी करें",
    pdf: "📄 PDF",
    new: "🔄 नया",
    chatTitle: "💬 सहायक से बात करें",
    chatSub: "इस पत्र के बारे में कुछ भी पूछें",
    placeholder: "इस पत्र के बारे में कुछ भी पूछें...",
    suggestions: ["जवाब का ड्राफ्ट बनाने में मदद करें", "मुझे पहले क्या करना चाहिए?", "क्या यह जरूरी है?", "सरल शब्दों में समझाएं"],
    welcome: "नमस्ते! मैंने आपका पत्र पढ़ लिया है। मुझसे कुछ भी पूछें — मैं इसे सरल रखूंगा। 👋",
    aboutTitle: "ℹ️ जर्मन पत्र सहायक",
    aboutFeatures: "विशेषताएं: OCR, स्मार्ट चैट, उत्तर ड्राफ्ट, बहुभाषी आउटपुट",
    aboutPrivacy: "गोपनीयता: आपके दस्तावेज़ अस्थायी रूप से संसाधित होते हैं और संग्रहीत नहीं होते।",
    aboutDisclaimer: "अस्वीकरण: यह AI-जनित सहायता है, कानूनी सलाह नहीं है।",
    close: "बंद करें",
    emptyTitle: "अभी तक कोई पत्र विश्लेषित नहीं किया गया",
    emptySub: "विश्लेषण देखने के लिए पत्र पेस्ट करें या अपलोड करें",
    bottomLine: "✨ निष्कर्ष",
    bridgeText: "📖 मैंने आपका पत्र पढ़ लिया है। कुछ अस्पष्ट है?",
    bridgeAsk: "नीचे पूछें ↓",
    urgency: "तात्कालिकता",
    paymentInvolved: "💳 भुगतान शामिल",
    quality: "✓ विश्लेषण गुणवत्ता:",
    additionalDetails: "📌 अतिरिक्त विवरण",
    safety: "🛡️",
    back: "← वापस",
    about: "के बारे में",
    pasteText: "📄 टेक्स्ट पेस्ट करें",
    upload: "📑 PDF / छवि अपलोड करें",
    dropText: "PDF या छवि अपलोड करने के लिए क्लिक करें",
    dropSubtext: "या खींचकर छोड़ें",
    analyzeBtn: "✨ पत्र का विश्लेषण करें",
    privacy: "आपका डेटा निजी है — कुछ भी संग्रहीत नहीं है",
    processing: "आपके पत्र को संसाधित किया जा रहा है...",
    accordionWhat: "आपको क्या करना है",
    accordionPay: "भुगतान कैसे करें",
    accordionDocs: "आपको जिन दस्तावेज़ों की आवश्यकता हो सकती है",
    accordionCons: "यदि आप इसे अनदेखा करते हैं तो क्या होता है",
    accordionCareful: "ध्यान देने योग्य बातें",
    from: "से",
    whatToDo: "आपको क्या करना है",
    deadline: "अंतिम तिथि",
    consequences: "संभावित परिणाम",
    draftReply: "यहाँ एक ड्राफ्ट जवाब है",
    basedOn: "मेरे द्वारा विश्लेषित पत्र के आधार पर:",
    actionsNeeded: "आवश्यक कार्रवाई",
    payment: "भुगतान विवरण",
    uploadTitle: "आपका पत्र",
    lettersAnalyzed: "पत्र का विश्लेषण किया गया",
    lettersAnalyzedPlural: "पत्रों का विश्लेषण किया गया",
    copied: "✅ कॉपी हो गया!",
    actBefore: "इस तिथि से पहले कार्रवाई करें!",
    analysisResult: "विश्लेषण परिणाम",
    brandName: "जर्मन पत्र सहायक",
    daysLeft: "दिन शेष हैं",
    mayNotBeOfficial: "⚠️ आधिकारिक नहीं हो सकता",
    typeMessage: "अपना संदेश लिखें...",
    send: "भेजें",
    translating: "अनुवाद हो रहा है...",
    howToPay: "भुगतान कैसे करें",
    documentsNeeded: "आपको जिन दस्तावेज़ों की आवश्यकता हो सकती है",
    whatHappensIfIgnore: "यदि आप इसे अनदेखा करते हैं तो क्या होता है",
    thingsToBeCareful: "ध्यान देने योग्य बातें",
    analyzeFirst: "📄 चैट शुरू करने के लिए पहले एक पत्र का विश्लेषण करें...",
  },
  French: {
    copy: "📋 Copier",
    pdf: "📄 PDF",
    new: "🔄 Nouveau",
    chatTitle: "💬 Discuter avec l'assistant",
    chatSub: "Posez n'importe quelle question sur cette lettre",
    placeholder: "Posez n'importe quelle question sur cette lettre...",
    suggestions: ["Aide-moi à rédiger une réponse", "Que dois-je faire en premier ?", "Est-ce urgent ?", "Explique en termes plus simples"],
    welcome: "Salut! J'ai lu votre lettre. Demandez-moi n'importe quoi — je garderai les choses simples. 👋",
    aboutTitle: "ℹ️ Assistant de Lettres Allemandes",
    aboutFeatures: "Fonctionnalités: OCR, Chat Intelligent, Assistant de Réponse, Sortie Multilingue",
    aboutPrivacy: "Confidentialité: Vos documents sont traités temporairement et non stockés.",
    aboutDisclaimer: "Avertissement: Ceci est une aide générée par l'IA, pas un conseil juridique.",
    close: "Fermer",
    emptyTitle: "Aucune lettre analysée",
    emptySub: "Collez ou téléchargez une lettre pour voir l'analyse",
    bottomLine: "✨ Conclusion",
    bridgeText: "📖 J'ai lu votre lettre. Quelque chose n'est pas clair ?",
    bridgeAsk: "Demandez ci-dessous ↓",
    urgency: "urgence",
    paymentInvolved: "💳 Paiement inclus",
    quality: "✓ Qualité d'analyse:",
    additionalDetails: "📌 Détails supplémentaires",
    safety: "🛡️",
    back: "← Retour",
    about: "À propos",
    pasteText: "📄 Coller le texte",
    upload: "📑 Télécharger PDF / Image",
    dropText: "Cliquez pour télécharger un PDF ou une image",
    dropSubtext: "ou glisser-déposer",
    analyzeBtn: "✨ Analyser la lettre",
    privacy: "Vos données sont privées — rien n'est stocké",
    processing: "Traitement de votre lettre...",
    accordionWhat: "Ce que vous devez faire",
    accordionPay: "Comment payer",
    accordionDocs: "Documents dont vous pourriez avoir besoin",
    accordionCons: "Ce qui se passe si vous ignorez cela",
    accordionCareful: "Choses à surveiller",
    from: "De",
    whatToDo: "Ce que vous devez faire",
    deadline: "La date limite est",
    consequences: "Conséquences possibles",
    draftReply: "Voici un brouillon de réponse",
    basedOn: "D'après la lettre que j'ai analysée:",
    actionsNeeded: "Actions nécessaires",
    payment: "Détails de paiement",
    uploadTitle: "Votre lettre",
    lettersAnalyzed: "lettre analysée",
    lettersAnalyzedPlural: "lettres analysées",
    copied: "✅ Copié !",
    actBefore: "Assurez-vous d'agir avant cette date!",
    analysisResult: "Résultat de l'analyse",
    brandName: "Assistant de Lettres Allemandes",
    daysLeft: "jours restants pour agir",
    mayNotBeOfficial: "⚠️ Peut ne pas être officiel",
    typeMessage: "Tapez votre message...",
    send: "Envoyer",
    translating: "Traduction...",
    howToPay: "Comment payer",
    documentsNeeded: "Documents dont vous pourriez avoir besoin",
    whatHappensIfIgnore: "Ce qui se passe si vous ignorez cela",
    thingsToBeCareful: "Choses à surveiller",
    analyzeFirst: "📄 Analysez d'abord une lettre pour commencer à discuter...",
  },
  Spanish: {
    copy: "📋 Copiar",
    pdf: "📄 PDF",
    new: "🔄 Nuevo",
    chatTitle: "💬 Chatear con el asistente",
    chatSub: "Pregunta cualquier cosa sobre esta carta",
    placeholder: "Pregunta cualquier cosa sobre esta carta...",
    suggestions: ["Ayúdame a redactar una respuesta", "¿Qué debo hacer primero?", "¿Es urgente?", "Explica en palabras más simples"],
    welcome: "¡Hola! He leído tu carta. Pregúntame cualquier cosa — lo mantendré simple. 👋",
    aboutTitle: "ℹ️ Asistente de Cartas Alemanas",
    aboutFeatures: "Características: OCR, Chat Inteligente, Asistente de Respuesta, Salida Multilingüe",
    aboutPrivacy: "Privacidad: Tus documentos se procesan temporalmente y no se almacenan.",
    aboutDisclaimer: "Descargo de responsabilidad: Esta es ayuda generada por IA, no asesoramiento legal.",
    close: "Cerrar",
    emptyTitle: "Ninguna carta analizada",
    emptySub: "Pega o sube una carta para ver el análisis",
    bottomLine: "✨ Conclusión",
    bridgeText: "📖 He leído tu carta. ¿Algo no está claro?",
    bridgeAsk: "Pregunta abajo ↓",
    urgency: "urgencia",
    paymentInvolved: "💳 Pago incluido",
    quality: "✓ Calidad del análisis:",
    additionalDetails: "📌 Detalles adicionales",
    safety: "🛡️",
    back: "← Volver",
    about: "Acerca de",
    pasteText: "📄 Pegar texto",
    upload: "📑 Subir PDF / Imagen",
    dropText: "Haz clic para subir PDF o imagen",
    dropSubtext: "o arrastrar y soltar",
    analyzeBtn: "✨ Analizar carta",
    privacy: "Tus datos son privados — nada se almacena",
    processing: "Procesando tu carta...",
    accordionWhat: "Qué debes hacer",
    accordionPay: "Cómo pagar",
    accordionDocs: "Documentos que puedas necesitar",
    accordionCons: "Qué pasa si ignoras esto",
    accordionCareful: "Cosas a tener en cuenta",
    from: "De",
    whatToDo: "Qué debes hacer",
    deadline: "La fecha límite es",
    consequences: "Posibles consecuencias",
    draftReply: "Aquí tienes un borrador de respuesta",
    basedOn: "Según la carta que analicé:",
    actionsNeeded: "Acciones necesarias",
    payment: "Detalles de pago",
    uploadTitle: "Tu carta",
    lettersAnalyzed: "carta analizada",
    lettersAnalyzedPlural: "cartas analizadas",
    copied: "✅ ¡Copiado!",
    actBefore: "¡Asegúrate de actuar antes de esta fecha!",
    analysisResult: "Resultado del análisis",
    brandName: "Asistente de Cartas Alemanas",
    daysLeft: "días para actuar",
    mayNotBeOfficial: "⚠️ Puede no ser oficial",
    typeMessage: "Escribe tu mensaje...",
    send: "Enviar",
    translating: "Traduciendo...",
    howToPay: "Cómo pagar",
    documentsNeeded: "Documentos que puedas necesitar",
    whatHappensIfIgnore: "Qué pasa si ignoras esto",
    thingsToBeCareful: "Cosas a tener en cuenta",
    analyzeFirst: "📄 Analiza primero una carta para empezar a chatear...",
  },
  Italian: {
    copy: "📋 Copia",
    pdf: "📄 PDF",
    new: "🔄 Nuovo",
    chatTitle: "💬 Chat con Assistente",
    chatSub: "Chiedi qualsiasi cosa su questa lettera",
    placeholder: "Chiedi qualsiasi cosa su questa lettera...",
    suggestions: ["Aiutami a scrivere una bozza di risposta", "Cosa dovrei fare prima?", "È urgente?", "Spiega in parole più semplici"],
    welcome: "Ciao! Ho letto la tua lettera. Chiedimi qualsiasi cosa — la terrò semplice. 👋",
    aboutTitle: "ℹ️ Assistente Lettere Tedesche",
    aboutFeatures: "Funzionalità: OCR, Chat Intelligente, Assistente Bozze, Output Multilingue",
    aboutPrivacy: "Privacy: I tuoi documenti vengono elaborati temporaneamente e non vengono conservati.",
    aboutDisclaimer: "Disclaimer: Questo è un aiuto generato dall'IA, non un consiglio legale.",
    close: "Chiudi",
    emptyTitle: "Nessuna lettera analizzata",
    emptySub: "Incolla o carica una lettera per vedere l'analisi",
    bottomLine: "✨ In conclusione",
    bridgeText: "📖 Ho letto la tua lettera. Qualcosa non è chiaro?",
    bridgeAsk: "Chiedi qui sotto ↓",
    urgency: "urgenza",
    paymentInvolved: "💳 Pagamento incluso",
    quality: "✓ Qualità dell'analisi:",
    additionalDetails: "📌 Dettagli aggiuntivi",
    safety: "🛡️",
    back: "← Indietro",
    about: "Informazioni",
    pasteText: "📄 Incolla Testo",
    upload: "📑 Carica PDF / Immagine",
    dropText: "Clicca per caricare PDF o immagine",
    dropSubtext: "o trascina e rilascia",
    analyzeBtn: "✨ Analizza Lettera",
    privacy: "I tuoi dati sono privati — nulla viene conservato",
    processing: "Elaborazione della tua lettera...",
    accordionWhat: "Cosa fare",
    accordionPay: "Come pagare",
    accordionDocs: "Documenti che potrebbero servirti",
    accordionCons: "Cosa succede se ignori questo",
    accordionCareful: "Cose a cui prestare attenzione",
    from: "Da",
    whatToDo: "Cosa devi fare",
    deadline: "La scadenza è",
    consequences: "Possibili conseguenze",
    draftReply: "Ecco una bozza di risposta",
    basedOn: "In base alla lettera che ho analizzato:",
    actionsNeeded: "Azioni necessarie",
    payment: "Dettagli di pagamento",
    uploadTitle: "La tua lettera",
    lettersAnalyzed: "lettera analizzata",
    lettersAnalyzedPlural: "lettere analizzate",
    copied: "✅ Copiato!",
    actBefore: "Assicurati di agire prima di questa data!",
    analysisResult: "Risultato dell'Analisi",
    brandName: "Assistente Lettere Tedesche",
    daysLeft: "giorni per agire",
    mayNotBeOfficial: "⚠️ Potrebbe non essere ufficiale",
    typeMessage: "Scrivi il tuo messaggio...",
    send: "Invia",
    translating: "Traduzione in corso...",
    howToPay: "Come pagare",
    documentsNeeded: "Documenti che potrebbero servirti",
    whatHappensIfIgnore: "Cosa succede se ignori questo",
    thingsToBeCareful: "Cose a cui prestare attenzione",
    analyzeFirst: "📄 Analizza prima una lettera per iniziare a chattare...",
  },
  Portuguese: {
    copy: "📋 Copiar",
    pdf: "📄 PDF",
    new: "🔄 Novo",
    chatTitle: "💬 Conversar com Assistente",
    chatSub: "Pergunte qualquer coisa sobre esta carta",
    placeholder: "Pergunte qualquer coisa sobre esta carta...",
    suggestions: ["Ajude-me a redigir uma resposta", "O que devo fazer primeiro?", "Isto é urgente?", "Explique em palavras mais simples"],
    welcome: "Olá! Li sua carta. Pergunte-me qualquer coisa — vou manter as coisas simples. 👋",
    aboutTitle: "ℹ️ Assistente de Cartas Alemãs",
    aboutFeatures: "Funcionalidades: OCR, Chat Inteligente, Assistente de Resposta, Saída Multilíngue",
    aboutPrivacy: "Privacidade: Seus documentos são processados temporariamente e não são armazenados.",
    aboutDisclaimer: "Aviso: Esta é uma ajuda gerada por IA, não um conselho jurídico.",
    close: "Fechar",
    emptyTitle: "Nenhuma carta analisada",
    emptySub: "Cole ou envie uma carta para ver a análise",
    bottomLine: "✨ Conclusão",
    bridgeText: "📖 Li sua carta. Algo não está claro?",
    bridgeAsk: "Pergunte abaixo ↓",
    urgency: "urgência",
    paymentInvolved: "💳 Pagamento envolvido",
    quality: "✓ Qualidade da Análise:",
    additionalDetails: "📌 Detalhes adicionais",
    safety: "🛡️",
    back: "← Voltar",
    about: "Sobre",
    pasteText: "📄 Colar Texto",
    upload: "📑 Enviar PDF / Imagem",
    dropText: "Clique para enviar PDF ou imagem",
    dropSubtext: "ou arraste e solte",
    analyzeBtn: "✨ Analisar Carta",
    privacy: "Seus dados são privados — nada é armazenado",
    processing: "Processando sua carta...",
    accordionWhat: "O que fazer",
    accordionPay: "Como pagar",
    accordionDocs: "Documentos que você pode precisar",
    accordionCons: "O que acontece se você ignorar isso",
    accordionCareful: "Coisas às quais prestar atenção",
    from: "De",
    whatToDo: "O que você precisa fazer",
    deadline: "O prazo é",
    consequences: "Possíveis consequências",
    draftReply: "Aqui está um rascunho de resposta",
    basedOn: "Com base na carta que analisei:",
    actionsNeeded: "Ações necessárias",
    payment: "Detalhes de pagamento",
    uploadTitle: "Sua carta",
    lettersAnalyzed: "carta analisada",
    lettersAnalyzedPlural: "cartas analisadas",
    copied: "✅ Copiado!",
    actBefore: "Certifique-se de agir antes desta data!",
    analysisResult: "Resultado da Análise",
    brandName: "Assistente de Cartas Alemãs",
    daysLeft: "dias para agir",
    mayNotBeOfficial: "⚠️ Pode não ser oficial",
    typeMessage: "Digite sua mensagem...",
    send: "Enviar",
    translating: "Traduzindo...",
    howToPay: "Como pagar",
    documentsNeeded: "Documentos que você pode precisar",
    whatHappensIfIgnore: "O que acontece se você ignorar isso",
    thingsToBeCareful: "Coisas às quais prestar atenção",
    analyzeFirst: "📄 Analise primeiro uma carta para começar a conversar...",
  },
  Dutch: {
    copy: "📋 Kopiëren",
    pdf: "📄 PDF",
    new: "🔄 Nieuw",
    chatTitle: "💬 Chat met Assistent",
    chatSub: "Vraag alles over deze brief",
    placeholder: "Vraag alles over deze brief...",
    suggestions: ["Help me een antwoord op te stellen", "Wat moet ik eerst doen?", "Is dit dringend?", "In eenvoudigere woorden uitleggen"],
    welcome: "Hallo! Ik heb je brief gelezen. Vraag me alles — ik hou het simpel. 👋",
    aboutTitle: "ℹ️ Duitse Brievenassistent",
    aboutFeatures: "Functies: OCR, Slimme Chat, Antwoordassistent, Meertalige Uitvoer",
    aboutPrivacy: "Privacy: Uw documenten worden tijdelijk verwerkt en niet opgeslagen.",
    aboutDisclaimer: "Disclaimer: Dit is AI-gegenereerde hulp, geen juridisch advies.",
    close: "Sluiten",
    emptyTitle: "Nog geen brief geanalyseerd",
    emptySub: "Plak of upload een brief om analyse te zien",
    bottomLine: "✨ Conclusie",
    bridgeText: "📖 Ik heb je brief gelezen. Iets onduidelijk?",
    bridgeAsk: "Vraag hieronder ↓",
    urgency: "dringendheid",
    paymentInvolved: "💳 Betaling inbegrepen",
    quality: "✓ Analyse Kwaliteit:",
    additionalDetails: "📌 Extra details",
    safety: "🛡️",
    back: "← Terug",
    about: "Over",
    pasteText: "📄 Tekst Plakken",
    upload: "📑 PDF / Afbeelding Uploaden",
    dropText: "Klik om PDF of afbeelding te uploaden",
    dropSubtext: "of sleep en laat vallen",
    analyzeBtn: "✨ Brief Analyseren",
    privacy: "Uw gegevens zijn privé — niets wordt opgeslagen",
    processing: "Uw brief wordt verwerkt...",
    accordionWhat: "Wat te doen",
    accordionPay: "Hoe te betalen",
    accordionDocs: "Documenten die u nodig heeft",
    accordionCons: "Wat gebeurt er als u dit negeert",
    accordionCareful: "Dingen om op te letten",
    from: "Van",
    whatToDo: "Wat u moet doen",
    deadline: "De deadline is",
    consequences: "Mogelijke gevolgen",
    draftReply: "Hier is een conceptantwoord",
    basedOn: "Op basis van de brief die ik heb geanalyseerd:",
    actionsNeeded: "Vereiste acties",
    payment: "Betalingsdetails",
    uploadTitle: "Uw brief",
    lettersAnalyzed: "brief geanalyseerd",
    lettersAnalyzedPlural: "brieven geanalyseerd",
    copied: "✅ Gekopieerd!",
    actBefore: "Zorg ervoor dat u voor deze datum handelt!",
    analysisResult: "Analyse Resultaat",
    brandName: "Duitse Brievenassistent",
    daysLeft: "dagen om te handelen",
    mayNotBeOfficial: "⚠️ Mogelijk niet officieel",
    typeMessage: "Typ uw bericht...",
    send: "Versturen",
    translating: "Vertalen...",
    howToPay: "Hoe te betalen",
    documentsNeeded: "Documenten die u nodig heeft",
    whatHappensIfIgnore: "Wat gebeurt er als u dit negeert",
    thingsToBeCareful: "Dingen om op te letten",
    analyzeFirst: "📄 Analyseer eerst een brief om te beginnen met chatten...",
  },
  Polish: {
    copy: "📋 Kopiuj",
    pdf: "📄 PDF",
    new: "🔄 Nowy",
    chatTitle: "💬 Czat z Asystentem",
    chatSub: "Zapytaj o wszystko dotyczące tego listu",
    placeholder: "Zapytaj o wszystko dotyczące tego listu...",
    suggestions: ["Pomóż mi przygotować odpowiedź", "Co powinienem zrobić najpierw?", "Czy to pilne?", "Wyjaśnij prostszymi słowami"],
    welcome: "Cześć! Przeczytałem twój list. Zapytaj mnie o wszystko — zachowam to prosto. 👋",
    aboutTitle: "ℹ️ Asystent Listów Niemieckich",
    aboutFeatures: "Funkcje: OCR, Inteligentny Czat, Asystent Odpowiedzi, Wielojęzyczne Wyjście",
    aboutPrivacy: "Prywatność: Twoje dokumenty są przetwarzane tymczasowo i nie są przechowywane.",
    aboutDisclaimer: "Zastrzeżenie: To pomoc generowana przez AI, nie porada prawna.",
    close: "Zamknij",
    emptyTitle: "Nie przeanalizowano jeszcze żadnego listu",
    emptySub: "Wklej lub prześlij list, aby zobaczyć analizę",
    bottomLine: "✨ Podsumowanie",
    bridgeText: "📖 Przeczytałem twój list. Coś jest niejasne?",
    bridgeAsk: "Zapytaj poniżej ↓",
    urgency: "pilność",
    paymentInvolved: "💳 Płatność wliczona",
    quality: "✓ Jakość Analizy:",
    additionalDetails: "📌 Dodatkowe szczegóły",
    safety: "🛡️",
    back: "← Wróć",
    about: "O aplikacji",
    pasteText: "📄 Wklej Tekst",
    upload: "📑 Prześlij PDF / Obraz",
    dropText: "Kliknij, aby przesłać PDF lub obraz",
    dropSubtext: "lub przeciągnij i upuść",
    analyzeBtn: "✨ Analizuj List",
    privacy: "Twoje dane są prywatne — nic nie jest przechowywane",
    processing: "Przetwarzanie twojego listu...",
    accordionWhat: "Co robić",
    accordionPay: "Jak zapłacić",
    accordionDocs: "Dokumenty, których możesz potrzebować",
    accordionCons: "Co się stanie, jeśli to zignorujesz",
    accordionCareful: "Rzeczy, na które należy uważać",
    from: "Od",
    whatToDo: "Co musisz zrobić",
    deadline: "Termin to",
    consequences: "Możliwe konsekwencje",
    draftReply: "Oto projekt odpowiedzi",
    basedOn: "Na podstawie listu, który przeanalizowałem:",
    actionsNeeded: "Wymagane działania",
    payment: "Szczegóły płatności",
    uploadTitle: "Twój list",
    lettersAnalyzed: "list przeanalizowany",
    lettersAnalyzedPlural: "listy przeanalizowane",
    copied: "✅ Skopiowano!",
    actBefore: "Upewnij się, że działasz przed tą datą!",
    analysisResult: "Wynik Analizy",
    brandName: "Asystent Listów Niemieckich",
    daysLeft: "dni na działanie",
    mayNotBeOfficial: "⚠️ Może nie być oficjalny",
    typeMessage: "Wpisz swoją wiadomość...",
    send: "Wyślij",
    translating: "Tłumaczenie...",
    howToPay: "Jak zapłacić",
    documentsNeeded: "Dokumenty, których możesz potrzebować",
    whatHappensIfIgnore: "Co się stanie, jeśli to zignorujesz",
    thingsToBeCareful: "Rzeczy, na które należy uważać",
    analyzeFirst: "📄 Najpierw przeanalizuj list, aby rozpocząć czat...",
  },
  Russian: {
    copy: "📋 Копировать",
    pdf: "📄 PDF",
    new: "🔄 Новый",
    chatTitle: "💬 Чат с Ассистентом",
    chatSub: "Спросите что угодно об этом письме",
    placeholder: "Спросите что угодно об этом письме...",
    suggestions: ["Помогите мне подготовить ответ", "Что мне делать в первую очередь?", "Это срочно?", "Объясните более простыми словами"],
    welcome: "Привет! Я прочитал ваше письмо. Спросите меня о чем угодно — я буду прост. 👋",
    aboutTitle: "ℹ️ Помощник по Немецким Письмам",
    aboutFeatures: "Функции: OCR, Умный Чат, Помощник по Ответам, Многоязычный Вывод",
    aboutPrivacy: "Конфиденциальность: Ваши документы обрабатываются временно и не сохраняются.",
    aboutDisclaimer: "Отказ от ответственности: Это помощь на основе ИИ, а не юридическая консультация.",
    close: "Закрыть",
    emptyTitle: "Письмо еще не проанализировано",
    emptySub: "Вставьте или загрузите письмо, чтобы увидеть анализ",
    bottomLine: "✨ Суть",
    bridgeText: "📖 Я прочитал ваше письмо. Что-то неясно?",
    bridgeAsk: "Спросите ниже ↓",
    urgency: "срочность",
    paymentInvolved: "💳 Включает оплату",
    quality: "✓ Качество Анализа:",
    additionalDetails: "📌 Дополнительные детали",
    safety: "🛡️",
    back: "← Назад",
    about: "О приложении",
    pasteText: "📄 Вставить Текст",
    upload: "📑 Загрузить PDF / Изображение",
    dropText: "Нажмите, чтобы загрузить PDF или изображение",
    dropSubtext: "или перетащите",
    analyzeBtn: "✨ Анализировать Письмо",
    privacy: "Ваши данные приватны — ничего не сохраняется",
    processing: "Обработка вашего письма...",
    accordionWhat: "Что делать",
    accordionPay: "Как оплатить",
    accordionDocs: "Необходимые документы",
    accordionCons: "Что будет, если проигнорировать",
    accordionCareful: "На что обратить внимание",
    from: "От",
    whatToDo: "Что вам нужно сделать",
    deadline: "Срок",
    consequences: "Возможные последствия",
    draftReply: "Вот проект ответа",
    basedOn: "На основе проанализированного письма:",
    actionsNeeded: "Необходимые действия",
    payment: "Детали оплаты",
    uploadTitle: "Ваше письмо",
    lettersAnalyzed: "письмо проанализировано",
    lettersAnalyzedPlural: "писем проанализировано",
    copied: "✅ Скопировано!",
    actBefore: "Убедитесь, что вы действуете до этой даты!",
    analysisResult: "Результат Анализа",
    brandName: "Помощник по Немецким Письмам",
    daysLeft: "дней для действий",
    mayNotBeOfficial: "⚠️ Может быть неофициальным",
    typeMessage: "Введите ваше сообщение...",
    send: "Отправить",
    translating: "Перевод...",
    howToPay: "Как оплатить",
    documentsNeeded: "Необходимые документы",
    whatHappensIfIgnore: "Что будет, если проигнорировать",
    thingsToBeCareful: "На что обратить внимание",
    analyzeFirst: "📄 Сначала проанализируйте письмо, чтобы начать чат...",
  },
  Japanese: {
    copy: "📋 コピー",
    pdf: "📄 PDF",
    new: "🔄 新規",
    chatTitle: "💬 アシスタントとチャット",
    chatSub: "この手紙について何でも質問してください",
    placeholder: "この手紙について何でも質問してください...",
    suggestions: ["返信の下書きを作成するのを手伝って", "最初に何をすればいいですか？", "これは緊急ですか？", "より簡単な言葉で説明して"],
    welcome: "こんにちは！あなたの手紙を読みました。何でも質問してください — シンプルに説明します。👋",
    aboutTitle: "ℹ️ ドイツ語手紙アシスタント",
    aboutFeatures: "機能: OCR、スマートチャット、返信下書きアシスタント、多言語出力",
    aboutPrivacy: "プライバシー: あなたの書類は一時的に処理され、保存されません。",
    aboutDisclaimer: "免責事項: これはAIによる支援であり、法的助言ではありません。",
    close: "閉じる",
    emptyTitle: "まだ手紙が分析されていません",
    emptySub: "分析を見るには手紙を貼り付けるかアップロードしてください",
    bottomLine: "✨ 結論",
    bridgeText: "📖 あなたの手紙を読みました。不明な点はありますか？",
    bridgeAsk: "下記で質問してください ↓",
    urgency: "緊急性",
    paymentInvolved: "💳 支払いあり",
    quality: "✓ 分析品質:",
    additionalDetails: "📌 追加詳細",
    safety: "🛡️",
    back: "← 戻る",
    about: "について",
    pasteText: "📄 テキストを貼り付け",
    upload: "📑 PDF / 画像をアップロード",
    dropText: "クリックしてPDFまたは画像をアップロード",
    dropSubtext: "またはドラッグ＆ドロップ",
    analyzeBtn: "✨ 手紙を分析",
    privacy: "あなたのデータはプライベート — 何も保存されません",
    processing: "手紙を処理中...",
    accordionWhat: "何をすべきか",
    accordionPay: "支払い方法",
    accordionDocs: "必要な書類",
    accordionCons: "無視した場合の結果",
    accordionCareful: "注意すべき点",
    from: "差出人",
    whatToDo: "あなたがすべきこと",
    deadline: "期限は",
    consequences: "考えられる結果",
    draftReply: "返信の下書きはこちら",
    basedOn: "分析した手紙に基づいて:",
    actionsNeeded: "必要なアクション",
    payment: "支払い詳細",
    uploadTitle: "あなたの手紙",
    lettersAnalyzed: "手紙を分析",
    lettersAnalyzedPlural: "手紙を分析",
    copied: "✅ コピーしました！",
    actBefore: "この日付より前に行動してください！",
    analysisResult: "分析結果",
    brandName: "ドイツ語手紙アシスタント",
    daysLeft: "残り日数",
    mayNotBeOfficial: "⚠️ 公式でない可能性があります",
    typeMessage: "メッセージを入力...",
    send: "送信",
    translating: "翻訳中...",
    howToPay: "支払い方法",
    documentsNeeded: "必要な書類",
    whatHappensIfIgnore: "無視した場合の結果",
    thingsToBeCareful: "注意すべき点",
    analyzeFirst: "📄 チャットを始めるにはまず手紙を分析してください...",
  },
  Korean: {
    copy: "📋 복사",
    pdf: "📄 PDF",
    new: "🔄 새로 만들기",
    chatTitle: "💬 어시스턴트와 채팅",
    chatSub: "이 편지에 대해 무엇이든 물어보세요",
    placeholder: "이 편지에 대해 무엇이든 물어보세요...",
    suggestions: ["답변 초안 작성 도움", "먼저 무엇을 해야 하나요?", "긴급한가요?", "더 간단한 단어로 설명해 주세요"],
    welcome: "안녕하세요! 편지를 읽었습니다. 무엇이든 물어보세요 — 간단하게 설명해 드리겠습니다. 👋",
    aboutTitle: "ℹ️ 독일어 편지 어시스턴트",
    aboutFeatures: "기능: OCR, 스마트 채팅, 답변 초안 도우미, 다국어 출력",
    aboutPrivacy: "개인정보: 문서는 일시적으로 처리되며 저장되지 않습니다.",
    aboutDisclaimer: "면책 조항: 이는 AI 생성 도움말이며 법률 조언이 아닙니다.",
    close: "닫기",
    emptyTitle: "아직 분석된 편지가 없습니다",
    emptySub: "분석을 보려면 편지를 붙여넣거나 업로드하세요",
    bottomLine: "✨ 결론",
    bridgeText: "📖 편지를 읽었습니다. 불명확한 점이 있나요?",
    bridgeAsk: "아래에 질문하세요 ↓",
    urgency: "긴급성",
    paymentInvolved: "💳 결제 포함",
    quality: "✓ 분석 품질:",
    additionalDetails: "📌 추가 세부사항",
    safety: "🛡️",
    back: "← 뒤로",
    about: "정보",
    pasteText: "📄 텍스트 붙여넣기",
    upload: "📑 PDF / 이미지 업로드",
    dropText: "클릭하여 PDF 또는 이미지 업로드",
    dropSubtext: "또는 드래그 앤 드롭",
    analyzeBtn: "✨ 편지 분석",
    privacy: "데이터는 비공개 — 아무것도 저장되지 않음",
    processing: "편지를 처리 중...",
    accordionWhat: "해야 할 일",
    accordionPay: "결제 방법",
    accordionDocs: "필요한 서류",
    accordionCons: "무시할 경우 발생하는 일",
    accordionCareful: "주의해야 할 사항",
    from: "보낸 사람",
    whatToDo: "해야 할 일",
    deadline: "마감일",
    consequences: "가능한 결과",
    draftReply: "답변 초안입니다",
    basedOn: "분석한 편지를 기반으로:",
    actionsNeeded: "필요한 조치",
    payment: "결제 세부사항",
    uploadTitle: "귀하의 편지",
    lettersAnalyzed: "편지 분석됨",
    lettersAnalyzedPlural: "편지 분석됨",
    copied: "✅ 복사됨!",
    actBefore: "이 날짜 이전에 조치하세요!",
    analysisResult: "분석 결과",
    brandName: "독일어 편지 어시스턴트",
    daysLeft: "남은 일수",
    mayNotBeOfficial: "⚠️ 공식적이지 않을 수 있음",
    typeMessage: "메시지를 입력하세요...",
    send: "보내기",
    translating: "번역 중...",
    howToPay: "결제 방법",
    documentsNeeded: "필요한 서류",
    whatHappensIfIgnore: "무시할 경우 발생하는 일",
    thingsToBeCareful: "주의해야 할 사항",
    analyzeFirst: "📄 채팅을 시작하려면 먼저 편지를 분석하세요...",
  },
  Chinese: {
    copy: "📋 复制",
    pdf: "📄 PDF",
    new: "🔄 新建",
    chatTitle: "💬 与助手聊天",
    chatSub: "询问关于这封信的任何问题",
    placeholder: "询问关于这封信的任何问题...",
    suggestions: ["帮我起草回复", "我应该先做什么？", "这紧急吗？", "用更简单的词语解释"],
    welcome: "你好！我已经读了你的信。问我任何问题 — 我会保持简单。👋",
    aboutTitle: "ℹ️ 德语信件助手",
    aboutFeatures: "功能: OCR、智能聊天、回复草稿助手、多语言输出",
    aboutPrivacy: "隐私: 您的文档会临时处理，不会被存储。",
    aboutDisclaimer: "免责声明: 这是AI生成的帮助，不是法律建议。",
    close: "关闭",
    emptyTitle: "尚未分析任何信件",
    emptySub: "粘贴或上传信件以查看分析",
    bottomLine: "✨ 总结",
    bridgeText: "📖 我已经读了你的信。有什么不清楚的吗？",
    bridgeAsk: "在下面提问 ↓",
    urgency: "紧急性",
    paymentInvolved: "💳 涉及付款",
    quality: "✓ 分析质量:",
    additionalDetails: "📌 额外细节",
    safety: "🛡️",
    back: "← 返回",
    about: "关于",
    pasteText: "📄 粘贴文本",
    upload: "📑 上传 PDF / 图片",
    dropText: "点击上传PDF或图片",
    dropSubtext: "或拖拽放置",
    analyzeBtn: "✨ 分析信件",
    privacy: "您的数据是私密的 — 不会存储任何内容",
    processing: "正在处理您的信件...",
    accordionWhat: "该做什么",
    accordionPay: "如何付款",
    accordionDocs: "您可能需要的文件",
    accordionCons: "如果您忽略此信的后果",
    accordionCareful: "需要注意的事项",
    from: "来自",
    whatToDo: "您需要做什么",
    deadline: "截止日期是",
    consequences: "可能的后果",
    draftReply: "这是回复草稿",
    basedOn: "根据我分析的信件:",
    actionsNeeded: "需要的行动",
    payment: "付款详情",
    uploadTitle: "您的信件",
    lettersAnalyzed: "信件已分析",
    lettersAnalyzedPlural: "信件已分析",
    copied: "✅ 已复制！",
    actBefore: "请确保在此日期之前采取行动！",
    analysisResult: "分析结果",
    brandName: "德语信件助手",
    daysLeft: "剩余天数",
    mayNotBeOfficial: "⚠️ 可能不是官方的",
    typeMessage: "输入您的消息...",
    send: "发送",
    translating: "翻译中...",
    howToPay: "如何付款",
    documentsNeeded: "您可能需要的文件",
    whatHappensIfIgnore: "如果您忽略此信的后果",
    thingsToBeCareful: "需要注意的事项",
    analyzeFirst: "📄 请先分析一封信件以开始聊天...",
  },
};

// ========== LANGUAGE NAMES WITH FLAG EMOJIS ==========
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

export default function Dashboard({ onBack }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("text");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [originalResult, setOriginalResult] = useState(null);
  const [animatedSummary, setAnimatedSummary] = useState("");
  const [activeAccordion, setActiveAccordion] = useState("whatToDo");
  const [showAbout, setShowAbout] = useState(false);
  const [copied, setCopied] = useState(false);
  const [outputLanguage, setOutputLanguage] = useState("English");
  const [sessionLetterCount, setSessionLetterCount] = useState(0);
  const [darkMode, setDarkMode] = useState(false);
  const [translationCache, setTranslationCache] = useState({});
  const [isTranslating, setIsTranslating] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    { role: "assistant", content: UI_LABELS.English.welcome }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState("");
  const [replyOptions, setReplyOptions] = useState(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatError, setChatError] = useState(null);

  const typewriterRef = useRef(null);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const labels = UI_LABELS[outputLanguage] || UI_LABELS.English;

  useEffect(() => {
    const saved = localStorage.getItem("darkMode");
    if (saved === "true") setDarkMode(true);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, streamingMessage]);

  // ========== INSTANT LANGUAGE SWITCHING - ALL FIELDS ==========
  useEffect(() => {
    const updateContent = async () => {
      // Update analysis results (all fields)
      if (originalResult) {
        if (outputLanguage === "English") {
          setResult(originalResult);
          setAnimatedSummary(originalResult?.tldr || "");
        } else {
          const cacheKey = `${JSON.stringify(originalResult)}_${outputLanguage}`;
          if (translationCache[cacheKey]) {
            const cached = translationCache[cacheKey];
            setResult(cached);
            setAnimatedSummary(cached?.tldr || "");
          } else {
            await translateResults(originalResult, outputLanguage);
          }
        }
      }
      
      // Update chat welcome message
      const newWelcome = labels.welcome;
      setChatMessages(prev => {
        const newMessages = [...prev];
        if (newMessages.length > 0 && newMessages[0].role === "assistant") {
          const isWelcome = newMessages[0].content === UI_LABELS.English.welcome || 
                           Object.values(UI_LABELS).some(l => l.welcome === newMessages[0].content);
          if (isWelcome) {
            newMessages[0] = { ...newMessages[0], content: newWelcome };
          }
        }
        return newMessages;
      });
    };

    updateContent();
  }, [outputLanguage]);

  // ========== UPDATED: translateResults with caching for instant switching ==========
  const translateResults = async (data, targetLang) => {
    if (isTranslating) return;
    
    // ✅ Check cache first - INSTANT if already translated
    const cacheKey = `${JSON.stringify(data)}_${targetLang}`;
    if (translationCache[cacheKey]) {
      const cached = translationCache[cacheKey];
      setResult(cached);
      setAnimatedSummary(cached?.tldr || "");
      return; // ✅ Instant return from cache - NO API call!
    }
    
    setIsTranslating(true);
    
    try {
      console.log(`🔄 Translating to: ${targetLang} (batch)`);
      const response = await fetch(`${API_URL}/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          analysis: data,
          output_language: targetLang
        })
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Translation failed:', errorText);
        throw new Error("Translation failed");
      }
      
      const translated = await response.json();
      console.log(`✅ Translation complete for: ${targetLang}`);
      
      // ✅ Cache the result for instant future switching
      setTranslationCache(prev => ({ ...prev, [cacheKey]: translated }));
      setResult(translated);
      setAnimatedSummary(translated?.tldr || "");
      
    } catch (err) {
      console.error("Translation error:", err);
      setResult(originalResult);
      setAnimatedSummary(originalResult?.tldr || "");
    } finally {
      setIsTranslating(false);
    }
  };

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

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    localStorage.setItem("darkMode", !darkMode);
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
        <h1 style="color: #7c3aed;">${labels.brandName}</h1>
        <p style="color: #6b7280;">${labels.analysisResult} - ${new Date().toLocaleString()}</p>
      </div>
      
      <div style="background: #fefce8; border: 1px solid #fef08a; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="color: #ca8a04; margin: 0 0 8px 0;">${labels.bottomLine}</h3>
        <p style="font-size: 16px; font-weight: 600; margin: 0;">"${result.tldr || "No summary available"}"</p>
        <p style="font-size: 12px; color: #6b7280; margin-top: 8px;">${labels.bridgeText}</p>
      </div>
      
      <div style="margin-bottom: 16px;">
        <p><strong>${labels.from}:</strong> ${result.sender || "Unknown"}</p>
        <p><strong>${labels.urgency}:</strong> ${result.urgency_level || "Medium"}</p>
        <p><strong>${labels.quality}</strong> ${result.confidence_level || "Medium"}</p>
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">${labels.accordionWhat}</h3>
        ${(result.required_actions || []).map((action, i) => `<p style="margin: 8px 0;">${i+1}. ${action}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">${labels.accordionPay}</h3>
        ${(result.payment_information || []).map(p => `<p style="margin: 8px 0;">• ${p}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">${labels.accordionDocs}</h3>
        ${(result.required_documents || []).map(d => `<p style="margin: 8px 0;">• ${d}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f8fafc; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">${labels.accordionCons}</h3>
        ${(result.possible_consequences || []).map(c => `<p style="margin: 8px 0;">• ${c}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f3e8ff; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
        <h3 style="margin: 0 0 12px 0;">${labels.additionalDetails}</h3>
        ${(result.useful_details || []).map(u => `<p style="margin: 8px 0;">• ${u}</p>`).join('') || "<p>None</p>"}
      </div>
      
      <div style="background: #f0fdf4; border-radius: 12px; padding: 12px; margin-top: 16px; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #166534;">${labels.safety} ${result.safety_note || "This is AI-generated help, not legal advice."}</p>
      </div>
      
      <div style="text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #e5e7eb; font-size: 10px; color: #9ca3af;">
        ${labels.brandName}
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
    if (mode === "text" && !text.trim()) {
      alert("Please paste your letter text");
      return;
    }
    if (mode === "pdf" && !file) {
      alert("Please upload a PDF or image file");
      return;
    }

    setLoading(true);
    setResult(null);
    setOriginalResult(null);
    setAnimatedSummary("");
    setChatError(null);
    const welcomeMsg = labels.welcome;
    setChatMessages([{ role: "assistant", content: welcomeMsg }]);

    try {
      let response;
      if (mode === "text") {
        response = await fetch(`${API_URL}/analyze-text`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            letter_text: text,
            output_language: outputLanguage
          }),
        });
      } else {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("output_language", outputLanguage);
        response = await fetch(`${API_URL}/analyze-pdf`, {
          method: "POST",
          body: formData,
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Backend error");
      }
      
      const data = await response.json();
      
      if (data.is_valid_letter === false) {
        const invalidMessage = data.message || "This doesn't look like an official German letter.";
        setChatMessages([{ role: "assistant", content: invalidMessage }]);
        setLoading(false);
        return;
      }
      
      setOriginalResult(data);
      setResult(data);
      startTypewriter(data.tldr || data.summary || "No summary available");
      setSessionLetterCount(prev => prev + 1);
    } catch (err) {
      console.error(err);
      alert("Backend connection failed. Make sure the server is running.");
    } finally {
      setLoading(false);
    }
  };

  const generateReplyDraft = async (intent) => {
    if (!result) return;
    
    setIsStreaming(true);
    setStreamingMessage("Generating reply draft...");
    setChatError(null);

    try {
      const requestBody = {
        analysis: result,
        intent: intent,
        output_language: outputLanguage,
      };

      const response = await fetch(`${API_URL}/reply-draft`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to generate reply draft");
      }

      const data = await response.json();
      
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        content: data.reply || "Here's your reply draft."
      }]);
      
    } catch (err) {
      console.error("Reply draft error:", err);
      setChatError(err.message || "Failed to generate reply draft. Please try again.");
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        content: `❌ ${err.message || "Failed to generate reply draft. Please try again."}`
      }]);
    } finally {
      setIsStreaming(false);
      setStreamingMessage("");
    }
  };

  // ========== UPDATED: sendChatMessage with letter check ==========
  const sendChatMessage = async () => {
    // ✅ Check if a letter has been analyzed
    if (!result) {
      setChatError("Please analyze a letter first.");
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        content: "⚠️ Please upload or paste a letter and click 'Analyze Letter' first before asking questions."
      }]);
      return;
    }
    
    if (!chatInput.trim() || isStreaming) return;
    
    const userMessage = chatInput;
    setChatInput("");
    setChatError(null);
    
    const messagesHistory = chatMessages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
    messagesHistory.push({ role: "user", content: userMessage });
    
    setChatMessages(prev => [...prev, { role: "user", content: userMessage }]);
    
    setIsStreaming(true);
    setStreamingMessage("");
    setReplyOptions(null);
    
    try {
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
        safety_note: result?.safety_note || "This is AI-generated help, not legal advice.",
      };

      const requestBody = {
        letter_text: result?.letter_text || text || "",
        analysis: analysisData,
        messages: messagesHistory,
        output_language: outputLanguage,
      };

      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Backend error: ${response.status}`);
      }
      
      const contentType = response.headers.get("content-type") || "";
      
      if (contentType.includes("application/json")) {
        const data = await response.json();
        setIsStreaming(false);
        
        if (data.reply) {
          setChatMessages(prev => [...prev, { role: "assistant", content: data.reply }]);
        } else if (data.ui_action === "show_reply_options" && data.options) {
          setChatMessages(prev => [...prev, { 
            role: "assistant", 
            content: data.reply || "How would you like me to write the reply?",
            isOptions: true,
            options: data.options
          }]);
        } else {
          const errorMsg = "I couldn't process your request. Please try again.";
          setChatMessages(prev => [...prev, { role: "assistant", content: `❌ ${errorMsg}` }]);
          setChatError(errorMsg);
        }
        return;
      }
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = "";
      let buffer = "";
      let isDone = false;
      
      while (!isDone) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";
        
        for (const line of lines) {
          const trimmedLine = line.trim();
          if (!trimmedLine) continue;
          
          if (trimmedLine.startsWith("data: ")) {
            try {
              const jsonStr = trimmedLine.substring(6);
              const data = JSON.parse(jsonStr);
              
              if (data.type === "token" && data.content) {
                fullResponse += data.content;
                setStreamingMessage(fullResponse);
              } else if (data.type === "reply_options") {
                setReplyOptions(data.options);
              } else if (data.type === "done") {
                isDone = true;
              } else if (data.type === "error") {
                throw new Error(data.message || "An error occurred during chat");
              } else if (data.reply) {
                fullResponse += data.reply;
                setStreamingMessage(fullResponse);
              }
            } catch (e) {
              if (trimmedLine.length > 10) {
                console.warn("Could not parse SSE data:", trimmedLine);
              }
            }
          }
        }
      }
      
      setIsStreaming(false);
      
      if (fullResponse) {
        setChatMessages(prev => [...prev, { role: "assistant", content: fullResponse }]);
      } else if (replyOptions && replyOptions.length > 0) {
        setChatMessages(prev => [...prev, { 
          role: "assistant", 
          content: "How would you like me to write the reply?",
          isOptions: true,
          options: replyOptions
        }]);
      } else {
        const errorMsg = "I couldn't process your request. Please try again.";
        setChatMessages(prev => [...prev, { role: "assistant", content: `❌ ${errorMsg}` }]);
        setChatError(errorMsg);
      }
      
    } catch (err) {
      console.error("Chat error:", err);
      setIsStreaming(false);
      
      const errorMsg = err.message || "Something went wrong. Please try again.";
      setChatError(errorMsg);
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        content: `❌ ${errorMsg}`
      }]);
    } finally {
      setIsStreaming(false);
      setStreamingMessage("");
    }
  };

  // ========== UPDATED: handleReplyOptionClick ==========
  const handleReplyOptionClick = (option) => {
    generateReplyDraft(option);
  };

  // ========== UPDATED: handleSuggestionClick with letter check ==========
  const handleSuggestionClick = (suggestion) => {
    // ✅ Check if a letter has been analyzed
    if (!result) {
      setChatError("Please analyze a letter first.");
      setChatMessages(prev => [...prev, { 
        role: "assistant", 
        content: "⚠️ Please upload or paste a letter and click 'Analyze Letter' first before asking questions."
      }]);
      return;
    }
    
    setChatInput(suggestion);
    setTimeout(() => sendChatMessage(), 100);
  };

  const resetAnalysis = () => {
    if (typewriterRef.current) clearInterval(typewriterRef.current);
    setResult(null);
    setOriginalResult(null);
    setAnimatedSummary("");
    setText("");
    setFile(null);
    setChatMessages([{ role: "assistant", content: labels.welcome }]);
    setSessionLetterCount(0);
    setReplyOptions(null);
    setChatError(null);
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
    { id: "whatToDo", items: result?.required_actions || [] },
    { id: "howToPay", items: result?.payment_information || [] },
    { id: "documents", items: result?.required_documents || [] },
    { id: "consequences", items: result?.possible_consequences || [] },
    { id: "careful", items: result?.unclear_or_risky_parts || [] }
  ];

  const accordionIcons = { whatToDo: "✅", howToPay: "💳", documents: "📄", consequences: "⚠️", careful: "🛡️" };

  const accordionTitles = {
    whatToDo: labels.accordionWhat,
    howToPay: labels.accordionPay,
    documents: labels.accordionDocs,
    consequences: labels.accordionCons,
    careful: labels.accordionCareful
  };

  // ========== STYLES ==========
  const getStyles = () => ({
    page: {
      background: darkMode ? "#0f172a" : "#f3f6fb",
      minHeight: "100vh",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      color: darkMode ? "#e2e8f0" : "#111827",
      transition: "all 0.3s ease",
    },
    topbar: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "12px 24px",
      background: darkMode ? "#1e293b" : "white",
      borderBottom: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      transition: "all 0.3s ease",
    },
    brand: { display: "flex", alignItems: "center", gap: "10px" },
    brandIcon: { fontSize: "24px" },
    brandName: { fontSize: "16px", fontWeight: 600, color: darkMode ? "#e2e8f0" : "#1e1b4b" },
    topRight: { display: "flex", alignItems: "center", gap: "12px" },
    themeBtn: {
      background: darkMode ? "#334155" : "white",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "8px",
      padding: "5px 12px",
      cursor: "pointer",
      fontSize: "16px",
    },
    langSel: {
      background: darkMode ? "#334155" : "white",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "8px",
      padding: "5px 12px",
      fontSize: "12px",
      cursor: "pointer",
      color: darkMode ? "#e2e8f0" : "#374151",
    },
    backBtn: {
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      background: darkMode ? "#334155" : "white",
      padding: "5px 12px",
      borderRadius: "8px",
      cursor: "pointer",
      fontSize: "12px",
      color: darkMode ? "#e2e8f0" : "#374151",
    },
    aboutBtn: {
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      background: darkMode ? "#334155" : "white",
      padding: "5px 12px",
      borderRadius: "8px",
      cursor: "pointer",
      fontSize: "12px",
      color: darkMode ? "#e2e8f0" : "#374151",
    },
    main: {
      display: "grid",
      gridTemplateColumns: "320px 1fr",
      minHeight: "calc(100vh - 55px)",
    },
    leftPanel: {
      padding: "24px",
      borderRight: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      background: darkMode ? "#1e293b" : "#fafcff",
    },
    rightPanel: {
      background: darkMode ? "#0f172a" : "#f3f6fb",
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
      color: darkMode ? "#e2e8f0" : "#1e1b4b",
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
      color: darkMode ? "#e2e8f0" : "#1e1b4b",
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
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      background: darkMode ? "#334155" : "white",
      color: darkMode ? "#94a3b8" : "#6b7280",
    },
    modeBtnActive: {
      background: "#ede9fe",
      border: "1px solid #7c3aed",
      color: "#7c3aed",
    },
    textarea: {
      width: "100%",
      minHeight: "180px",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "12px",
      padding: "12px",
      fontSize: "13px",
      outline: "none",
      background: darkMode ? "#0f172a" : "white",
      fontFamily: "monospace",
      resize: "vertical",
      color: darkMode ? "#e2e8f0" : "#111827",
    },
    dropZone: {
      border: darkMode ? "2px dashed #475569" : "2px dashed #c7d2fe",
      borderRadius: "12px",
      padding: "32px",
      textAlign: "center",
      background: darkMode ? "#0f172a" : "#f8fbff",
      cursor: "pointer",
      minHeight: "180px",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: "6px",
    },
    dropIcon: { fontSize: "32px" },
    dropText: { fontSize: "13px", color: darkMode ? "#94a3b8" : "#4b5563" },
    dropSubtext: { fontSize: "11px", color: darkMode ? "#64748b" : "#9ca3af" },
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
      background: darkMode ? "#0f172a" : "#f8fafc",
      borderRadius: "12px",
      textAlign: "center",
      border: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
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
      color: darkMode ? "#94a3b8" : "#6b7280",
      display: "flex",
      alignItems: "center",
      gap: "6px",
      background: darkMode ? "#0f172a" : "#f8fafc",
      borderRadius: "8px",
      border: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
    },
    sessionNote: {
      fontSize: "11px",
      color: darkMode ? "#64748b" : "#9ca3af",
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
      color: darkMode ? "#64748b" : "#9ca3af",
    },
    emptyIcon: { fontSize: "48px", marginBottom: "12px" },
    emptyTitle: { fontSize: "16px", color: darkMode ? "#94a3b8" : "#6b7280", marginBottom: "4px" },
    emptySub: { fontSize: "13px", color: darkMode ? "#64748b" : "#9ca3af" },
    bottomLineCard: {
      background: darkMode ? "#1e293b" : "white",
      border: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      borderRadius: "14px",
      padding: "20px",
      boxShadow: darkMode ? "none" : "0 1px 3px rgba(0,0,0,0.05)",
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
      color: darkMode ? "#e2e8f0" : "#1e1b4b",
    },
    bridgeLine: {
      fontSize: "12px",
      color: darkMode ? "#94a3b8" : "#6b7280",
      marginTop: "10px",
      paddingTop: "10px",
      borderTop: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
    },
    bridgeLink: {
      color: "#7c3aed",
      cursor: "pointer",
      fontWeight: 500,
    },
    metaRow: {
      display: "flex",
      gap: "16px",
      flexWrap: "wrap",
      fontSize: "13px",
      color: darkMode ? "#94a3b8" : "#6b7280",
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
      background: darkMode ? "#2a1414" : "#fef2f2",
      border: darkMode ? "1px solid #5a2a2a" : "1px solid #fca5a5",
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
      color: darkMode ? "#94a3b8" : "#6b7280",
    },
    accordionWrap: {
      display: "flex",
      flexDirection: "column",
      gap: "6px",
    },
    accordion: {
      background: darkMode ? "#1e293b" : "white",
      border: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      borderRadius: "10px",
      padding: "4px 0",
    },
    accordionSummary: {
      padding: "12px 16px",
      cursor: "pointer",
      fontWeight: 600,
      fontSize: "13px",
      color: darkMode ? "#e2e8f0" : "#4c1d95",
      listStyle: "none",
      display: "flex",
      alignItems: "center",
      gap: "8px",
    },
    accordionBody: {
      padding: "0 16px 12px 16px",
      borderTop: darkMode ? "1px solid #334155" : "1px solid #f1f5f9",
    },
    accordionItem: {
      padding: "6px 0",
      fontSize: "13px",
      color: darkMode ? "#cbd5e1" : "#4b5563",
      borderBottom: darkMode ? "1px solid #334155" : "1px solid #f1f5f9",
    },
    additionalDetails: {
      background: darkMode ? "#1e293b" : "white",
      border: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      borderRadius: "10px",
      padding: "14px 16px",
    },
    additionalTitle: {
      fontWeight: 600,
      fontSize: "13px",
      color: darkMode ? "#e2e8f0" : "#4c1d95",
      marginBottom: "8px",
    },
    additionalItem: {
      fontSize: "12px",
      color: darkMode ? "#94a3b8" : "#6b7280",
      padding: "3px 0",
    },
    safetyNote: {
      background: darkMode ? "#0a1e0a" : "#f0fdf4",
      border: darkMode ? "1px solid #1a3a1a" : "1px solid #bbf7d0",
      borderRadius: "10px",
      padding: "10px 14px",
      fontSize: "12px",
      color: darkMode ? "#86efac" : "#166534",
    },
    actionRow: {
      display: "flex",
      gap: "8px",
      marginTop: "4px",
    },
    actionBtn: {
      background: darkMode ? "#334155" : "white",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "8px",
      padding: "6px 14px",
      fontSize: "12px",
      cursor: "pointer",
      color: darkMode ? "#e2e8f0" : "#374151",
    },
    skeletonCard: {
      height: "80px",
      borderRadius: "12px",
      background: darkMode ? "linear-gradient(90deg, #1e293b, #334155, #1e293b)" : "linear-gradient(90deg, #f1f5f9, #e2e8f0, #f1f5f9)",
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
      background: darkMode ? "#1e293b" : "white",
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
    chatButton: {
      position: "fixed",
      bottom: "30px",
      right: "30px",
      width: "60px",
      height: "60px",
      borderRadius: "50%",
      background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
      border: "none",
      color: "white",
      fontSize: "28px",
      cursor: "pointer",
      boxShadow: "0 8px 30px rgba(124,58,237,0.4)",
      transition: "all 0.3s ease",
      zIndex: 999,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    chatWindow: {
      position: "fixed",
      bottom: "100px",
      right: "30px",
      width: "420px",
      height: "560px",
      background: darkMode ? "#1e293b" : "white",
      borderRadius: "16px",
      boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
      display: isChatOpen ? "flex" : "none",
      flexDirection: "column",
      overflow: "hidden",
      zIndex: 999,
      border: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      animation: "slideUp 0.3s ease",
    },
    chatWindowHeader: {
      padding: "16px 20px",
      background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
      color: "white",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      flexShrink: 0,
    },
    chatWindowHeaderLeft: {
      display: "flex",
      alignItems: "center",
      gap: "10px",
    },
    chatWindowHeaderTitle: {
      fontSize: "16px",
      fontWeight: 600,
    },
    chatWindowHeaderSub: {
      fontSize: "12px",
      opacity: 0.8,
    },
    chatWindowClose: {
      background: "none",
      border: "none",
      color: "white",
      fontSize: "20px",
      cursor: "pointer",
      padding: "4px 8px",
      opacity: 0.8,
      transition: "opacity 0.2s",
    },
    chatWindowMessages: {
      flex: 1,
      overflowY: "auto",
      padding: "16px 20px",
      display: "flex",
      flexDirection: "column",
      gap: "12px",
      background: darkMode ? "#0f172a" : "#f8fafc",
    },
    chatWindowInput: {
      padding: "12px 16px",
      borderTop: darkMode ? "1px solid #334155" : "1px solid #e5e7eb",
      background: darkMode ? "#1e293b" : "white",
      flexShrink: 0,
      display: "flex",
      gap: "10px",
      alignItems: "center",
    },
    chatWindowInputField: {
      flex: 1,
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      borderRadius: "8px",
      padding: "10px 14px",
      fontSize: "13px",
      outline: "none",
      background: darkMode ? "#0f172a" : "white",
      color: darkMode ? "#e2e8f0" : "#111827",
    },
    chatWindowSendBtn: {
      background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
      border: "none",
      borderRadius: "8px",
      padding: "10px 20px",
      color: "white",
      cursor: "pointer",
      fontSize: "13px",
      fontWeight: 600,
      transition: "all 0.2s",
    },
    chatWindowSendBtnDisabled: {
      opacity: 0.5,
      cursor: "not-allowed",
    },
    chatMessageWrapper: {
      display: "flex",
      gap: "8px",
      maxWidth: "85%",
    },
    chatMessageWrapperUser: {
      alignSelf: "flex-end",
      flexDirection: "row-reverse",
    },
    chatMessageWrapperAssistant: {
      alignSelf: "flex-start",
    },
    chatAvatar: {
      width: "32px",
      height: "32px",
      borderRadius: "50%",
      background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "white",
      fontSize: "12px",
      fontWeight: 600,
      flexShrink: 0,
    },
    chatAvatarUser: {
      background: darkMode ? "#334155" : "#e5e7eb",
      color: darkMode ? "#e2e8f0" : "#1a1a1a",
    },
    chatBubble: {
      padding: "10px 14px",
      borderRadius: "12px",
      fontSize: "13px",
      lineHeight: 1.5,
      wordWrap: "break-word",
      maxWidth: "100%",
    },
    chatBubbleUser: {
      background: "linear-gradient(135deg, #7c3aed, #5b21b6)",
      color: "white",
      borderBottomRightRadius: "4px",
    },
    chatBubbleAssistant: {
      background: darkMode ? "#334155" : "white",
      color: darkMode ? "#e2e8f0" : "#1a1a1a",
      borderBottomLeftRadius: "4px",
      boxShadow: darkMode ? "none" : "0 1px 3px rgba(0,0,0,0.1)",
    },
    chatBubbleTime: {
      fontSize: "10px",
      color: darkMode ? "#64748b" : "#9ca3af",
      marginTop: "4px",
    },
    chatSuggestions: {
      display: "flex",
      gap: "6px",
      flexWrap: "wrap",
      padding: "8px 0",
    },
    chatSuggestion: {
      padding: "4px 12px",
      borderRadius: "20px",
      border: darkMode ? "1px solid #475569" : "1px solid #e5e7eb",
      fontSize: "11px",
      cursor: "pointer",
      background: darkMode ? "#334155" : "white",
      color: darkMode ? "#e2e8f0" : "#374151",
      transition: "all 0.2s",
    },
    chatCursor: {
      display: "inline-block",
      width: "2px",
      height: "14px",
      background: "#7c3aed",
      marginLeft: "2px",
      animation: "blink 1s infinite",
    },
    badge: {
      position: "absolute",
      top: "-4px",
      right: "-4px",
      width: "20px",
      height: "20px",
      borderRadius: "50%",
      background: "#ef4444",
      color: "white",
      fontSize: "10px",
      fontWeight: 700,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
  });

  const styles = getStyles();

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
            {Object.keys(LANGUAGE_NAMES).map(lang => (
              <option key={lang} value={lang}>{LANGUAGE_NAMES[lang]}</option>
            ))}
          </select>
          <button style={styles.themeBtn} onClick={toggleDarkMode}>
            {darkMode ? "☀️" : "🌙"}
          </button>
          <button style={styles.backBtn} onClick={onBack}>{labels.back}</button>
          <button style={styles.aboutBtn} onClick={() => setShowAbout(true)}>{labels.about}</button>
        </div>
      </div>

      {/* Main Grid */}
      <div style={styles.main}>
        <div style={styles.leftPanel}>
          <div style={styles.sidebarSection}>
            <div style={styles.stepBadge}>1</div>
            <div style={styles.sidebarTitle}>{labels.uploadTitle}</div>
          </div>
          
          <div style={styles.modeToggle}>
            <button onClick={() => setMode("text")} style={mode === "text" ? {...styles.modeBtn, ...styles.modeBtnActive} : styles.modeBtn}>
              {labels.pasteText}
            </button>
            <button onClick={() => setMode("pdf")} style={mode === "pdf" ? {...styles.modeBtn, ...styles.modeBtnActive} : styles.modeBtn}>
              {labels.upload}
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
              <div style={styles.dropText}>{labels.dropText}</div>
              <div style={styles.dropSubtext}>{labels.dropSubtext}</div>
              {file && <div style={styles.fileName}>✓ {file.name}</div>}
            </div>
          )}

          <button style={styles.analyzeBtn} onClick={analyzeLetter} disabled={loading}>
            {loading ? "⏳ Analyzing..." : labels.analyzeBtn}
          </button>

          {loading && (
            <div style={styles.loadingCard}>
              <div style={styles.loadingDot}></div>
              <div style={styles.loadingText}>{labels.processing}</div>
            </div>
          )}

          <div style={styles.privacyNote}>
            <span>🔒</span>
            <span>{labels.privacy}</span>
          </div>

          {sessionLetterCount > 0 && (
            <div style={styles.sessionNote}>
              {sessionLetterCount} {sessionLetterCount === 1 ? labels.lettersAnalyzed : labels.lettersAnalyzedPlural}
            </div>
          )}
        </div>

        <div style={styles.rightPanel}>
          <div style={styles.resultsArea}>
            <div style={styles.stepBadgeRow}>
              <div style={styles.stepBadge}>2</div>
              <div style={styles.stepBadgeLabel}>{labels.analysisResult}</div>
            </div>

            {!result && !loading && (
              <div style={styles.emptyState}>
                <div style={styles.emptyIcon}>📄</div>
                <div style={styles.emptyTitle}>{labels.emptyTitle}</div>
                <div style={styles.emptySub}>{labels.emptySub}</div>
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
                <div style={styles.bottomLineCard}>
                  <div style={styles.blLabel}>{labels.bottomLine}</div>
                  <div style={styles.blText}>
                    {isTranslating ? (
                      <span style={{ opacity: 0.6, display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span className="spinner">⟳</span> {labels.translating}
                      </span>
                    ) : (
                      `"${animatedSummary || result.tldr}"`
                    )}
                  </div>
                  <div style={styles.bridgeLine}>
                    {labels.bridgeText} <span style={styles.bridgeLink} onClick={() => setIsChatOpen(true)}>{labels.bridgeAsk}</span>
                  </div>
                </div>

                <div style={styles.metaRow}>
                  <span style={styles.metaItem}>📧 {result.sender || "Unknown sender"}</span>
                  <span style={styles.metaItem}>🏷️ {result.letter_topic || "Official letter"}</span>
                  <span style={styles.urgencyBadge}>● {result.urgency_level || "Medium"} {labels.urgency}</span>
                  {result.letter_involves_payment && (
                    <span style={styles.paymentBadge}>{labels.paymentInvolved}</span>
                  )}
                  {result.is_valid_letter === false && (
                    <span style={styles.warningBadge}>{labels.mayNotBeOfficial}</span>
                  )}
                </div>

                {daysLeft && (
                  <div style={styles.deadlineBar}>
                    ⏰ {daysLeft} {labels.daysLeft}
                  </div>
                )}

                <div style={{ ...styles.qualityBar, background: confidenceInfo.bg, border: `1px solid ${confidenceInfo.border}` }}>
                  <div style={{ ...styles.qualityTitle, color: confidenceInfo.color }}>
                    {labels.quality} {confidenceInfo.label}
                  </div>
                  <div style={styles.qualityText}>
                    {result.confidence_reason || "Analysis completed based on the letter content."}
                  </div>
                </div>

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
                          {accordionIcons[section.id]} {accordionTitles[section.id]}
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

                {result.useful_details && result.useful_details.length > 0 && (
                  <div style={styles.additionalDetails}>
                    <div style={styles.additionalTitle}>{labels.additionalDetails}</div>
                    {(result.useful_details || []).map((detail, i) => (
                      <div key={i} style={styles.additionalItem}>• {detail}</div>
                    ))}
                  </div>
                )}

                <div style={styles.safetyNote}>
                  {labels.safety} {result.safety_note || "This is AI-generated help, not legal advice."}
                </div>

                <div style={styles.actionRow}>
                  <button style={styles.actionBtn} onClick={copyToClipboard}>{copied ? labels.copied : labels.copy}</button>
                  <button style={styles.actionBtn} onClick={exportToPDF}>{labels.pdf}</button>
                  <button style={styles.actionBtn} onClick={resetAnalysis}>{labels.new}</button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Floating Chat Button */}
      <button
        style={styles.chatButton}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "scale(1.1)";
          e.currentTarget.style.boxShadow = "0 12px 40px rgba(124,58,237,0.6)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.boxShadow = "0 8px 30px rgba(124,58,237,0.4)";
        }}
        onClick={() => setIsChatOpen(!isChatOpen)}
      >
        {isChatOpen ? "✕" : "💬"}
        {!isChatOpen && chatMessages.length > 1 && (
          <span style={styles.badge}>{chatMessages.length - 1}</span>
        )}
      </button>

      {/* Floating Chat Window */}
      <div style={styles.chatWindow}>
        <div style={styles.chatWindowHeader}>
          <div style={styles.chatWindowHeaderLeft}>
            <span>🤖</span>
            <div>
              <div style={styles.chatWindowHeaderTitle}>{labels.chatTitle}</div>
              <div style={styles.chatWindowHeaderSub}>{labels.chatSub}</div>
            </div>
          </div>
          <button
            style={styles.chatWindowClose}
            onMouseEnter={(e) => (e.currentTarget.style.opacity = "1")}
            onMouseLeave={(e) => (e.currentTarget.style.opacity = "0.8")}
            onClick={() => setIsChatOpen(false)}
          >
            ✕
          </button>
        </div>

        <div style={styles.chatWindowMessages}>
          {chatMessages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                ...styles.chatMessageWrapper,
                ...(msg.role === "user"
                  ? styles.chatMessageWrapperUser
                  : styles.chatMessageWrapperAssistant),
              }}
            >
              {msg.role === "assistant" && (
                <div style={styles.chatAvatar}>AI</div>
              )}
              <div>
                <div
                  style={{
                    ...styles.chatBubble,
                    ...(msg.role === "user"
                      ? styles.chatBubbleUser
                      : styles.chatBubbleAssistant),
                  }}
                >
                  {msg.content}
                  {msg.isOptions && (
                    <div style={{ display: "flex", gap: "6px", marginTop: "8px", flexWrap: "wrap" }}>
                      {msg.options?.map((opt) => (
                        <button
                          key={opt}
                          style={{
                            padding: "4px 12px",
                            borderRadius: "20px",
                            border: "1px solid #7c3aed",
                            background: "#ede9fe",
                            color: "#7c3aed",
                            fontSize: "11px",
                            cursor: "pointer",
                          }}
                          onClick={() => handleReplyOptionClick(opt)}
                        >
                          {opt}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                <div style={styles.chatBubbleTime}>
                  {new Date().toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
              {msg.role === "user" && (
                <div style={{ ...styles.chatAvatar, ...styles.chatAvatarUser }}>U</div>
              )}
            </div>
          ))}
          {isStreaming && streamingMessage && (
            <div style={{ ...styles.chatMessageWrapper, ...styles.chatMessageWrapperAssistant }}>
              <div style={styles.chatAvatar}>AI</div>
              <div>
                <div style={{ ...styles.chatBubble, ...styles.chatBubbleAssistant }}>
                  {streamingMessage}
                  <span style={styles.chatCursor}>|</span>
                </div>
              </div>
            </div>
          )}
          {chatError && (
            <div style={{ ...styles.chatMessageWrapper, ...styles.chatMessageWrapperAssistant }}>
              <div style={styles.chatAvatar}>⚠️</div>
              <div>
                <div style={{ ...styles.chatBubble, ...styles.chatBubbleAssistant, background: darkMode ? "#2a1414" : "#fee2e2", color: "#dc2626" }}>
                  ❌ {chatError}
                </div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Chat Suggestions */}
        <div style={{ padding: "0 16px", background: darkMode ? "#1e293b" : "white" }}>
          <div style={styles.chatSuggestions}>
            {labels.suggestions.map((sug, i) => (
              <div
                key={i}
                style={styles.chatSuggestion}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = "#7c3aed";
                  e.currentTarget.style.color = "#7c3aed";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = darkMode ? "#475569" : "#e5e7eb";
                  e.currentTarget.style.color = darkMode ? "#e2e8f0" : "#374151";
                }}
                onClick={() => handleSuggestionClick(sug)}
              >
                {sug}
              </div>
            ))}
          </div>
        </div>

        {/* Chat Input - Updated with disabled state when no letter is analyzed */}
        <div style={styles.chatWindowInput}>
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendChatMessage()}
            placeholder={!result ? labels.analyzeFirst || "📄 Analyze a letter first to start chatting..." : (labels.typeMessage || labels.placeholder)}
            style={styles.chatWindowInputField}
            disabled={isStreaming || !result}
          />
          <button
            style={{
              ...styles.chatWindowSendBtn,
              ...((isStreaming || !chatInput.trim() || !result) ? styles.chatWindowSendBtnDisabled : {}),
            }}
            onClick={sendChatMessage}
            disabled={isStreaming || !chatInput.trim() || !result}
          >
            {labels.send || "Send"}
          </button>
        </div>
      </div>

      {/* About Modal */}
      {showAbout && (
        <div style={styles.modalOverlay} onClick={() => setShowAbout(false)}>
          <div style={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <h3>{labels.aboutTitle}</h3>
            <p><strong>Version:</strong> 3.0</p>
            <p>{labels.aboutFeatures}</p>
            <p>{labels.aboutPrivacy}</p>
            <p>{labels.aboutDisclaimer}</p>
            <button style={styles.modalClose} onClick={() => setShowAbout(false)}>{labels.close}</button>
          </div>
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0; }
        }
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .spinner {
          display: inline-block;
          animation: spin 1s linear infinite;
          font-size: 18px;
        }
      `}</style>
    </div>
  );
}