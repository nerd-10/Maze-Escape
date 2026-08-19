# Maze Escape

A lightweight **DOOM-inspired first-person maze game** built from scratch using **Python + Pygame**.

The project focuses on learning **raycasting, procedural maze generation, game loops, collision detection, texture rendering, and basic game-engine architecture**.

## Gameplay

The player is placed inside a randomly generated maze and must find the **Ancient Gateway** as quickly as possible.

```text
Generate Maze
     ↓
Explore
     ↓
Find Gateway
     ↓
Record Time
     ↓
Generate New Maze
     ↓
Repeat
```

The goal is to improve completion times across randomly generated mazes.

## Scope

### Included

* Procedurally generated mazes
* First-person movement and camera
* Raycasting renderer
* Wall, floor and ceiling rendering
* Multiple wall textures
* Ancient Gateway
* Gateway animation
* Timer
* Endless maze loop
* Performance optimization

### Not Included

* Enemies
* Combat
* Weapons
* Health
* Inventory
* Keys / locked doors
* NPCs
* Multiplayer
* Audio
* Complex menus

The scope is intentionally limited to keep the project focused and lightweight.

## Tech Stack

* **Python**
* **Pygame**
* Raycasting
* Procedural generation

## Project Structure

```text
maze-escape/
├── assets/
├── src/
│   ├── main.py
│   ├── game.py
│   ├── player.py
│   ├── maze.py
│   ├── raycaster.py
│   └── settings.py
├── README.md
└── requirements.txt
```

## Goal

Build a small first-person engine from scratch and understand the underlying mathematics and systems instead of relying on an existing 3D engine.
