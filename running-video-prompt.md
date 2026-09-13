# running-right — video prompt

## 建议参数

- 模式：首尾帧（Frame A + Frame B）
- 时长：2 秒
- 画幅：16:9 横屏
- 运动强度：低
- 镜头：固定

## Prompt

```text
2D hand-drawn anime illustration style, flat cel-shaded coloring, clean visible outlines.

Morgana from Persona 5 runs smoothly toward screen-right for one compact looping cycle. Keep the character centered in place while the legs and arms alternate naturally. The body makes only a small vertical bounce. The yellow scarf tips and white-tipped tail trail behind with restrained secondary motion. Preserve the exact face, visible blue eye, black-and-white markings, proportions, utility belt, pouches, line thickness and colors from the supplied first and last frames. Fixed camera, fixed scale, pure white background, low motion intensity, seamless loop.

Do not generate five paws. No extra limbs, no direction change, no camera movement, no zoom, no crop, no props, no speed lines, no effects, no 3D, no CGI, no photorealism, no plastic or Pixar-like rendering.
```

左跑行不重复生成：右跑视频通过确定性水平翻转后用于 `running-left`，以确保轮廓、帧时序与动作节奏完全一致。
