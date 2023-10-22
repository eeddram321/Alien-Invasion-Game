class Settings:
    '''A class to store all settings for alien invasion game'''

    def __init__(self):
        '''Initialize the game's settings.'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        #self.ship_speed = 2.0
        self.ship_limit = 4
        #self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = (0, 230, 0)
        self.bullets_allowed = 5
        #self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.4
        self.initialize_dynamic_settings()
        #fleet_direction of 1 represents right; -1 represents left
        #self.fleet_direction = 1
        self.rock_speed = 3.0
        self.rock_fleet_drop_speed = 10
        self.rock_fleet_direction = 1

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

                