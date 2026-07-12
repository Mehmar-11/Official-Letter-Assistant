import assert from "node:assert/strict";
import test from "node:test";

import {
  analyzeText,
  ApiError,
  generateReplyDraft,
  streamChat,
  translateAnalysis,
} from "./letterAssistantApi.js";

function eventStream(events) {
  const encoder = new TextEncoder();
  const chunks = events.map((event) => encoder.encode(`data: ${JSON.stringify(event)}\n\n`));
  return new ReadableStream({
    start(controller) {
      for (const chunk of chunks) controller.enqueue(chunk);
      controller.close();
    },
  });
}

function mockResponse(events, status = 200) {
  return new Response(eventStream(events), {
    status,
    headers: { "Content-Type": "text/event-stream" },
  });
}

test("JSON requests classify fetch failures as network errors", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    throw new TypeError("Failed to fetch");
  };

  try {
    await assert.rejects(
      analyzeText("Letter", "English"),
      (error) => error instanceof ApiError && error.code === "network" && error.status === null,
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("streamChat combines token events", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => mockResponse([
    { type: "token", content: "The deadline " },
    { type: "token", content: "is tomorrow." },
    { type: "done" },
  ]);

  try {
    const result = await streamChat({
      letterText: "Letter",
      analysis: { letter_text: "Letter" },
      messages: [{ role: "user", content: "When?" }],
      outputLanguage: "English",
    });
    assert.equal(result.content, "The deadline is tomorrow.");
    assert.equal(result.replyOptions, null);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("streamChat returns stable reply option identifiers", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => mockResponse([
    { type: "reply_options", options: ["already_completed", "need_more_time_or_question", "disagree"] },
    { type: "done" },
  ]);

  try {
    const result = await streamChat({
      letterText: "Letter",
      analysis: { letter_text: "Letter" },
      messages: [{ role: "user", content: "Draft a reply" }],
      outputLanguage: "English",
    });
    assert.deepEqual(result.replyOptions, ["already_completed", "need_more_time_or_question", "disagree"]);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("streamChat surfaces SSE error events", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => mockResponse([
    { type: "error", message: "Chat request failed." },
  ]);

  try {
    await assert.rejects(
      streamChat({
        letterText: "Letter",
        analysis: { letter_text: "Letter" },
        messages: [{ role: "user", content: "Question" }],
        outputLanguage: "English",
      }),
      (error) => error instanceof ApiError && error.message === "Chat request failed.",
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("generateReplyDraft sends only the backend contract fields", async () => {
  const originalFetch = globalThis.fetch;
  let requestBody;
  globalThis.fetch = async (_url, options) => {
    requestBody = JSON.parse(options.body);
    return Response.json({ reply: "Draft" });
  };

  try {
    await generateReplyDraft({ is_valid_letter: true }, "already_completed");
    assert.deepEqual(requestBody, {
      analysis: { is_valid_letter: true },
      intent: "already_completed",
    });
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("generateReplyDraft includes trimmed optional context", async () => {
  const originalFetch = globalThis.fetch;
  let requestBody;
  globalThis.fetch = async (_url, options) => {
    requestBody = JSON.parse(options.body);
    return Response.json({ reply: "Draft" });
  };

  try {
    await generateReplyDraft(
      { is_valid_letter: true },
      "need_more_time_or_question",
      "  Please request two more weeks.  ",
    );
    assert.deepEqual(requestBody, {
      analysis: { is_valid_letter: true },
      intent: "need_more_time_or_question",
      additional_context: "Please request two more weeks.",
    });
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("translateAnalysis sends the complete analysis in one request", async () => {
  const originalFetch = globalThis.fetch;
  const analysis = { letter_text: "Letter", required_actions: ["Pay"] };
  let requestBody;
  globalThis.fetch = async (_url, options) => {
    requestBody = JSON.parse(options.body);
    return Response.json({ ...analysis, required_actions: ["Zahlen"] });
  };

  try {
    await translateAnalysis(analysis, "German");
    assert.deepEqual(requestBody, {
      analysis,
      output_language: "German",
    });
  } finally {
    globalThis.fetch = originalFetch;
  }
});
