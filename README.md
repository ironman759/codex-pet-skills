# Codex Pet Skills

这是一套用于设计、生产和安装 Codex 个性化宠物的 skills。它把“先确认角色设计”与“再生成并质检动画精灵图”分成两个阶段，避免未经确认的形象直接进入最终宠物。

## 包含内容

### `jarvis-pet-studio`

前期设计入口，适合从动物、人物、原创角色或参考图制作个性化 Codex 宠物。它负责：

- 理解角色来源、身份特征、风格和必须保留/禁止添加的元素；
- 在生成前给出中英文 prompt，并等待视觉设计确认；
- 确认主形象、显示名称、技术 ID 和 variant；
- 预演动作语义与 16 个视角的 mechanics；
- 生成并确认六帧 idle 原型；
- 产出 `studio-brief.json`，作为后续生产的唯一设计契约。

### `hatch-pet`

正式生产入口，适合把已批准的主形象制作成 Codex-compatible v2 宠物。它负责：

- 生成 9 个标准动画状态；
- 生成 16 个顺时针视角方向；
- 组装 `8×11` atlas，每个 cell 为 `192×208`；
- 执行透明背景、色键清理、边缘去污染、方向连续性和视觉 QA；
- 打包 `spriteVersionNumber: 2`，并在完整验收后安装；
- 不会自动切换当前正在使用的宠物。

## 推荐用法

完整流程如下：

```text
jarvis-pet-studio
    ↓ 用户确认主形象、动作和视角机制
hatch-pet
    ↓ 确定性组装、QA、打包
安装 Codex 宠物
```

### 1. 先设计和确认

在 Codex 中提出类似请求：

```text
帮我制作一个 Codex 宠物：一只穿实验服、性格可靠的橘猫。
风格偏 3D toy，主色为橙色和深蓝色。
```

`jarvis-pet-studio` 会先整理角色理解和中英文 prompt。确认 prompt 后才生成主形象。不要跳过主形象、动作语义和视角 mechanics 的确认。

### 2. 交给 hatch-pet 生产

设计阶段批准后，使用批准的主图和唯一的设计简报：

```bash
prepare_pet_run.py \
  --approved-base /absolute/path/approved.png \
  --studio-brief /absolute/path/studio-brief.json
```

`studio-brief.json` 至少应包含：

```json
{
  "source_character": "角色来源或原创设定",
  "source_interpretation": "本次采用的角色理解",
  "design_axes": ["风格", "比例", "材质", "配色"],
  "identity_lock": {
    "must_preserve": ["必须保留的身份特征"],
    "must_not_add": ["禁止添加的元素"]
  },
  "action_contract": {},
  "look_mechanics": {},
  "animation_energy": "动作能量描述",
  "naming": {
    "display_name": "显示名称",
    "technical_id": "技术 ID",
    "variant": "版本或变体"
  },
  "approvals": {}
}
```

运行 bundled scripts 前，必须先加载 workspace dependencies，并使用工具返回的 Python 路径；不要使用裸 `python` 替代：

```text
load_workspace_dependencies
```

## 输入和输出

输入可以是：

- 文字角色设定；
- 用户提供的参考图；
- 已批准的主形象；
- 已有的 v1/v2 atlas（用于验证、升级或修复）。

完整生产结果通常包括：

- `studio-brief.json`：设计源文件；
- `8×11` v2 atlas；
- contact sheet 和动画预览；
- 透明度、色键、方向和 atlas 验证报告；
- 可安装的 Codex pet 包。

## 重要约束

- 不要让图像模型直接生成完整的 `8×11` atlas；atlas 必须由确定性脚本组装。
- 不要在未确认主形象前生成完整动画。
- `running-left` 只有在 `running-right` 通过检查后才可镜像；不适合镜像时应重新生成。
- 透明背景中不得有内部意外透明洞、色键污染、悬浮装饰、文字、UI 或可读 logo。
- `000` 视角表示向上，不是正面 neutral frame。
- 只安装完整通过确定性和视觉 QA 的版本；不要自动选为当前宠物。
- 原始生成图应按本机 Codex 归档规则保留。

## 目录结构

```text
jarvis-pet-studio/
├── SKILL.md
└── agents/openai.yaml

hatch-pet/
├── SKILL.md
├── LICENSE.txt
├── agents/openai.yaml
├── references/
├── scripts/
└── tests/
```

## Skill 入口

- [jarvis-pet-studio/SKILL.md](jarvis-pet-studio/SKILL.md)
- [hatch-pet/SKILL.md](hatch-pet/SKILL.md)

