# Texture loading
import os

import pygame as pg


class TextureManager:
    def __init__(self, floor_path, wall_directory):
        self.floor_path = floor_path
        self.wall_directory = wall_directory

        self.wall_textures = []
        self.floor_texture = None

    def load_texture(self):
        self.floor_texture = pg.image.load(
            self.floor_path
        ).convert()

        wall_filenames = [
            *(f"brick_wall_texture_{i}.png" for i in range(1,8)),
            "moss_texture.png",
            "moss_texture_2.png",
            "moss_wall_texture.png"
        ]
        for filename in wall_filenames:
            path = os.path.join(self.wall_directory, filename)
            texture = pg.image.load(path).convert()
            self.wall_textures.append(texture)