const ERROR_MESSAGES = {
  English: {
    network: "We couldn't connect to the server. Check your connection and try again.",
    unsupportedFile: "This file type is not supported. Upload a PDF, JPEG, or PNG file.",
    emptyFile: "The selected file is empty. Choose another file.",
    fileTooLarge: "This file is too large. Choose a smaller file and try again.",
    fileMismatch: "The file content does not match its file type. Choose a valid PDF, JPEG, or PNG file.",
    missingText: "Paste the letter text before starting the analysis.",
    missingFile: "Choose a PDF or image before starting the analysis.",
    serviceUnavailable: "The language service is temporarily unavailable. Please try again shortly.",
    analysis: "We couldn't analyze this letter. Please try again.",
    translation: "We couldn't translate the analysis. The previous language has been restored.",
    chat: "We couldn't answer that question. Please try again.",
    replyDraft: "We couldn't create the reply draft. Please try again.",
    missingLetter: "Analyze a letter before using this feature.",
  },
  German: {
    network: "Die Verbindung zum Server konnte nicht hergestellt werden. Prüfen Sie Ihre Verbindung und versuchen Sie es erneut.",
    unsupportedFile: "Dieser Dateityp wird nicht unterstützt. Laden Sie eine PDF-, JPEG- oder PNG-Datei hoch.",
    emptyFile: "Die ausgewählte Datei ist leer. Wählen Sie eine andere Datei.",
    fileTooLarge: "Diese Datei ist zu groß. Wählen Sie eine kleinere Datei und versuchen Sie es erneut.",
    fileMismatch: "Der Dateiinhalt stimmt nicht mit dem Dateityp überein. Wählen Sie eine gültige PDF-, JPEG- oder PNG-Datei.",
    missingText: "Fügen Sie den Brieftext ein, bevor Sie die Analyse starten.",
    missingFile: "Wählen Sie eine PDF-Datei oder ein Bild, bevor Sie die Analyse starten.",
    serviceUnavailable: "Der Sprachdienst ist vorübergehend nicht verfügbar. Versuchen Sie es bitte später erneut.",
    analysis: "Der Brief konnte nicht analysiert werden. Bitte versuchen Sie es erneut.",
    translation: "Die Analyse konnte nicht übersetzt werden. Die vorherige Sprache wurde wiederhergestellt.",
    chat: "Die Frage konnte nicht beantwortet werden. Bitte versuchen Sie es erneut.",
    replyDraft: "Der Antwortentwurf konnte nicht erstellt werden. Bitte versuchen Sie es erneut.",
    missingLetter: "Analysieren Sie zuerst einen Brief, bevor Sie diese Funktion verwenden.",
  },
  Persian: {
    network: "ارتباط با سرور برقرار نشد. اتصال اینترنت را بررسی و دوباره تلاش کنید.",
    unsupportedFile: "این نوع فایل پشتیبانی نمی‌شود. یک فایل پی‌دی‌اف، جی‌پگ یا پی‌ان‌جی انتخاب کنید.",
    emptyFile: "فایل انتخاب‌شده خالی است. فایل دیگری انتخاب کنید.",
    fileTooLarge: "حجم فایل بیش از حد مجاز است. فایل کوچک‌تری انتخاب و دوباره تلاش کنید.",
    fileMismatch: "محتوای فایل با نوع آن مطابقت ندارد. یک فایل معتبر پی‌دی‌اف، جی‌پگ یا پی‌ان‌جی انتخاب کنید.",
    missingText: "پیش از شروع تحلیل، متن نامه را وارد کنید.",
    missingFile: "پیش از شروع تحلیل، یک فایل پی‌دی‌اف یا تصویر انتخاب کنید.",
    serviceUnavailable: "سرویس زبانی موقتاً در دسترس نیست. کمی بعد دوباره تلاش کنید.",
    analysis: "تحلیل این نامه انجام نشد. دوباره تلاش کنید.",
    translation: "ترجمهٔ تحلیل انجام نشد و زبان قبلی بازگردانده شد.",
    chat: "پاسخ‌گویی به این پرسش انجام نشد. دوباره تلاش کنید.",
    replyDraft: "ساخت پیش‌نویس پاسخ انجام نشد. دوباره تلاش کنید.",
    missingLetter: "پیش از استفاده از این قابلیت، یک نامه را تحلیل کنید.",
  },
};

const normalizedMessage = (error) => String(error?.message || "").toLowerCase();

export function getUserErrorMessage(error, operation = "analysis", language = "English") {
  const messages = ERROR_MESSAGES[language] || ERROR_MESSAGES.English;
  const message = normalizedMessage(error);
  const status = error?.status;
  const code = error?.code;

  if (code === "missing_text") return messages.missingText;
  if (code === "missing_file") return messages.missingFile;
  if (code === "missing_letter") return messages.missingLetter;
  if (code === "unsupported_file") return messages.unsupportedFile;
  if (code === "network" || message.includes("failed to fetch") || message.includes("networkerror")) {
    return messages.network;
  }
  if (status === 413 || message.includes("too large")) return messages.fileTooLarge;
  if (message.includes("uploaded file is empty")) return messages.emptyFile;
  if (message.includes("does not match its declared type")) return messages.fileMismatch;
  if (message.includes("only pdf, jpeg, or png")) return messages.unsupportedFile;
  if (status === 503 || message.includes("not configured") || message.includes("temporarily unavailable")) {
    return messages.serviceUnavailable;
  }
  if (message.includes("requires a valid analyzed letter") || message.includes("analyze a letter first")) {
    return messages.missingLetter;
  }

  return messages[operation] || messages.analysis;
}
