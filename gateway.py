# exit animation
import pygame as pg


class Gateway:
    def __init__(self,sprite_sheet_path):
        self.sprite_sheet = pg.image.load(
            sprite_sheet_path
        ).convert_alpha()

        self.frame_width = 40
        self.frame_height = 40
        self.frame_count = 3

        self.frames = []

        for frame_index in range(self.frame_count):
           frame_rect = pg.Rect(frame_index * self.frame_width,
                                0,
                                self.frame_width, self.frame_height,
                                )
           frame = self.sprite_sheet.subsurface(frame_rect).copy()
           self.frames.append(frame)