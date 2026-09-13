# Morgana desktop pet

摩尔加纳 Codex 桌宠项目。9 个 Codex 状态已完成动画、实际尺寸 QA、v1 图集构建和本机安装。

## 当前文件

- `references/morgana-official.png`：ATLUS 官方角色页视觉参考，仅作为身份锚点。
- `source-frames/`：8 个生成状态的 Frame A / Frame B。
- `video-prompt.md`、`running-video-prompt.md`、`batch*-video-prompts.md`：全部视频提示词。
- `VIDEO-PRODUCTION.md`：使用外部视频模型时的可选生产说明。
- `qa/`：已通过的 59×64 关键帧对照图。
- `qa/final-contact.png`：9 个状态的最终实际尺寸接触表。
- `qa/package-verification.json`：尺寸、透明度、边界、帧运动与镜像验证报告。
- `tools/synthesize_tween_animations.py`：从已批准 A/B 帧生成确定性光流循环。
- `tools/process_animations.py`：抽帧、镜像左跑、QA 与图集构建入口。
- `CODEX-INTEGRATION.md`：Codex v1 图集协议与安装说明。

## 下一步

```powershell
python tools/synthesize_tween_animations.py
python tools/process_animations.py
python tools/verify_package.py
powershell -ExecutionPolicy Bypass -File tools/install_codex_pet.ps1
```

安装目录为 `%USERPROFILE%\.codex\pets\morgana`。本机 Codex 配置已选择 `custom:morgana` 并启用桌宠显示。

## 参考来源

角色视觉参考来自 [《Persona 5》官方摩尔加纳角色页](https://persona5.jp/sp/character/morgana.html)。角色及相关商标归 ATLUS / SEGA 所有；本目录产物按个人非商业同人桌宠用途准备。
