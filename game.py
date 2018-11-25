## @file game.py
#  Source file for game class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/14/19

import pygame
import os.path
import sys
import random
from text import Text
from player import Player
from enemy import Enemy
from shot import Shot
from health import Health
from pygame.locals import *
import constants as const
from enemy_shot import Enemy_shot
from recover_health import Recover_health
import check_constants as checks


## @class Game
#  @brief Runs the game session and manages all actors
class Game:

    ## Constructor
    #  @post: Game components have been initialized
    def __init__(self):

        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Initialize member variables
        self.screen = pygame.display.set_mode(const.SCREENRECT.size, 0)
        self.clock = pygame.time.Clock()
        self.quit = False
        self.enemy_count = 1
        self.enemy_shot_count = 1
        self.gameover = False
        self.score = 0

        # Setup Game Window
        icon = pygame.image.load('assets/images/player_ship.png')
        icon = pygame.transform.scale(icon, (60, 80))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Gallaga Clone')
        #pygame.mouse.set_visible(0)

        self.start_menu()

    ## Loads a start screen with clickable options
    #  @pre Game components have been initialized
    def start_menu(self):
        # Load black background
        self.screen.fill(const.BLACK)
        pygame.display.update()

        # Load text
        start_game = Text("START GAME", const.WHITE, (300, 100), self.run)
        test_game = Text("TEST GAME", const.WHITE, (300, 200))
        quit_game = Text("QUIT GAME", const.WHITE, (300, 300), self.quit_game)

        # Draw text on screen
        options = []
        for text in [start_game] + [test_game] + [quit_game]:
            render = text.draw(self.screen)
            options.append(render)

        # Draw screen
        pygame.display.update(options)

        exit_menu = False
        while not exit_menu:
            for event in pygame.event.get():
                if pygame.event.peek(QUIT):
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for text in [start_game] + [test_game] + [quit_game]:
                        if text.rect.collidepoint(pos):
                            exit_menu = True
                            text.action()

    ## Loads and scales object/game image
    #  @pre: image exists
    #  @param: filename, name of image to be loaded
    #  @param: width, desired width of image
    #  @param: height, desired height of image
    #  @returns: Surface object
    def load_image(self, filename, file_width, file_height):
        filename = os.path.join('assets/images', filename)
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (file_width, file_height))
        img.set_colorkey(img.get_at((0, 0)), RLEACCEL)
        return img.convert()

    ## Loads audio
    #  @param filename, name of audio to be loaded
    def load_audio(self, filename):
        sound = pygame.mixer.Sound('assets/audios/'+filename)
        return sound

    ## Runs the game session
    #  @pre: Game components have been initialized
    #  @post: Game has been exited properly
    def run(self):

        # Load Images
        background_img = pygame.image.load('assets/images/space.jpg')
        player_img = self.load_image('player_ship.png', 45, 65)
        enemy_img = self.load_image('enemy_spaceship.png', 26, 26)
        shot_img = self.load_image('missile1.png', 10, 24)
        health_img_3 = self.load_image('hearts_3.png', 60, 20)
        health_img_2 = self.load_image('hearts_2.png', 60, 20)
        health_img_1 = self.load_image('hearts_1.png', 60, 20)
        health_img_0 = self.load_image('hearts_0.png', 60, 20)
        enemy_shot_img = self.load_image('missile2.png', 10, 24)
        recover_health_img = self.load_image('hearts_1.png', 60, 20)

        # Load Background
        background = pygame.Surface(const.SCREENRECT.size)
        for x in range(0, const.SCREENRECT.width, background_img.get_width()):
            background.blit(background_img, (x, 0))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

        # load audio:
        shot_audio = self.load_audio('shot.wav')
        explode_audio = self.load_audio('explosion.wav')
        enemy_audio = self.load_audio('enemy.wav')
        gameover_audio = self.load_audio('gameover.wav')
        hit_audio = self.load_audio('hit.wav')
        power_up_audio = self.load_audio('power_up2.wav')
        # Should be music not sound
        #main_menu_audio = self.load_audio('main_menu.mp3')

        # Load and play background music
        pygame.mixer.music.load('assets/audios/background.wav')
        pygame.mixer.music.play(20)

        # Initialize Starting Actors
        player = Player(player_img)
        health = Health(health_img_3, player)
        recover_health = []
        enemies = [Enemy(enemy_img)]
        shots = []
        enemy_shots = []
        actors = []
        score_text = Text("Score 0", const.WHITE, (50, 25))

        #Moved the initial starting postion out of the loop and controlling back and forth
        x_dir = const.SCREENRECT.centerx
        hit_right = True
        hit_left = False

        # Game loop
        while player.alive and not self.quit:

            self.clock.tick(const.FPS)

            # Call event queue
            pygame.event.pump()

            # Process input
            key_presses = pygame.key.get_pressed()
            right = key_presses[pygame.K_RIGHT]
            left = key_presses[pygame.K_LEFT]
            shoot = key_presses[pygame.K_SPACE]
            exit = key_presses[pygame.K_q]

            # Check for quit conditions
            if pygame.event.peek(QUIT) or exit:
                self.quit = True
                break

            # Update actors
            for actor in [score_text] + [player] + [health] + enemies + shots + enemy_shots + recover_health:
                render = actor.erase(self.screen, background)
                actors.append(render)
                actor.update()

            # Remove out-of-frame shots
            for shot in shots:
                if shot.rect.top <= 0:
                    shots.remove(shot)

            for shot in enemy_shots:
                if shot.rect.bottom >= const.SCREENRECT.height:
                    enemy_shots.remove(shot)

            # Move the player, x_dir initialization moved outside while loop with a starting value of the center.
            #Uses hit_right and hit_left to tell if the edges have been hit.
            if(player.rect.x < 50):
                hit_left = True
                hit_right = False
            if(player.rect.x > 500):
                hit_left = False
                hit_right = True

            if(hit_right):
                x_dir = - 1
                player.move(x_dir)
            elif(hit_left):
                x_dir = + 1
                player.move(x_dir)


            # Update text
            score_text.update_text("Score " + str(self.score))

            # Create new shots
            if not player.reloading and len(shots) < const.MAX_SHOTS:
                shots.append(Shot(shot_img, player))
                shot_audio.play()
            player.reloading = shoot

            # Create new alien
            if not int(random.random() * const.ENEMY_ODDS):
                #only appends until the number of max is reached
                ##CHECK
                ##make sure the enemy array is incrementing
                check = len(enemies)
                if(self.enemy_count < const.MAX_ENEMIES):
                    #counting the number of enemies that were spawned
                    #self.enemy_count += 1
                    enemies.append(Enemy(enemy_img))
                    self.enemy_count += 1
                    ##CHECK
                    if(len(enemies) == (check+1)):
                        checks.ENEMY_LIST_INCREMENTS = True
                    else :
                        checks.ENEMY_LIST_INCREMENTS = False
                        print("Enemy list increments when enemy spawned: FALSE")
                    #CHECK to make sure enemies not spawning when MAX_ENEMIES is reached
                    if(self.enemy_count > const.MAX_ENEMIES):
                        checks.LESS_MAX_ENEMIES = False
                        print("Enemies stop spawning when max count reached: FALSE")

            #spawning health recovery objects on screen
            if player.health < 3:
                if random.randint(1, 201) == 1:
                    recover_health.append(Recover_health(recover_health_img))

            #player collision with health recovery objects
            for z in recover_health:
                if player.health < 3:
                    if z.pickup(player):
                        recover_health.remove(z)
                        player.health += 1
                        power_up_audio.play()
                        if player.health == 3:
                            health.image = health_img_3
                        elif player.health == 2:
                            health.image = health_img_2

            #remove health recovery object as it moves off screen
            for z in recover_health:
                if z.rect.bottom >= const.SCREENRECT.height:
                    recover_health.remove(z)

            # Make enemies shoot
            if(len(enemies) > 0):
                ##CHECK
                ##make sure the enemy_shot array is incrementing
                check = len(enemy_shots)
                if not int(random.random() * const.ENEMY_SHOT_ODDS):
                    if (self.enemy_shot_count < const.MAX_ENEMY_SHOT):
                        self.enemy_shot_count += 1
                        #enemy_shots.append(Enemy_shot(enemy_shot_img, enemies[int(random.random() * (len(enemies)-1))]))
                        enemy_shots.append(Enemy_shot(enemy_shot_img, enemies[random.randint(0, len(enemies)-1)]))
                        ##CHECK
                        if(len(enemy_shots) == (check+1)):
                            checks.ENEMY_SHOT_LIST_INCREMENTS = True
                        else :
                            checks.ENEMY_SHOT_LIST_INCREMENTS = False
                            print("Enemy_shot list increments when enemy shoots: FALSE")
                        #CHECK to make sure enemies not spawning when MAX_ENEMIES is reached
                        if(self.enemy_shot_count > const.MAX_ENEMY_SHOT):
                            checks.LESS_MAX_ENEMY_SHOT = False
                            print("Enemies stop shooting when max count reached: FALSE")

            for y in enemy_shots:
                if y.collision_check(player):
                    enemy_shots.remove(y)
                    player.health -= 1
                    if player.health == 0:
                        health.image = health_img_0
                        player.alive = False
                        self.gameover = True
                    elif player.health == 1:
                        hit_audio.play()
                        health.image = health_img_1
                    elif player.health == 2:
                        hit_audio.play()
                        health.image = health_img_2

            # Check for collisions
            for enemy in enemies:
                if enemy.collision_check(player):
                    enemies.remove(enemy)
                    player.health -= 1
                    if player.health == 0:
                        health.image = health_img_0
                        player.alive = False
                        self.gameover = True
                    elif player.health == 1:
                        hit_audio.play()
                        health.image = health_img_1
                    elif player.health == 2:
                        hit_audio.play()
                        health.image = health_img_2

                #enemies go away once they hit the bottom
                if enemy.rect.y >= const.SCREENRECT.height - 30:
                    enemies.remove(enemy)


                for shot in shots:
                    if shot.collision_check(enemy):
                        enemy_audio.play()
                        shots.remove(shot)
                        enemies.remove(enemy)
                        self.score += 1

            # Draw actors
            for actor in [score_text] + [player] + [health] + enemies + shots + enemy_shots + recover_health:
                render = actor.draw(self.screen)
                actors.append(render)

            # Update actors
            pygame.display.update(actors)
            actors = []

        #CHECKS
        print("Does not go over max enemy: " + str(checks.LESS_MAX_ENEMIES))
        print("Does not go over max enemy shot: " + str(checks.LESS_MAX_ENEMY_SHOT))
        print("List increments when enemy added: " + str(checks.ENEMY_LIST_INCREMENTS))
        print("List increments when enemy shoots: " + str(checks.ENEMY_SHOT_LIST_INCREMENTS))
        # Exit game and system
        if self.gameover:
            gameover_audio.play()
        self.quit_game()

    ## Quits the game
    #  @pre A game session is running
    #  @post All components have been properly suspended
    def quit_game(self):
        pygame.time.delay(2000)
        pygame.display.quit()
        pygame.quit()
        sys.exit()