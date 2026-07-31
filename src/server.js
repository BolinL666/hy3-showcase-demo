
import http from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const rootDir = fileURLToPath(new URL("..", import.meta.url));
const publicDir = join(rootDir, "public");
const port = Number(process.env.PORT || 8787);
const host = process.env.HOST || "127.0.0.1";
const apiKey = process.env.TOKENHUB_API_KEY;
const tokenHubBaseUrl = process.env.TOKENHUB_BASE_URL || "https://tokenhub.tencentmaas.com/v1";
const model = process.env.HY3_MODEL || "hy3";

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8"
};

function sendJson(response, status, payload) {
  response.writeHead(status, { "content-type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload));
}

async function readJson(request) {
  const chunks = [];
  for await (const chunk of request) {
    chunks.push(chunk);
  }

  return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
}

function buildPrompt(goal) {
  return [
    "你是一个务实的项目规划者。请把用户输入的项目目标拆成可以今天开始执行的计划。",
    "输出必须使用 Markdown，包含：",
    "1. 一句话目标复述",
    "2. 5 个里程碑，每个里程碑包含任务、交付物、风险、验收标准",
    "3. 今天最应该做的 3 件事",
    "4. 一个不超过 60 秒演示视频的录制脚本",
    "",
    `项目目标：${goal}`
  ].join("\n");
}

async function callHy3(goal) {
  if (!apiKey) {
    throw new Error("TOKENHUB_API_KEY is not configured.");
  }

  const response = await fetch(`${tokenHubBaseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "authorization": `Bearer ${apiKey}`,
      "content-type": "application/json"
    },
    body: JSON.stringify({
      model,
      messages: [
        {
          role: "system",
          content: "你擅长把项目目标转化为清晰、可验收、适合开源协作的执行计划。"
        },
        {
          role: "user",
          content: buildPrompt(goal)
        }
      ],
      max_tokens: 900,
      temperature: 0.4
    })
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Hy3 request failed with ${response.status}: ${detail}`);
  }

  const data = await response.json();
  return data.choices?.[0]?.message?.content || "Hy3 returned an empty response.";
}

async function handlePlan(request, response) {
  try {
    const body = await readJson(request);
    const goal = String(body.goal || "").trim();

    if (goal.length < 8) {
      sendJson(response, 400, { error: "Please enter a project goal with at least 8 characters." });
      return;
    }

    const plan = await callHy3(goal);
    sendJson(response, 200, { plan });
  } catch (error) {
    sendJson(response, 500, { error: error.message });
  }
}

async function serveStatic(request, response) {
  const url = new URL(request.url, `http://${request.headers.host}`);
  const pathname = url.pathname === "/" ? "/index.html" : url.pathname;
  const safePath = normalize(pathname).replace(/^(\.\.[/\\])+/, "");
  const filePath = join(publicDir, safePath);

  try {
    const file = await readFile(filePath);
    response.writeHead(200, { "content-type": mimeTypes[extname(filePath)] || "application/octet-stream" });
    response.end(file);
  } catch {
    sendJson(response, 404, { error: "Not found" });
  }
}

const server = http.createServer(async (request, response) => {
  if (request.method === "POST" && request.url === "/api/plan") {
    await handlePlan(request, response);
    return;
  }

  if (request.method === "GET") {
    await serveStatic(request, response);
    return;
  }

  sendJson(response, 405, { error: "Method not allowed" });
});

server.listen(port, host, () => {
  console.log(`Hy3 project planner is running at http://${host}:${port}`);
});
