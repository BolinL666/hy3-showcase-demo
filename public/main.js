const form = document.querySelector("#plan-form");
const goalInput = document.querySelector("#goal");
const result = document.querySelector("#result");
const submitButton = document.querySelector("#submit-button");
const sampleButton = document.querySelector("#sample-button");
const copyButton = document.querySelector("#copy-button");

const samples = [
  "为一个开源项目补充 Hy3 接入文档，覆盖 OpenRouter、Codex CLI、Cline、Continue、Aider 和 Dify，并制作一个可运行示例。",
  "做一个面向研究生的论文阅读工作台，把一篇论文拆成摘要、方法、实验、局限和复现计划。",
  "开发一个小型浏览器插件，用 Hy3 帮用户把网页长文整理成行动清单和会议纪要。"
];

let sampleIndex = 0;

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  submitButton.textContent = isLoading ? "生成中..." : "生成拆解计划";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const goal = goalInput.value.trim();

  if (!goal) {
    result.textContent = "请先输入项目目标。";
    return;
  }

  setLoading(true);
  result.textContent = "Hy3 正在拆解任务，请稍候...";

  try {
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ goal })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "请求失败");
    }

    result.textContent = data.plan;
  } catch (error) {
    result.textContent = `调用失败：${error.message}\n\n请确认已配置 TOKENHUB_API_KEY，并且本地服务正在运行。`;
  } finally {
    setLoading(false);
  }
});

sampleButton.addEventListener("click", () => {
  sampleIndex = (sampleIndex + 1) % samples.length;
  goalInput.value = samples[sampleIndex];
  goalInput.focus();
});

copyButton.addEventListener("click", async () => {
  await navigator.clipboard.writeText(result.textContent);
  copyButton.textContent = "已复制";
  window.setTimeout(() => {
    copyButton.textContent = "复制";
  }, 1200);
});
