import assert from "node:assert/strict";
import test from "node:test";

import { ApiError } from "./letterAssistantApi.js";
import { getUserErrorMessage } from "./errorMessages.js";

test("localizes network failures without exposing fetch wording", () => {
  const error = new ApiError("Network request failed.", null, "network");
  assert.equal(
    getUserErrorMessage(error, "analysis", "Persian"),
    "ارتباط با سرور برقرار نشد. اتصال اینترنت را بررسی و دوباره تلاش کنید.",
  );
});

test("distinguishes upload validation errors", () => {
  assert.match(
    getUserErrorMessage(new ApiError("The uploaded file is too large.", 413), "analysis", "English"),
    /too large/i,
  );
  assert.match(
    getUserErrorMessage(new ApiError("The uploaded file is empty.", 400), "analysis", "German"),
    /leer/i,
  );
  assert.match(
    getUserErrorMessage(new ApiError("The file content does not match its declared type.", 400), "analysis", "English"),
    /does not match/i,
  );
});

test("uses an operation-specific message for translation failures", () => {
  assert.equal(
    getUserErrorMessage(new ApiError("Translation request failed.", 502), "translation", "English"),
    "We couldn't translate the analysis. The previous language has been restored.",
  );
});

test("uses English as the fallback error language", () => {
  assert.equal(
    getUserErrorMessage(new ApiError("Reply draft request failed.", 502), "replyDraft", "French"),
    "We couldn't create the reply draft. Please try again.",
  );
});
