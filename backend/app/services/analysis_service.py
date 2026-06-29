import re
from typing import Union

from app.schemas.common import OutputLanguage
from app.schemas.analysis import AnalyzeTextResponse, InvalidLetterResponse
from app.services.llm_service import analyze_letter_with_llm

CONFIDENCE_REASON_TEXTS = {
    "text_too_short": {
    "English": "The letter text was too short to analyze reliably.",
    "German": "Der Brieftext war zu kurz, um ihn zuverlässig zu analysieren.",
    "Persian": "متن نامه خیلی کوتاه بود و نمی‌شود آن را با اطمینان تحلیل کرد.",
    "Turkish": "Mektup metni güvenilir şekilde analiz edilemeyecek kadar kısaydı.",
    "Arabic": "كان نص الرسالة قصيراً جداً ولا يمكن تحليله بشكل موثوق.",
    "French": "Le texte de la lettre était trop court pour être analysé de manière fiable.",
    "Spanish": "El texto de la carta era demasiado corto para analizarlo de forma fiable.",
    "Hindi": "पत्र का पाठ विश्वसनीय रूप से विश्लेषण करने के लिए बहुत छोटा था।",
    "Chinese": "信件内容太短，无法可靠地进行分析。",
},
    "no_required_actions": {
    "English": "No clear required actions could be found in the letter.",
    "German": "Im Brief konnten keine klar erforderlichen Handlungen gefunden werden.",
    "Persian": "هیچ اقدام لازم و واضحی در نامه پیدا نشد.",
    "Turkish": "Mektupta açıkça gerekli bir işlem bulunamadı.",
    "Arabic": "لم يتم العثور على إجراءات مطلوبة واضحة في الرسالة.",
    "French": "Aucune action clairement requise n'a été trouvée dans la lettre.",
    "Spanish": "No se encontraron acciones claramente requeridas en la carta.",
    "Hindi": "पत्र में कोई स्पष्ट आवश्यक कार्रवाई नहीं मिली।",
    "Chinese": "信件中没有找到明确需要采取的行动。",
},
"sender_and_topic_missing": {
    "English": "The sender and topic of the letter could not be identified.",
    "German": "Absender und Thema des Briefes konnten nicht erkannt werden.",
    "Persian": "فرستنده و موضوع نامه قابل شناسایی نبودند.",
    "Turkish": "Mektubun göndereni ve konusu belirlenemedi.",
    "Arabic": "تعذر تحديد مرسل الرسالة وموضوعها.",
    "French": "L'expéditeur et le sujet de la lettre n'ont pas pu être identifiés.",
    "Spanish": "No se pudieron identificar el remitente ni el tema de la carta.",
    "Hindi": "पत्र के भेजने वाले और विषय की पहचान नहीं की जा सकी।",
    "Chinese": "无法识别信件的发件人和主题。",
},
"sender_or_topic_missing": {
    "English": "The sender or topic of the letter was not clearly identified.",
    "German": "Der Absender oder das Thema des Briefes wurde nicht klar erkannt.",
    "Persian": "فرستنده یا موضوع نامه به‌طور واضح شناسایی نشد.",
    "Turkish": "Mektubun göndereni veya konusu net şekilde belirlenemedi.",
    "Arabic": "لم يتم تحديد مرسل الرسالة أو موضوعها بوضوح.",
    "French": "L'expéditeur ou le sujet de la lettre n'a pas été clairement identifié.",
    "Spanish": "El remitente o el tema de la carta no se identificó claramente.",
    "Hindi": "पत्र के भेजने वाले या विषय की स्पष्ट पहचान नहीं हो सकी।",
    "Chinese": "信件的发件人或主题没有被明确识别。",
},
"payment_incomplete": {
    "English": "This letter involves a payment, but the payment instructions appear incomplete — IBAN or payment recipient is missing.",
    "German": "Dieser Brief betrifft eine Zahlung, aber die Zahlungsangaben scheinen unvollständig zu sein; IBAN oder Zahlungsempfänger fehlt.",
    "Persian": "این نامه شامل پرداخت است، اما اطلاعات پرداخت ناقص به نظر می‌رسد؛ مثلاً IBAN یا گیرنده پرداخت مشخص نیست.",
    "Turkish": "Bu mektup bir ödeme içeriyor, ancak ödeme bilgileri eksik görünüyor; IBAN veya ödeme alıcısı eksik.",
    "Arabic": "تتضمن هذه الرسالة دفعة، لكن تعليمات الدفع تبدو غير مكتملة؛ رقم IBAN أو مستلم الدفع غير مذكور.",
    "French": "Cette lettre concerne un paiement, mais les informations de paiement semblent incomplètes ; l'IBAN ou le destinataire du paiement manque.",
    "Spanish": "Esta carta implica un pago, pero las instrucciones de pago parecen incompletas; falta el IBAN o el destinatario del pago.",
    "Hindi": "इस पत्र में भुगतान शामिल है, लेकिन भुगतान निर्देश अधूरे लगते हैं; IBAN या भुगतान प्राप्तकर्ता गायब है।",
    "Chinese": "这封信涉及付款，但付款说明似乎不完整；缺少 IBAN 或收款人信息。",
},
"deadline_missing": {
    "English": "This letter seems to require timely action, but no clear deadline was found.",
    "German": "Dieser Brief scheint eine rechtzeitige Handlung zu erfordern, aber es wurde keine klare Frist gefunden.",
    "Persian": "به نظر می‌رسد این نامه نیاز به اقدام در زمان مشخص دارد، اما مهلت واضحی پیدا نشد.",
    "Turkish": "Bu mektup zamanında işlem gerektiriyor gibi görünüyor, ancak net bir son tarih bulunamadı.",
    "Arabic": "يبدو أن هذه الرسالة تتطلب إجراءً في الوقت المناسب، لكن لم يتم العثور على موعد نهائي واضح.",
    "French": "Cette lettre semble nécessiter une action dans les délais, mais aucune échéance claire n'a été trouvée.",
    "Spanish": "Esta carta parece requerir una acción a tiempo, pero no se encontró una fecha límite clara.",
    "Hindi": "यह पत्र समय पर कार्रवाई की मांग करता लगता है, लेकिन कोई स्पष्ट समय सीमा नहीं मिली।",
    "Chinese": "这封信似乎需要及时采取行动，但没有找到明确的截止日期。",
},
"clear_details": {
    "English": "The letter text was clear and all key details were identified.",
    "German": "Der Brieftext war klar und alle wichtigen Details wurden erkannt.",
    "Persian": "متن نامه واضح بود و جزئیات اصلی شناسایی شدند.",
    "Turkish": "Mektup metni açıktı ve tüm önemli ayrıntılar belirlendi.",
    "Arabic": "كان نص الرسالة واضحاً وتم تحديد جميع التفاصيل الرئيسية.",
    "French": "Le texte de la lettre était clair et tous les détails clés ont été identifiés.",
    "Spanish": "El texto de la carta era claro y se identificaron todos los detalles clave.",
    "Hindi": "पत्र का पाठ स्पष्ट था और सभी मुख्य विवरण पहचाने गए।",
    "Chinese": "信件内容清晰，所有关键细节均已识别。",
},
}


def get_confidence_reason(reason_key: str, output_language: OutputLanguage) -> str:
    reason_texts = CONFIDENCE_REASON_TEXTS[reason_key]
    return reason_texts.get(output_language, reason_texts["English"])

def calculate_reliability(
    llm_result: dict,
    output_language: OutputLanguage = "English",
) -> tuple[str, str]:
    """
    Calculate confidence_level and confidence_reason based on
    rule-based checks on the LLM output.
    """
    letter_text = llm_result.get("letter_text", "")
    sender = llm_result.get("sender", "")
    letter_topic = llm_result.get("letter_topic", "")
    required_actions = llm_result.get("required_actions", [])
    deadlines = llm_result.get("deadlines", [])
    payment_information = llm_result.get("payment_information", [])
    urgency_level = llm_result.get("urgency_level", "Low")
    letter_involves_payment = llm_result.get("letter_involves_payment", False)

    not_stated = "Not clearly stated in the letter."

    # Low reliability checks
    if len(letter_text) < 200:
        return "low", get_confidence_reason("text_too_short", output_language)

    if not required_actions and urgency_level != "Low":
        return "low", get_confidence_reason("no_required_actions", output_language)

    if sender == not_stated and letter_topic == not_stated:
        return "low", get_confidence_reason("sender_and_topic_missing", output_language)
    # Medium reliability checks
    if sender == not_stated or letter_topic == not_stated:
        return "medium", get_confidence_reason("sender_or_topic_missing", output_language)
    if letter_involves_payment:
        payment_text = " ".join(payment_information).lower()
        payment_text_no_spaces = payment_text.replace(" ", "")

        has_iban = bool(
            re.search(
                r"\bde[0-9]{2}[a-z0-9]{10,30}\b",
                payment_text_no_spaces,
            )
        )

        has_recipient = any(
            w in payment_text
            for w in [
                "zahlungsempfänger",
                "empfänger",
                "recipient",
                "gläubiger",
                "krankenkasse",
                "sparkasse",
                "finanzamt",
                "hausverwaltung",
                "universität",
                "gmbh",
                "ag",
            ]
        )

        if not payment_information or not has_iban or not has_recipient:
            return "medium", get_confidence_reason("payment_incomplete", output_language)

    if urgency_level != "Low" and not deadlines:
        return "medium", get_confidence_reason("deadline_missing", output_language)
    
    # High reliability
    return "high", get_confidence_reason("clear_details", output_language)


def analyze_letter_text(
    letter_text: str,
    output_language: OutputLanguage = "English",
) -> Union[AnalyzeTextResponse, InvalidLetterResponse]:
    llm_result = analyze_letter_with_llm(
        letter_text=letter_text,
        output_language=output_language,
    )

    if not llm_result.get("is_valid_letter", True):
        return InvalidLetterResponse(
            message=llm_result.get(
                "message",
                "This doesn't look like an official German letter.",
            )
        )

    llm_result["letter_text"] = letter_text

    confidence_level, confidence_reason = calculate_reliability(
        llm_result=llm_result,
        output_language=output_language,
    )
    llm_result["confidence_level"] = confidence_level
    llm_result["confidence_reason"] = confidence_reason

    return AnalyzeTextResponse(**llm_result)