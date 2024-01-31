# importing pygame module
import pygame
import time
import random
import sys

from enum import Enum # VER ESTO

from enemy import Enemy
from hero import Hero

from collections import namedtuple #???

# Reset function: Agent needs to be able to reset the game
# reward: Agent reward
# play(action) -> direction:  play function gets an action and returns a direction
# frame_iteration
# is_colission to detect a colission :P



# y crece hacia abajo
# x crece hacia la derecha


pygame.init()
pygame.font.init()
FONT = pygame.font.Font(None, 36)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5

Point = namedtuple('Point', 'x, y')


class AstroDestroyer:
    def __init__(self, canvas_w=600, canvas_h=600):
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        
        #init display
        self.display = pygame.display.set_mode((self.canvas_w, self.canvas_h))
        pygame.display.set_caption('AstroDestroyer')
        self.clock = pygame.time.Clock()

        # Parameters: Hero
        self.hero_color = pygame.Color("white")
        # Parameters: Enemy
        self.enemy_color = pygame.Color("red")
        self.default_enemy_width = 10
        self.default_enemy_height = 10
        self.hp_multiplier = 30
        self.enemy_base_speed = 1
        self.new_enemy_delay = 1
        self.last_enemy_t = time.time()
        # Parameters: Bullet
        self.bullet_color = pygame.Color("yellow")
        self.bullet_damage = 400
        self.bullet_size = 2
        self.bullet_speed = 4
        self.new_bullet_delay = 0.05
        self.last_bullet_t = time.time()

        # These will be reseted by reset()
        # Initialize hero
        self.hero = Hero(x=150,
            y=150,
            width=30,
            height=30,
            step=10,
            color=self.hero_color,
            bullet_size=self.bullet_size)
        self.direction = Direction.NONE
        
        # Initialize enemies
        self.enemies = []
        self.destroyed_enemies = 0

        # Initialize bullets
        self.bullets = []
        self.throw_megabomb = False

        # Game state
        self.score = 0
        self.frame_iteration = 0

    def reset(self):
        # Initialize hero
        self.hero = Hero(x=150,
            y=150,
            width=30,
            height=30,
            step=10,
            color=self.hero_color,
            bullet_size=self.bullet_size)
        self.direction = Direction.NONE
        
        # Initialize enemies
        self.enemies = []
        self.destroyed_enemies = 0

        # Initialize bullets
        self.bullets = []
        self.throw_megabomb = False

        # Game state
        self.score = 0
        self.frame_iteration = 0

    def log_info(self):
        if self.frame_iteration % 100 == 0:
            print(f"iteration {self.frame_iteration}, num bullets {len(self.bullets)}, num enemies {len(self.enemies)}, score {self.score}, destroyed_enemies {self.destroyed_enemies}")

    def _move_hero(self, direction):
        if direction == Direction.UP: #UP
            self.hero.y = max(self.hero.y - self.hero.step, 0)
        elif direction == Direction.DOWN: # DOWN
            self.hero.y = min(self.hero.y + self.hero.step, self.canvas_h - self.hero.h)
            # self.hero.y += self.hero.step
        elif direction == Direction.LEFT: # LEFT
            self.hero.x = max(self.hero.x - self.hero.step, 0)
            # self.hero.x -= self.hero.step
        elif direction == Direction.RIGHT: # RIGHT
            # self.hero.x += self.hero.step
            self.hero.x = min(self.hero.x + self.hero.step, self.canvas_w - self.hero.w)

    def is_collision(self):
        for enemy in self.enemies:
            if not enemy.destroyed:
                enemy.draw(self.display)

                # check hero collision
                if enemy.hero_collision:
                    self.hero.color = pygame.Color("red")
                    print("CRASH CTM")
                    # still_playing = False
                    my_font = pygame.font.SysFont('Comic Sans MS', 30)
                    text_surface = my_font.render('Some Text', False, (0, 0, 0))
                    self.display.blit(text_surface, (0,0))

                    return True
        return False

    def _new_bullet(self):
        t_now = time.time()
        if t_now - self.last_bullet_t >= self.new_bullet_delay:
            self.last_bullet_t = t_now
            self.bullets.append(self.hero.new_bullet())
    
    def _new_enemies(self):
        t_now = time.time()
        if t_now - self.last_enemy_t >= self.new_enemy_delay:
            self.last_enemy_t = t_now

            new_enemies = random.randint(1, 5)
            for _ in range(0, new_enemies):
                new_enemy = Enemy(
                                    x=self.canvas_w + random.randint(0, 50),
                                    y=random.randint(20, 580),
                                    size=self.default_enemy_width + random.randint(0, 10),
                                    hp_multiplier=self.hp_multiplier)
                self.enemies.append(new_enemy)

    def _damage_enemies(self):
        if self.throw_megabomb:
            self._mega_bomb()
            self.throw_megabomb = False
        else:
            for enemy in self.enemies:
                delete_bullets = []
                for i, bullet in enumerate(self.bullets):
                    # check bullet collision
                    if not enemy.destroyed:
                        if enemy.x <= bullet[0] <= enemy.x + enemy.size:
                            if enemy.y <= bullet[1] <= enemy.y + enemy.size:
                                enemy.update_hp(self.bullet_damage)
                                delete_bullets.append(i)

                                if enemy.destroyed:
                                    self.destroyed_enemies += 1
                                    if enemy.errante:
                                        self.score += enemy.size*2
                                    # else:
                                    #     self.score += enemy.size

                self.bullets = [b for i,b in enumerate(self.bullets) if i not in delete_bullets]

    def _mega_bomb(self):
        self.enemies = []

    def _update_ui(self):
        # Update UI and CLOCK
        # Completely fill the surface object with black colour  
        self.display.fill((0, 0, 0))
        
        # Draw Hero
        self.hero.draw(self.display)

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(self.display, self.bullet_color, bullet)

        # Draw enemies
        for enemy in self.enemies:
            if not enemy.destroyed:
                enemy.draw(self.display)

        # Set up the font object
        score_text = FONT.render(f'Score: {self.score}', True, (255, 255, 0))
        self.display.blit(score_text, (10, 10))

    def play_step(self):
        # print("pixels hero", self.display.get_at((self.hero.x, self.hero.y)))

        self.frame_iteration += 1
        move_event = False
        # Get action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # -----------------------------
            # SECCION DE USUARIO
            # checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
                # Key to quit game
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_TAB:
                    pygame.quit()
                    sys.exit()
                # Key to reset
                if event.key == pygame.K_r:
                    self.reset()
                # Direction
                if event.key == pygame.K_UP:
                    move_event = True
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    move_event = True
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    move_event = True
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    move_event = True
                    self.direction = Direction.RIGHT
                
                # # Special Attack
                # if event.key == pygame.K_SPACE:
                #     self.throw_megabomb = True
            # Fin seccion de usuario
            # -----------------------------

        # ACTION
        # Move Hero
        if move_event:
            self._move_hero(self.direction)

        # UPDATE EVERYTHING ELSE
        # Move bullets
        self._new_bullet()
        self.bullets = [(bullet[0] + self.bullet_speed, bullet[1], bullet[2], bullet[3]) for bullet in self.bullets if bullet[0] + self.bullet_speed < self.canvas_w]

        # Move enemies
        self._new_enemies()
        # Move enemies
        for e in self.enemies:
            e.move(self.enemy_base_speed, self.hero.x, self.hero.y, self.hero.w, self.hero.h)
        
        self.enemies = [e for e in self.enemies if not e.left_screen]

        # Damage enemies
        self._damage_enemies()

        # Check game over
        reward = 0
        game_over = False
        if self.is_collision():# or self.frame_iteration > ....
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Update UI
        self._update_ui()

        pygame.display.update()
        self.clock.tick(100)

        # Return game over and score
        return reward, game_over, self.score

if __name__ == '__main__':
    game = AstroDestroyer()
    while True:
        reward, game_over, score = game.play_step()

        # get the state from the pixels
        # During its lifetime, the PixelArray locks the surface, thus you explicitly have to delete it once its not used anymore and the surface should perform operations in the same scope.
        state_blit = pygame.surfarray.pixels3d(game.display)
        state = state_blit.copy()
        del state_blit

        # STATE: ndarray 600x600x3

        game.log_info()
        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()