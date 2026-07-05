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
    "Italian": "Il testo della lettera era troppo breve per essere analizzato in modo affidabile.",
    "Portuguese": "O texto da carta era curto demais para ser analisado de forma confiável.",
    "Dutch": "De brieftekst was te kort om betrouwbaar te analyseren.",
    "Polish": "Tekst pisma był zbyt krótki, aby można go było wiarygodnie przeanalizować.",
    "Russian": "Текст письма был слишком коротким для надежного анализа.",
    "Japanese": "手紙の本文が短すぎるため、信頼性の高い分析ができませんでした。",
    "Korean": "편지 내용이 너무 짧아 신뢰성 있게 분석할 수 없었습니다.",
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
    "Italian": "Nella lettera non sono state trovate azioni chiaramente richieste.",
    "Portuguese": "Nenhuma ação claramente necessária foi encontrada na carta.",
    "Dutch": "Er zijn geen duidelijk vereiste acties in de brief gevonden.",
    "Polish": "W piśmie nie znaleziono żadnych wyraźnie wymaganych działań.",
    "Russian": "В письме не было найдено четко требуемых действий.",
    "Japanese": "手紙の中に明確に必要な対応は見つかりませんでした。",
    "Korean": "편지에서 명확하게 필요한 조치를 찾을 수 없었습니다.",
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
    "Italian": "Il mittente e l'argomento della lettera non sono stati identificati.",
    "Portuguese": "O remetente e o assunto da carta não puderam ser identificados.",
    "Dutch": "De afzender en het onderwerp van de brief konden niet worden vastgesteld.",
    "Polish": "Nie udało się zidentyfikować nadawcy ani tematu pisma.",
    "Russian": "Не удалось определить отправителя и тему письма.",
    "Japanese": "手紙の送信者と件名を特定できませんでした。",
    "Korean": "편지의 발신자와 주제를 식별할 수 없었습니다.",
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
    "Italian": "Il mittente o l'argomento della lettera non sono stati identificati chiaramente.",
    "Portuguese": "O remetente ou o assunto da carta não foi identificado claramente.",
    "Dutch": "De afzender of het onderwerp van de brief kon niet duidelijk worden vastgesteld.",
    "Polish": "Nadawca lub temat pisma nie został jednoznacznie zidentyfikowany.",
    "Russian": "Отправитель или тема письма не были четко определены.",
    "Japanese": "手紙の送信者または件名を明確に特定できませんでした。",
    "Korean": "편지의 발신자 또는 주제를 명확하게 식별할 수 없었습니다.",
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
    "Italian": "Questa lettera riguarda un pagamento, ma le istruzioni di pagamento sembrano incomplete; mancano l'IBAN o il destinatario del pagamento.",
    "Portuguese": "Esta carta envolve um pagamento, mas as instruções de pagamento parecem incompletas; falta o IBAN ou o destinatário do pagamento.",
    "Dutch": "Deze brief gaat over een betaling, maar de betalingsinstructies lijken onvolledig; IBAN of ontvanger ontbreekt.",
    "Polish": "To pismo dotyczy płatności, ale instrukcje płatności wydają się niekompletne; brakuje numeru IBAN lub odbiorcy płatności.",
    "Russian": "Это письмо связано с платежом, но платежные данные кажутся неполными; отсутствует IBAN или получатель платежа.",
    "Japanese": "この手紙には支払いが含まれていますが、支払い情報が不完全なようです。IBANまたは受取人が記載されていません。",
    "Korean": "이 편지에는 결제가 포함되어 있지만 결제 안내가 불완전해 보입니다. IBAN 또는 수취인이 누락되었습니다.",
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
    "Italian": "Questa lettera sembra richiedere un'azione tempestiva, ma non è stata trovata una scadenza chiara.",
    "Portuguese": "Esta carta parece exigir uma ação dentro de um prazo, mas nenhum prazo claro foi encontrado.",
    "Dutch": "Deze brief lijkt tijdige actie te vereisen, maar er is geen duidelijke deadline gevonden.",
    "Polish": "To pismo wydaje się wymagać działania w określonym czasie, ale nie znaleziono jasnego terminu.",
    "Russian": "Похоже, это письмо требует своевременного действия, но четкий срок не был найден.",
    "Japanese": "この手紙は期限内の対応が必要なようですが、明確な期限は見つかりませんでした。",
    "Korean": "이 편지는 기한 내 조치가 필요한 것처럼 보이지만 명확한 마감일을 찾을 수 없었습니다.",
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
    "Italian": "Il testo della lettera era chiaro e tutti i dettagli principali sono stati identificati.",
    "Portuguese": "O texto da carta estava claro e todos os principais detalhes foram identificados.",
    "Dutch": "De brieftekst was duidelijk en alle belangrijke details zijn herkend.",
    "Polish": "Treść pisma była jasna i wszystkie najważniejsze szczegóły zostały zidentyfikowane.",
    "Russian": "Текст письма был понятным, и все основные детали были определены.",
    "Japanese": "手紙の内容は明確で、重要な情報はすべて確認できました。",
    "Korean": "편지 내용이 명확했고 모든 주요 세부사항이 확인되었습니다.",
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
