const API_URL = (import.meta.env?.VITE_API_URL || "http://localhost:8000").replace(/\/+$/, "");

export class ApiError extends Error {
  constructor(message, status = null, code = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

async function fetchResponse(url, options) {
  try {
    return await fetch(url, options);
  } catch {
    throw new ApiError("Network request failed.", null, "network");
  }
}

async function readError(response, fallback) {
  try {
    const data = await response.json();
    return data.detail || data.message || fallback;
  } catch {
    return fallback;
  }
}

async function requestJson(path, options, fallback) {
  const response = await fetchResponse(`${API_URL}${path}`, options);
  if (!response.ok) {
    throw new ApiError(await readError(response, fallback), response.status);
  }
  return response.json();
}

export function analyzeText(letterText, outputLanguage) {
  return requestJson(
    "/analyze-text",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ letter_text: letterText, output_language: outputLanguage }),
    },
    "Letter analysis failed.",
  );
}

export function analyzeFile(file, outputLanguage) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("output_language", outputLanguage);
  return requestJson(
    "/analyze-pdf",
    { method: "POST", body: formData },
    "File analysis failed.",
  );
}

export function translateAnalysis(analysis, outputLanguage) {
  return requestJson(
    "/translate",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ analysis, output_language: outputLanguage }),
    },
    "Translation failed.",
  );
}

export function generateReplyDraft(analysis, intent, additionalContext = "") {
  const body = { analysis, intent };
  if (additionalContext.trim()) {
    body.additional_context = additionalContext.trim();
  }

  return requestJson(
    "/reply-draft",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    "Reply draft generation failed.",
  );
}

function parseEventBlock(block) {
  const payload = block
    .split(/\r?\n/)
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice(5).trimStart())
    .join("\n");

  return payload ? JSON.parse(payload) : null;
}

export async function streamChat({
  letterText,
  analysis,
  messages,
  outputLanguage,
  onToken,
}) {
  const response = await fetchResponse(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      letter_text: letterText,
      analysis,
      messages,
      output_language: outputLanguage,
    }),
  });

  if (!response.ok) {
    throw new ApiError(await readError(response, "Chat request failed."), response.status);
  }

  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("text/event-stream") || !response.body) {
    throw new ApiError("The backend returned an invalid chat response.", response.status);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let content = "";
  let replyOptions = null;
  let completed = false;

  const handleEvent = (event) => {
    if (!event) return;
    if (event.type === "token") {
      content += event.content || "";
      onToken?.(content);
      return;
    }
    if (event.type === "reply_options") {
      replyOptions = event.options || [];
      return;
    }
    if (event.type === "error") {
      throw new ApiError(event.message || "Chat request failed.");
    }
    if (event.type === "done") completed = true;
  };

  while (!completed) {
    const { done, value } = await reader.read();
    buffer += decoder.decode(value || new Uint8Array(), { stream: !done });

    const blocks = buffer.split(/\r?\n\r?\n/);
    buffer = blocks.pop() || "";
    for (const block of blocks) handleEvent(parseEventBlock(block));
    if (done) break;
  }

  if (buffer.trim()) handleEvent(parseEventBlock(buffer));
  if (!completed) throw new ApiError("The chat stream ended unexpectedly.");

  return { content, replyOptions };
}
