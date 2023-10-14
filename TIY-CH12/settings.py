class Settings:
    '''A class to store all settings for alien invasion game'''

    def __init__(self):
        '''Initialize the game's settings.'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.ship_speed = 2.0
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = (0, 230, 0)
        self.bullets_allowed = 5
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        self.rock_speed = 3.0
        self.rock_fleet_drop_speed = 10
        self.rock_fleet_direction = 1
                