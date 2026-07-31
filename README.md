
# Hy3 项目计划生成器

一个基于腾讯混元 Hy3 的轻量 Web Demo。用户输入一个项目目标后，应用会通过 TokenHub OpenAI 兼容接口调用 `hy3` 模型，把一句比较开放的想法拆成可以执行、可以验收、可以直接用于汇报的项目计划。

这个仓库用于展示 Hy3 在真实开发场景里的落地方式：不是只返回一段泛泛的建议，而是把目标拆成阶段、任务、交付物、风险、验收标准和 60 秒演示脚本。

![Hy3 项目计划生成器演示](assets/demo-run.gif)

## Demo 场景

示例输入：

```text
做一个面向研究生的论文阅读助手。输入论文标题和摘要后，Hy3 需要输出论文贡献、方法步骤、实验设计、局限性和复现计划。
```

点击生成后，页面会把请求发送到本地服务端：

```text
浏览器 → /api/plan → TokenHub /v1/chat/completions → hy3
```

Hy3 返回的内容会被展示在右侧结果区，用户可以直接复制到项目计划、周报、PR 描述或演示讲稿中。

## 核心功能

- 输入自然语言项目目标，生成结构化执行计划。
- 输出目标复述、5 个里程碑、每个里程碑的任务/交付物/风险/验收标准。
- 自动补充“今天可以开始做什么”和“60 秒 demo 脚本”。
- 服务端统一调用 TokenHub，前端只负责输入和展示。
- 无前端框架和第三方运行依赖，Node.js 18+ 即可启动。

## 为什么使用 Hy3

这个 Demo 重点验证 Hy3 的项目理解和长文本组织能力。项目目标通常不是一个明确的代码需求，而是一段比较松散的想法；Hy3 适合把这类输入整理成稳定的结构化输出。

在这个应用里，Hy3 主要承担三件事：

1. 理解用户输入的项目目标和使用场景。
2. 把目标拆成可执行的阶段计划。
3. 补充风险、验收标准和演示脚本，让结果更接近真实项目交付。

## 项目结构

```text
.
├── public/
│   ├── index.html        # 页面结构
│   ├── styles.css        # 页面样式
│   └── main.js           # 前端交互
├── src/
│   ├── server.js         # 本地服务端与 Hy3 调用逻辑
│   └── check-config.js   # 配置检查脚本
├── assets/
│   ├── demo-run.gif      # 演示 GIF
│   └── demo-output.md    # 一次真实调用输出记录
├── scripts/
│   └── make_demo_gif.py  # GIF 生成脚本
├── .env.example
└── package.json
```

## 本地运行

复制环境变量示例：

```bash
cp .env.example .env
```

填写 `.env`：

```bash
TOKENHUB_API_KEY=你的 TokenHub API Key
PORT=8787
```

启动服务：

```bash
set -a
source .env
set +a
npm start
```

浏览器打开：

```text
http://localhost:8787
```

## 配置项

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `TOKENHUB_API_KEY` | 无 | TokenHub API Key |
| `TOKENHUB_BASE_URL` | `https://tokenhub.tencentmaas.com/v1` | TokenHub OpenAI 兼容地址 |
| `HY3_MODEL` | `hy3` | 调用的模型名 |
| `HOST` | `127.0.0.1` | 本地监听地址 |
| `PORT` | `8787` | 本地服务端口 |

## 输出格式

服务端会要求 Hy3 尽量按照固定结构输出，方便用户直接复制使用：

```text
# 项目目标复述

## 里程碑 1
- 任务
- 交付物
- 风险
- 验收标准

## 今天可以开始做什么

## 60 秒演示脚本
```

## 验证记录

已使用 TokenHub `hy3` 模型完成一次端到端调用验证。示例输入与返回结果保存在：

```text
assets/demo-output.md
```

## 相关提交

- Hy3 集成文档 PR：[Tencent-Hunyuan/Hy3 #206](https://github.com/Tencent-Hunyuan/Hy3/pull/206)
- 展示仓库：[BolinL666/hy3-showcase-demo](https://github.com/BolinL666/hy3-showcase-demo)
