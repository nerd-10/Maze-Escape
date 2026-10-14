# sprite animation


class Animation:
    def __init__(self, frames, frame_duration=0.3):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.current_time = 0
        self.elapsed_time = 0.0

    def update(self, dt):
        self.elapsed_time += dt

        if self.elapsed_time >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.elapsed_time -= self.frame_duration

    def get_current_frame(self):
        return self.frames[self.current_frame]