# 牛油果爱娜 · AvocadoUaena

一只以牛油果为灵感、腹部装饰着荧光黄与紫色交织 UAENA logo 的 Codex Desktop v2 动画宠物。

An animated v2 pet for Codex Desktop, inspired by an avocado and decorated with a fluorescent yellow-and-purple UAENA logo.

> 非官方粉丝作品，与 OpenAI、IU 官方及 UAENA 官方无隶属或合作关系，仅供个人非商业使用。
>
> This is an unofficial fan work with no affiliation or partnership with OpenAI, IU, or official UAENA organizations. For personal, non-commercial use only.

## 动作预览 · Animation Preview

| 待机 · Idle | 向右移动 · Move Right | 向左移动 · Move Left |
| --- | --- | --- |
| <img src="previews/gif/01-idle.gif" width="240"> | <img src="previews/gif/02-running-right.gif" width="240"> | <img src="previews/gif/03-running-left.gif" width="240"> |

| 挥手 · Wave | 跳跃 · Jump | 失败 · Failed |
| --- | --- | --- |
| <img src="previews/gif/04-waving.gif" width="240"> | <img src="previews/gif/05-jumping.gif" width="240"> | <img src="previews/gif/06-failed.gif" width="240"> |

| 等待你 · Waiting | 执行任务 · Working | 审查 · Review |
| --- | --- | --- |
| <img src="previews/gif/07-waiting.gif" width="240"> | <img src="previews/gif/08-running.gif" width="240"> | <img src="previews/gif/09-review.gif" width="240"> |

## 中文安装说明

### 方法一：下载发布包

1. 打开仓库右侧的 **Releases**。
2. 下载 `AvocadoUaena-v1.0.0.zip` 并解压。
3. 将解压得到的整个 `AvocadoUaena` 文件夹复制到：

   ```text
   ~/.codex/pets/
   ```

4. 完全退出并重新打开 Codex，在宠物列表中选择“牛油果爱娜”。

### 方法二：克隆仓库后安装

```bash
git clone https://github.com/dlwIrma/AvocadoUaena.git
cd AvocadoUaena
./install.sh
```

## Installation in English

### Option 1: Download the release

1. Open **Releases** on the right side of this repository.
2. Download and extract `AvocadoUaena-v1.0.0.zip`.
3. Copy the entire extracted `AvocadoUaena` folder to:

   ```text
   ~/.codex/pets/
   ```

4. Quit and reopen Codex, then select “牛油果爱娜” from the pet list.

### Option 2: Clone and install

```bash
git clone https://github.com/dlwIrma/AvocadoUaena.git
cd AvocadoUaena
./install.sh
```

## 安装结构 · Package Structure

```text
~/.codex/pets/AvocadoUaena/
├── pet.json
└── spritesheet.webp
```

图集使用 Codex v2 规范：8×11 网格、单格 192×208、完整图集 1536×2288。

The atlas follows the Codex v2 format: an 8×11 grid, 192×208 cells, and a full size of 1536×2288.

## 卸载 · Uninstall

完全退出 Codex 后，删除 `~/.codex/pets/AvocadoUaena/`，然后重新打开 Codex。

Quit Codex, delete `~/.codex/pets/AvocadoUaena/`, and reopen Codex.
