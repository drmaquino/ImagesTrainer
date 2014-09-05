from kivy.clock import Clock

class Timer:
    def __init__(self):
        self.time = 0.0
        self.state = 'stopped'
        self.direction = 'fwd'

    def increment_time(self, dt):
        self.time += dt

    def decrement_time(self, dt):
        self.time -= dt

    def start(self, direction='fwd' ):
        self.direction = direction
        if self.direction == 'fwd':
            Clock.schedule_interval(self.increment_time, 1 / 100.)
        elif self.direction == 'bwd':
            Clock.schedule_interval(self.decrement_time, 1 / 100.)
        self.state = 'running'

    def stop(self):
        if self.direction == 'fwd':
            Clock.unschedule(self.increment_time)
        elif self.direction == 'bwd':
            Clock.unschedule(self.decrement_time)
        self.state = 'stopped'

    def reset(self, time=0):
        self.time = time

    def get_time(self):
        return self.time