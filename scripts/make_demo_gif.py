from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "demo-run.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT_REG = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"

W, H = 1280, 720


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


f_eyebrow = font(18, True)
f_title = font(52, True)
f_subtitle = font(22)
f_label = font(22, True)
f_body = font(20)
f_small = font(16)
f_tiny = font(14)
f_result = font(18)
f_result_bold = font(20, True)

INK = "#162428"
MUTED = "#65747a"
TEAL = "#16766d"
TEAL_DARK = "#0d5b55"
MINT = "#e5f1eb"
CREAM = "#fffaf0"
LINE = "#ddd6c9"
PAPER = "#fffdf7"

goal = (
    "做一个面向研究生的论文阅读助手。输入论文标题和摘要后，"
    "Hy3 需要输出论文贡献、方法步骤、实验设计、局限性和复现计划。"
)

result_blocks = [
    [
        "# 项目目标复述",
        "把论文摘要转成结构化阅读笔记，并给出可落地的复现计划。",
        "",
        "## 里程碑 1：需求定义",
        "任务：确定输入字段、输出模板和目标用户。",
        "交付物：需求说明 + 输出样例。",
        "验收：研究生能直接复制结果做组会汇报。",
    ],
    [
        "## 里程碑 2：Hy3 接口接入",
        "任务：服务端通过 TokenHub 调用 model=hy3。",
        "交付物：/api/plan 接口和错误提示。",
        "风险：上游超时、输出过长或格式漂移。",
        "验收：输入摘要后返回贡献、方法、实验和局限。",
    ],
    [
        "## 里程碑 3：前端工作台",
        "任务：输入框、生成按钮、结果区、复制按钮。",
        "交付物：可运行 Web 页面。",
        "验收：浏览器打开即可完成一次完整生成。",
        "",
        "今天行动：整理 prompt、跑通接口、录制 60 秒 demo。",
    ],
    [
        "# 60 秒演示脚本",
        "0-10s：输入论文标题和摘要。",
        "10-25s：点击生成，说明请求链路。",
        "25-45s：展示 Hy3 拆出的贡献、方法、实验、局限。",
        "45-60s：复制结果，用于组会汇报或复现计划。",
    ],
]


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def ellipse(draw, box, fill):
    draw.ellipse(box, fill=fill)


def wrap(text, chars):
    if not text:
        return [""]
    return textwrap.wrap(text, width=chars, break_long_words=False, replace_whitespace=False)


def text(draw, xy, value, fnt, fill=INK):
    draw.text(xy, value, font=fnt, fill=fill)


def draw_wrapped(draw, value, xy, fnt, fill, chars, gap=7, max_y=None):
    x, y = xy
    for line in wrap(value, chars):
        if max_y and y > max_y:
            text(draw, (x, y), "…", fnt, fill)
            return y + fnt.size + gap
        text(draw, (x, y), line, fnt, fill)
        y += fnt.size + gap
    return y


def button(draw, box, label, active=True):
    fill = TEAL if active else "#dfece7"
    label_fill = "#ffffff" if active else "#1f3937"
    rounded(draw, box, 16, fill)
    bx = draw.textbbox((0, 0), label, font=f_label)
    x1, y1, x2, y2 = box
    text(
        draw,
        (x1 + (x2 - x1 - (bx[2] - bx[0])) / 2, y1 + (y2 - y1 - (bx[3] - bx[1])) / 2 - 3),
        label,
        f_label,
        label_fill,
    )


def pill(draw, xy, label, fill=MINT, fg=TEAL_DARK):
    x, y = xy
    bbox = draw.textbbox((0, 0), label, font=f_tiny)
    w = bbox[2] - bbox[0] + 24
    rounded(draw, (x, y, x + w, y + 30), 15, fill)
    text(draw, (x + 12, y + 7), label, f_tiny, fg)
    return x + w


def base(progress, subtitle, button_label="生成拆解计划", typed_chars=None, loading=False, lines=None, final=False):
    img = Image.new("RGB", (W, H), "#f7f2e8")
    draw = ImageDraw.Draw(img)

    ellipse(draw, (-140, -190, 550, 500), "#dcece4")
    ellipse(draw, (930, 430, 1510, 950), "#ead6c8")
    for x in range(0, W, 48):
        draw.line((x, 0, x, H), fill="#eee5d8")
    for y in range(0, H, 48):
        draw.line((0, y, W, y), fill="#eee5d8")

    text(draw, (54, 32), "●  Hy3 Project Planner · TokenHub Demo", f_eyebrow, TEAL)
    text(draw, (54, 67), "把一个想法，拆成可以执行的项目计划", f_title, INK)
    text(draw, (56, 132), subtitle, f_subtitle, MUTED)

    rounded(draw, (974, 42, 1226, 148), 26, "#ffffff", "#ffffff", 1)
    rounded(draw, (994, 62, 1032, 100), 14, TEAL)
    text(draw, (1046, 60), "真实 hy3 调用", f_label, INK)
    text(draw, (1046, 96), "密钥只保存在本地 .env", f_small, MUTED)

    proof_x = 54
    for title, value, width in [
        ("模型", "hy3", 174),
        ("接口", "TokenHub /v1/chat/completions", 342),
        ("输出", "计划 + 验收 + Demo 脚本", 330),
    ]:
        rounded(draw, (proof_x, 170, proof_x + width, 232), 20, "#ffffff", "#ffffff", 1)
        text(draw, (proof_x + 18, 184), title, f_tiny, "#7a888c")
        text(draw, (proof_x + 18, 205), value, f_small, INK)
        proof_x += width + 12

    rounded(draw, (54, 250, 476, 610), 28, "#ffffff", "#ffffff", 1)
    pill(draw, (78, 274), "01 输入项目场景")
    text(draw, (78, 318), "示例：论文阅读助手", f_label, INK)
    rounded(draw, (78, 354, 452, 504), 20, PAPER, LINE, 1)
    visible_goal = goal if typed_chars is None else goal[:typed_chars]
    y = 376
    for line in wrap(visible_goal, 19):
        text(draw, (102, y), line, f_body, "#263138")
        y += 30
    if typed_chars is not None and typed_chars < len(goal):
        text(draw, (102, y), "▌", f_body, TEAL)

    button(draw, (78, 530, 252, 576), button_label, active=True)
    button(draw, (268, 530, 404, 576), "换一个示例", active=False)

    rounded(draw, (498, 250, 1226, 610), 28, "#ffffff", "#ffffff", 1)
    pill(draw, (526, 274), "02 Hy3 结构化输出")
    button(draw, (1140, 274, 1200, 306), "复制", active=False)

    if loading:
        rounded(draw, (526, 340, 1198, 470), 22, "#f5faf8", "#dce7e3", 1)
        text(draw, (558, 366), "Hy3 正在生成结构化计划", font(30, True), TEAL)
        text(draw, (558, 420), "POST /api/plan  →  TokenHub  →  hy3", f_body, MUTED)
        for i, w in enumerate([90, 140, 110]):
            rounded(draw, (558 + i * 156, 508, 558 + i * 156 + w, 520), 6, "#dfece7")

    if lines:
        y = 326
        for line in lines:
            if line.startswith("#"):
                fnt, fill, extra = f_result_bold, TEAL_DARK, 4
            elif line.startswith("##"):
                fnt, fill, extra = f_result_bold, INK, 4
            else:
                fnt, fill, extra = f_result, "#263138", 1
            y = draw_wrapped(draw, line, (526, y), fnt, fill, 43, gap=5, max_y=572)
            y += extra

    if final:
        rounded(draw, (54, 626, 1226, 678), 22, "#ffffff", "#ffffff", 1)
        text(draw, (78, 643), "提交材料", f_tiny, "#7a888c")
        x = 166
        for label in ["文档 PR #206", "示例仓库", "assets/demo-run.gif"]:
            x = pill(draw, (x, 637), label) + 10
    else:
        rounded(draw, (54, 646, 1226, 652), 3, "#ded8ce")
        rounded(draw, (54, 646, int(54 + (1226 - 54) * progress), 652), 3, TEAL)
        text(draw, (54, 668), "演示重点：输入真实场景 → 服务端调用 Hy3 → 输出可复制的执行计划", f_small, MUTED)

    return img


frames = []
durations = []

for chars in [0, 20, 45, 72, 99, len(goal)]:
    frames.append(base(0.16, "示例清晰展示输入：评委能看懂这个工具要解决什么问题", typed_chars=chars))
    durations.append(330)

for _ in range(6):
    frames.append(base(0.38, "点击生成后，服务端调用 TokenHub 的 hy3 模型", "生成中...", loading=True))
    durations.append(420)

for idx, block in enumerate(result_blocks):
    for _ in range(5):
        frames.append(base(0.50 + idx * 0.11, "生成完成：输出是可执行、可验收、可演示的计划", "已生成", lines=block))
        durations.append(460)

frames.append(
    base(
        1.0,
        "交付物已经整理：文档 PR、示例仓库和演示 GIF 都可直接查看",
        "已生成",
        lines=[
            "# 已提交材料",
            "文档 PR：Tencent-Hunyuan/Hy3 #206",
            "示例仓库：github.com/BolinL666/hy3-showcase-demo",
            "演示 GIF：assets/demo-run.gif",
        ],
        final=True,
    )
)
durations.append(1500)

frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
)

print(OUT)
