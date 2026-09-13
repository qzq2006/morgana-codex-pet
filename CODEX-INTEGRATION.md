# Codex integration

本机安装的 Codex 26.908.4834 支持两种自定义桌宠图集：

- v1：1536×1872，8 列 × 9 行；
- v2：1536×2288，8 列 × 11 行。

本项目采用兼容面更稳的 v1。每格固定为 192×208。

| 行 | 素材目录 | Codex 状态 | 必需帧 |
|---:|---|---|---:|
| 0 | `idle` | 待机 | 6 |
| 1 | `running-right` | 向右跑 | 8 |
| 2 | `running-left` | 向左跑 | 8 |
| 3 | `waving` | 挥手 | 4 |
| 4 | `jumping` | 跳跃 / 悬停反馈 | 5 |
| 5 | `failed` | 失败 | 8 |
| 6 | `waiting` | 等待用户输入或确认 | 6 |
| 7 | `running` | Codex 执行中 | 6 |
| 8 | `review` | 审查 / 整理结果 | 6 |

将各状态的透明 PNG 帧放入 `rows/<状态>/frame-01.png` 起的连续文件。执行：

```powershell
python tools/build_codex_sheet.py
```

构建器会检查尺寸、必需帧、可见像素和透明背景。全部通过后生成：

- `package/spritesheet.png`
- `package/pet.json`

再运行：

```powershell
powershell -ExecutionPolicy Bypass -File tools/install_codex_pet.ps1
```

安装位置是 `%USERPROFILE%\.codex\pets\morgana`。重启 Codex 后，在“设置 → 个性化 → 桌宠”中选择 Morgana。

公开的 OpenAI Docs 当前没有列出自定义桌宠图集协议；这里的尺寸、帧数和清单字段来自本机 Codex 客户端实现。升级客户端后应重新验收。

