import pygame
import pygame.image
import pygame.sprite
import pygame.transform
import pygame.mixer

from setting import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, filename, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.game = game
        self.spritesheet = pygame.image.load(filename)
        self.image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.right_image = pygame.transform.flip(self.image, 0, 0)
        self.left_image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.vx = 0
        self.vy = 0
        self.grounded = False
        self.left_direction = False

    def jump(self):
        if self.grounded == True:
            self.game.jump_sound.play()
            self.vy = JUMP_POWER
            self.grounded = False

    def small_jump(self):
        self.vy = JUMP_POWER //2

    def update(self):
        self.keys = pygame.key.get_pressed()
        # もしみぎのボタンをおしたら
        if self.keys[pygame.K_RIGHT]:
            self.vx=SPEED
        # もしひだりのボタンをおしたら
        elif self.keys[pygame.K_LEFT]:
            self.vx=-SPEED
        # それいがいのとき
        else:
            self.vx=0
        
        if self.keys[pygame.K_SPACE]:
            self.jump()

        if not self.grounded:
            self.vy += GRAVITY
        self.check_collision_x()
        self.check_collision_y()
        self.check_enemy_collision()
        self.check_goal_collsion()
        self.set_direction()
        self.prev_button = self.keys[pygame.K_SPACE]


    def set_direction(self):
        if self.left_direction == True:
            self.image = self.left_image
        elif self.left_direction == False:
            self.image = self.right_image


    def check_collision_x(self):
        new_x = self.rect.x + self.vx
        new_rect = pygame.Rect(new_x, self.rect.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        for block in self.game.block_sprites:
            collide = new_rect.colliderect(block.rect)
            if collide:
                if self.vx > 0:
                    self.rect.x = block.rect.left - PLAYER_WIDTH
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.x = block.rect.right
                    self.vx = 0
                break
            else:
                self.rect.x = new_x


    def check_collision_y(self):
        new_y = self.rect.y + self.vy
        new_rect = pygame.Rect(self.rect.x, new_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        for block in self.game.block_sprites:
            collide = new_rect.colliderect(block.rect)
            if collide:
                if self.vy > 0:
                    self.rect.y = block.rect.top - PLAYER_HEIGHT
                    self.vy = 0
                    if self.prev_button != self.keys[pygame.K_SPACE]:
                        self.grounded = True
                elif self.vy < 0:
                    self.rect.y = block.rect.bottom
                    self.vy = 0
                break
            else:
                self.rect.y = new_y
                self.grounded = False

    def check_enemy_collision(self):
        for enemy in self.game.enemy_sprites:
            collide = self.rect.colliderect(enemy.rect)
            if collide:
                if self.rect.y < enemy.rect.y - OBJECT_SIZE //2:
                    self.game.bump_sound.play()
                    enemy.kill()
                    self.vy = JUMP_POWER // 2
                else:
                    self.kill()
                    self.game.playing = False
                    print("ゲームオーバー：", self.game.playing)

    def check_goal_collsion(self):
        collide = self.rect.colliderect(self.game.goal.rect)
        if collide:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join(SOUND_DIR, GAMECLEAR_BGM))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            self.game.new()




class Block(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.spritesheet = pygame.image.load(filename).convert()
        self.image.blit(self.spritesheet, (0,0), (x, y, width, height))
        color_key = self.image.get_at((0,0))
        self.image.set_colorkey(color_key)
        self.image = pygame.transform.scale(self.image, (OBJECT_SIZE, OBJECT_SIZE))
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.topleft = (x, y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load(filename)
        self.image = pygame.Surface((width, height))
        self.image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        color_key = self.image.get_at((0, 0))
        self.image.set_colorkey(color_key)
        self.image = pygame.transform.scale(self.image, (OBJECT_SIZE, OBJECT_SIZE))
        self.vx = -1
        self.moving_area = 0

        self.right_image = pygame.transform.flip(self.image, 0, 0)
        self.left_image = pygame.transform.flip(self.image, 1, 0)

        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def update(self):
        if abs(self.moving_area) >= 200:
            self.vx *= -1

        self.moving_area += self.vx
        self.rect.x += self.vx