---
title: From-Scratch CPU game engine in Rust
keywords: [Computer Graphics, Rust, Vision, Game Engine]
description: A 3D world renderer written from scratch in Rust, without any vision library such as OpenGL or Vulkan.
priority: 1
featuredImage: images/engine.png
---

# Custom Game Engine framework

*WORK IN PROGRESS*

I the quest for a new project, I have decided to program a Doom game. When I explored the several options in Rust to write OpenGL or Vulkan bindings, I was slightly disappointed. I though it would a great idea to try and **write a custom game engine**. Since it is quite a challenging piece of work, I limited myself to a **CPU engine** (no hardware acceleration *yet*).

The current state of the engine is to display any kind of cube-base objects, supporting textures. To render 3D objects, I work at the pixel level : for each pixel of the screen, I perform **ray-tracing** to determine *which face is the closest to the camera*. Once a face is determined, I use its texture to determine which RGB color must be written at this pixel. I am currently working on **binary space partitioning** to accelerate the visual processing when there are hundreds / thousands of objects to display.

When this will be finished, I will use it to write my own **Doom**.
