import sys #Use tools in the sys module to exit game when player quits
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from rocks import Rock
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''Overall class to manage game assets and behavior'''

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()       
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) #display.set_mode represents the entire game window
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()

        self._create_fleet()
        self._create_star_fleet()
        self._create_rock_fleet()

        self.game_active = False

        self.play_button = Button(self, "Play")

    '''Start the main loop for the game'''
    '''The game is controlled by the run game method'''
    def run_game(self):
        while True:
             self._check_events()

             if self.game_active:
                  
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_rocks()
             self.bullets.update()
             self._update_screen()

             
             #print(len(self.bullets))
             
            #Pygame will try its best to make the loop run exactly 60 times per second
             self.clock.tick(60)
            
    def _check_events(self):
        #Watch for keyboard and mouse events(events are actions).
            #pygame.event.get returns a list of events that have taken place since the last time this function-
            #was called
            for event in pygame.event.get(): 
                #if statement to respond to specific events
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                      self._check_keydown_events(event)                                         
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
         '''Start a new game when the player clicks play.'''
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.game_active:
              self.stats._reset_stats()
              self.sb.prep_score()
              self.sb.prep_level()
              self.sb.prep_ships()
              self.game_active = True

              self.bullets.empty()
              self.aliens.empty()

              self._create_fleet()
              self.ship.center_ship()

              pygame.mouse.set_visible(False) 

              self.settings.initialize_dynamic_settings()
         
                    
                     
    '''Method that responds to key presses'''
    def _check_keydown_events(self, event):
        #right arrow key == pygame.K_RIGHT
        if event.key == pygame.K_RIGHT:
            #Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
             sys.exit()
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()
        elif event.key == pygame.K_p:
             mouse_pos = pygame.mouse.get_pos()
             self._check_play_button(mouse_pos)
    '''Method that responds to key releases'''
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    
    def _fire_bullet(self):
         '''Create a new bullet and add it to the bullets group'''
         if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
         #update bullet position
         #get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,
                                                True)
        if not self.aliens:
              self.bullets.empty()
              self._create_fleet()
              self.settings.increase_speed()
        
        if collisions:
          for aliens in collisions.values():
             self.stats.score += self.settings.alien_points *len(aliens)
          self.sb.prep_score()
          self.sb.check_high_score()
        
        if not self.aliens:
             self.bullets.empty()
             self._create_fleet()
             self.settings.increase_speed()


             self.stats.level += 1
             self.sb.prep_level()
        

        #check for any bullets that have hit aliens.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,
                                                 True)



    def _create_fleet(self):
         '''Create the fleet of aliens'''
         alien = Alien(self)
         #alien width from first alien created
         alien_width, alien_height = alien.rect.size 

         current_x, current_y = alien_width, alien_height
         while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width -4 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 4 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
         new_alien = Alien(self)
         new_alien.x = x_position
         new_alien.rect.x = x_position
         new_alien.rect.y = y_position
         self.aliens.add(new_alien)

    def _check_fleet_edges(self):
         '''Respond appropriately if any aliens have reached an edge'''
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
    
    def _change_fleet_direction(self):
         '''Drop the entire fleet and change the fleet's direction'''
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed
         self.settings.fleet_direction *= -1

    def _ship_hit(self):
         if self.stats.ships_left > 0:
         #Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

         #get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

         #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

         #pause
            sleep(0.5)
         else:
              self.game_active = False
              pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= self.settings.screen_height:
                   self._ship_hit()
                   break

    def _update_aliens(self):
         #Update the positions of all aliens in the fleet.
         self._check_fleet_edges()
         self.aliens.update()
         #look for alien-ship collisions
         if pygame.sprite.spritecollideany(self.ship, self.aliens):
              self._ship_hit()

         self._check_aliens_bottom()

    def _create_star_fleet(self):
         star_width = Star(self).rect.width
         screen_width = self.settings.screen_width
         screen_height = self.settings.screen_height

         for _ in range(30):
              new_star =Star(self)
              new_star.rect.x = randint(0, screen_width - star_width)  # Random x coordinate
              new_star.rect.y = randint(0, screen_height - star_width)  # Random y coordinate
              self.stars.add(new_star)   

    def _create_rock_fleet(self):
         '''Create the fleet of aliens.'''
         #Create an alien and keep adding aliens until the's no room left.
         #Spacing between aliens is on alien width
         #Make an alien.

         rock = Rock(self)
         rock_width, rock_height = rock.rect.size
         rock_width = rock.rect.width

         current_x, current_y = rock_width, rock_height
         while current_y < (self.settings.screen_height -5 * rock_height):
            while current_x < (self.settings.screen_width - 5 * rock_width):
                self._create_rock(current_x, current_y)
                current_x += 5 * rock_width

                #Finished a row; reset x value, and increment y value.
            current_x = rock_width
            current_y += 5 * rock_height
         
    def _create_rock(self, x_position, y_position):
         new_rock = Rock(self)
         new_rock.x = x_position
         new_rock.rect.x = x_position
         new_rock.rect.y = y_position
         self.rocks.add(new_rock)


    def _check_rock_fleet_edges(self):
         for rock in self.rocks.sprites():
              if rock.check_edges():
                self._change_rock_fleet_direction()
                break
              
    def _change_rock_fleet_direction(self):
         '''Drop the entire fleet and change the fleet's direction'''
         for rock in self.rocks.sprites():
              rock.rect.y += self.settings.rock_fleet_drop_speed
         self.settings.rock_fleet_direction *= -1

    def _update_rocks(self):
         self._check_rock_fleet_edges()
         self.rocks.update() 



    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)
        self.rocks.draw(self.screen)

        self.sb.show_score()
        if not self.game_active:
             self.play_button.draw_button()

        for bullet in self.bullets.sprites():
             bullet.draw_bullet()

        #Make the most recently drawn screen visible.
        pygame.display.flip()
        
if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()