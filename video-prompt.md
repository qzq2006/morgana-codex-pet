# idle breathing — video prompt

## 建议参数

- 模式：首尾帧（Frame A + Frame B）
- 时长：2–3 秒
- 画幅：16:9 横屏
- 运动强度：低
- 镜头：固定
- 循环：开启；若工具没有循环开关，要求首尾平滑衔接

## Prompt

```text
2D hand-drawn anime illustration style, flat cel-shaded coloring, clean visible outlines.

Morgana from Persona 5 performs one tiny, calm idle breathing cycle. His upper chest and shoulders rise and fall subtly. The yellow scarf tips lift only a little with the breath. The white-tipped tail makes one very small smooth curve and returns. Keep the full body centered and fully visible. Fixed camera, fixed scale, fixed white background, low motion intensity. Preserve the exact face, huge blue eyes, black-and-white markings, body proportions, costume, belt, pouches, line thickness and colors from the supplied first and last frames. Seamless gentle loop.

Do not generate five paws. No extra limbs, no blinking, no mouth movement, no walking, no waving, no camera movement, no zoom, no crop, no props, no effects, no background change, no 3D, no CGI, no photorealism, no plastic or Pixar-like rendering.
```

## 失败时的简化版

如果首尾帧模式出现缩放或构图漂移，只输入 `idle-frame-a.png`，改用单图 i2v：

```text
2D hand-drawn anime illustration style, flat cel-shaded coloring, clean visible outlines. Morgana makes one tiny calm breathing motion while standing still. Keep his feet, head, face, eyes, arms, belt and camera completely fixed. Only the chest, scarf tips and tail tip move very slightly. Seamless loop. Do not generate five paws. No 3D, CGI, photorealism, plastic, camera movement, crop, props or effects.
```

