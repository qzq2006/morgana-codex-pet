# 动画生产与交付

关键帧已完成身份终审。下一步必须用支持首尾帧的 AI 视频工具制作 8 段短视频；`running-left` 会从 `running-right` 确定性镜像生成。

## 统一参数

- 首尾帧模式：Frame A + Frame B
- 画幅：16:9 横屏
- 时长：2 秒（idle 可用 2–3 秒）
- 镜头：固定
- 运动强度：低或极低
- 背景：纯白
- 输出：MP4，保持角色完整且居中

## 文件清单

| 输出视频 | 首帧 | 尾帧 | 提示词 |
|---|---|---|---|
| `videos/idle.mp4` | `source-frames/idle-frame-a.png` | `source-frames/idle-frame-b.png` | `video-prompt.md` |
| `videos/running-right.mp4` | `source-frames/running-right-frame-a.png` | `source-frames/running-right-frame-b.png` | `running-video-prompt.md` |
| `videos/waving.mp4` | `source-frames/waving-frame-a.png` | `source-frames/waving-frame-b.png` | `batch2-video-prompts.md` |
| `videos/jumping.mp4` | `source-frames/jumping-frame-a.png` | `source-frames/jumping-frame-b.png` | `batch2-video-prompts.md` |
| `videos/failed.mp4` | `source-frames/failed-frame-a.png` | `source-frames/failed-frame-b.png` | `batch3-video-prompts.md` |
| `videos/waiting.mp4` | `source-frames/waiting-frame-a.png` | `source-frames/waiting-frame-b.png` | `batch3-video-prompts.md` |
| `videos/running.mp4` | `source-frames/running-frame-a.png` | `source-frames/running-frame-b.png` | `batch4-video-prompts.md` |
| `videos/review.mp4` | `source-frames/review-frame-a.png` | `source-frames/review-frame-b.png` | `batch4-video-prompts.md` |

如果视频工具只能导出逐帧 PNG，可将序列放到 `videos/<状态>/frame-0001.png` 等目录中。

## 自动加工

8 段视频齐全后运行：

```powershell
python tools/process_animations.py
```

脚本会均匀抽取 Codex 需要的帧数，镜像生成左跑，生成 59×64 contact/GIF，抠除白底，拼装 1536×1872 图集，并生成 `package/pet.json`。

检查 `qa/animations/` 中的 GIF 与 contact sheet。身份、肢体数量、循环连续性和透明边缘都通过后，运行：

```powershell
powershell -ExecutionPolicy Bypass -File tools/install_codex_pet.ps1
```
