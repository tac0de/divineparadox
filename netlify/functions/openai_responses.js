/* eslint-disable no-undef */

function json(statusCode, obj, extraHeaders = {}) {
  return {
    statusCode,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...extraHeaders,
    },
    body: JSON.stringify(obj),
  };
}

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 204,
      headers: {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "POST,OPTIONS",
        "access-control-allow-headers": "authorization,content-type,x-request-id",
        "cache-control": "no-store",
      },
      body: "",
    };
  }

  if (event.httpMethod !== "POST") {
    return json(405, { ok: false, error: "method_not_allowed" }, { "access-control-allow-origin": "*" });
  }

  const OPENAI_BRIDGE_URL = (process.env.OPENAI_BRIDGE_URL || "").replace(/\/+$/, "");
  const DEPLOY_TOKEN = process.env.DEPLOY_TOKEN || "";
  if (!OPENAI_BRIDGE_URL) return json(500, { ok: false, error: "openai_bridge_url_missing" });
  if (!DEPLOY_TOKEN) return json(500, { ok: false, error: "deploy_token_missing" });

  let bodyObj = {};
  try {
    bodyObj = event.body ? JSON.parse(event.body) : {};
  } catch {
    return json(400, { ok: false, error: "invalid_json" }, { "access-control-allow-origin": "*" });
  }

  const requestId = event.headers["x-request-id"] || event.headers["X-Request-Id"] || "";

  const upstream = await fetch(`${OPENAI_BRIDGE_URL}/v1/responses`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${DEPLOY_TOKEN}`,
      ...(requestId ? { "x-request-id": String(requestId) } : {}),
    },
    body: JSON.stringify(bodyObj),
  });

  const text = await upstream.text();

  return {
    statusCode: upstream.status,
    headers: {
      "content-type": upstream.headers.get("content-type") || "application/json; charset=utf-8",
      "cache-control": "no-store",
      "access-control-allow-origin": "*",
    },
    body: text,
  };
};

