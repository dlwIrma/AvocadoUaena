#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$ROOT_DIR/AvocadoUaena"
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/pets/AvocadoUaena"

if [[ ! -f "$SOURCE_DIR/pet.json" || ! -f "$SOURCE_DIR/spritesheet.webp" ]]; then
  echo "安装文件不完整，请重新下载发布包。 / Installation files are incomplete. Please download the release again." >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"
cp "$SOURCE_DIR/pet.json" "$TARGET_DIR/pet.json"
cp "$SOURCE_DIR/spritesheet.webp" "$TARGET_DIR/spritesheet.webp"

echo "牛油果爱娜已安装到：$TARGET_DIR"
echo "AvocadoUaena was installed to: $TARGET_DIR"
echo "请完全退出并重新打开 Codex，然后在宠物列表中选择“牛油果爱娜”。"
echo "Quit and reopen Codex, then select '牛油果爱娜' from the pet list."
