# Importando bibliotecas/módulos
import pygame
import sys
import os
import tkinter as tk

from tkinter import messagebox
from random import randint, choice
from pygame.locals import VIDEORESIZE
from colors import *
from deep_translator import GoogleTranslator

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Função para criar o caminho do arquivo relativo ao diretório base
def get_path(relative_path):
    return os.path.join(BASE_DIR, relative_path)

# Adiciona o diretório atual ao path do sistema
dirpath = os.getcwd()
sys.path.append(dirpath)

# Ajuste do diretório para pacotes congelados
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
    
def show_error_message(error_message):
    """Exibe uma janela pop-up com a mensagem de erro."""
    root = tk.Tk()
    root.withdraw() # Oculta a janela principal do Tkinter
    messagebox.showerror('Erro', error_message)
    root.destroy()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(get_path('data/graphics/Player/player_walk_1.png')).convert_alpha()
        player_walk_2 = pygame.image.load(get_path('data/graphics/Player/player_walk_2.png')).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(get_path('data/graphics/Player/jump.png')).convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('data/audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            
            if self.player_index >= len(self.player_walk):
                self.player_index = 0

            self.image = self.player_walk[int(self.player_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load(get_path('data/graphics/Fly/Fly1.png')).convert_alpha()
            fly_2 = pygame.image.load(get_path('data/graphics/Fly/Fly2.png')).convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load(get_path('data/graphics/snail/snail1.png')).convert_alpha()
            snail_2 = pygame.image.load(get_path('data/graphics/snail/snail2.png')).convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        
    def animation_state(self):
        self.animation_index += 0.1
        
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
            
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Game:

    def __init__(self):
        """Inicializando a classe Game."""
        
        # Inicialização do Pygame
        pygame.init()
        
        self.fps = 60 # Quadros por segundo
        self.clock = pygame.time.Clock()
        
        self.test_font = pygame.font.Font(get_path('data/font/Pixeltype.ttf'), 50)

        # Definindo altura e largura da tela
        self.width = 800
        self.height = 400

        # Definindo argumentos da janela
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Título da janela do jogo
        pygame.display.set_caption('Pixel Runner')

        self.game_active = True
        self.start_time = 0
        self.score = 0
        self.bg_music = pygame.mixer.Sound('data/audio/music.wav')
        self.bg_music.set_volume(0.5)
        self.bg_music.play(loops = -1)
        
        # Groups | Grupos
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacle_group = pygame.sprite.Group()
        
        """ Carregando Sprites """
        # Background | Plano de Fundo
        self.sky_surface = pygame.image.load(get_path('data/graphics/Sky.png')).convert_alpha()
        self.ground_surface = pygame.image.load(get_path('data/graphics/ground.png')).convert_alpha()

        # Snail | Lesma
        self.snail_frame_1 = pygame.image.load(get_path('data/graphics/snail/snail1.png')).convert_alpha()
        self.snail_frame_2 = pygame.image.load(get_path('data/graphics/snail/snail2.png')).convert_alpha()
        self.snail_frames = [self.snail_frame_1, self.snail_frame_2]
        self.snail_frame_index = 0
        self.snail_surf = self.snail_frames[self.snail_frame_index]

        # Player | Jogador
        self.player_walk_1 = pygame.image.load(get_path('data/graphics/Player/player_walk_1.png')).convert_alpha()
        self.player_walk_2 = pygame.image.load(get_path('data/graphics/Player/player_walk_2.png')).convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(get_path('data/graphics/Player/jump.png')).convert_alpha()
        self.player_stand = pygame.image.load(get_path('data/graphics/Player/player_stand.png')).convert_alpha()
        self.player_surf = self.player_walk[self.player_index]

        # Mosca | Fly
        self.fly_frame_1 = pygame.image.load(get_path('data/graphics/Fly/Fly1.png')).convert_alpha()
        self.fly_frame_2 = pygame.image.load(get_path('data/graphics/Fly/Fly2.png')).convert_alpha()
        self.fly_frames = [self.fly_frame_1, self.fly_frame_2]
        self.fly_frame_index = 0
        self.fly_surf = self.fly_frames[self.fly_frame_index]
        
        # Gravity / Gravidade
        self.player_gravity = 0

    def display_score(self):
        """Exibe a pontuação e a atualiza."""
        
        # Inicialização das variáveis
        screen = self.screen
        start_time = self.start_time
        test_font = self.test_font
        
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = test_font.render(f'Pontos: {current_time}', False, text_color)
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)
        return current_time

    def obstacle_movement(self, obstacle_list):
        # Inicialização das variáveis
        screen = self.screen
        snail_surf = self.snail_surf
        fly_surf = self.fly_surf
        
        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= 5
                
                if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
                else: screen.blit(fly_surf, obstacle_rect)
                
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
                
            return obstacle_list
        
        else: return []
    
    def collisions(self, player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect): return False
        return True
    
    def collision_sprite(self):
        # Inicializando as variáveis
        player = self.player
        obstacle_group = self.obstacle_group
        
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            obstacle_group.empty()
            return False
        else:
            return True
    
    def player_animation(self):
        """
            Reproduz a animação de caminhada se o jogador estiver no chão.
            Exibe a superfície do salto quando o jogador não estiver no chão.
        """

        player_jump = self.player_jump
        player_walk = self.player_walk

        global player_surf, player_index
        
        if self.player_rect.bottom < 300:
            # Jump | Pulo
            self.player_surf = player_jump
        else:
            # Walk | Andar
            self.player_index += 0.1
            
            if self.player_index >= len(player_walk):
                self.player_index = 0
            
            self.player_surf = player_walk[int(self.player_index)]
    
    def startGame(self):
        """ Função onde o jogo será iniciado. """
        
        # Causa um erro proposital para teste
        # self.non_existent_variable # Isso causará um AttributeError
        
        # Inicialização das variáveis
        sky_surface = self.sky_surface
        ground_surface = self.ground_surface
        player_walk_1 = self.player_walk_1
        player_stand = self.player_stand
        test_font = self.test_font
        screen = self.screen
        game_active = self.game_active
        fps = self.fps
        clock = self.clock
        snail_frames = self.snail_frames
        fly_frames = self.fly_frames
        player = self.player
        self.player_rect = self.player_walk_1.get_rect(midbottom=(80, 300))
        
        # Obstáculos
        obstacle_rect_list = []
        
        player_rect = player_walk_1.get_rect(midbottom = (80, 300))
        
        # Intro screen | Tela de introdução
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rect = player_stand.get_rect(center = (400, 200))
        
        game_name = test_font.render('Pixel Runner', False, title_color)
        game_name_rect = game_name.get_rect(center = (400, 80))
        
        game_message = test_font.render('Pressione "espaco" para correr', False, title_color)
        game_message_rect = game_message.get_rect(center = (400, 330))

        # Timer | Cronômetro
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer, 1500)
        
        snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(snail_animation_timer, 500)
        
        fly_animation_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(fly_animation_timer, 200)
        
        while True:
            pygame.display.update()
            for event in pygame.event.get(): # Usuário realiza uma ação
                if event.type == pygame.QUIT: # Se o usuário clica para fechar a janela
                    pygame.quit()
                    sys.exit()

                if event.type == VIDEORESIZE:
                    old_screen_saved = screen
                    screen = pygame.display.set_mode((event.w, event.h))
                    screen.blit(old_screen_saved, (0,0))
                    del old_screen_saved

                if game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                            player_gravity = -20

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                            player_gravity = -20
                
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                        self.start_time = int(pygame.time.get_ticks() / 1000)

                if game_active:
                    if event.type == obstacle_timer:
                        self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                        
                        # if randint(0, 2):
                        #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
                        # else:
                        #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))
                    
                    if event.type == snail_animation_timer:
                        if self.snail_frame_index == 0:
                            self.snail_frame_index = 1
                        else:
                            self.snail_frame_index = 0
                        
                        self.snail_surf = snail_frames[self.snail_frame_index]

                    if event.type == fly_animation_timer:
                        if self.fly_frame_index == 0:
                            self.fly_frame_index = 1
                        else:
                            self.fly_frame_index = 0
                        
                        self.fly_surf = fly_frames[self.fly_frame_index]
             
                
            if game_active:
                # Plano de fundo da tela | Background
                screen.blit(sky_surface, (0, 0))
                screen.blit(ground_surface, (0, 300))
                score = self.display_score()

                # Player | Jogador
                # player_gravity += 1
                # player_rect.y += player_gravity
                
                # if player_rect.bottom >= 300:
                #     player_rect.bottom = 300

                # self.player_animation()
                # screen.blit(self.player_surf, player_rect)
                player.draw(screen)
                player.update()
                
                self.obstacle_group.draw(screen)
                self.obstacle_group.update()
                
                # Movimentação dos obstáculos/inimigos | Obstacle movement
                # obstacle_rect_list = self.obstacle_movement(obstacle_rect_list)
                
                # Colisão
                game_active = self.collision_sprite()
                # game_active = self.collisions(player_rect, obstacle_rect_list)
                
            else:
                screen.fill(game_over_bg)
                screen.blit(player_stand, player_stand_rect)
                obstacle_rect_list.clear()
                player_rect.midbottom = (80, 300)
                player_gravity = 0
                
                score_message = test_font.render(f'Seus pontos: {score}', False, points_text_color)
                score_message_rect = score_message.get_rect(center = (400, 330))
                screen.blit(game_name, game_name_rect)
                
                if score == 0:
                    screen.blit(game_message, game_message_rect)
                else:
                    screen.blit(score_message, score_message_rect)
            
            pygame.display.flip()
            game_fps = clock.tick(fps)
            game_fps

if __name__ == '__main__':
    try:
        game = Game()
        game.startGame()
    except Exception as error:
        tradutor = GoogleTranslator(source = 'en', target = 'pt')
        traducao = tradutor.translate(str(error))
        error_message = f'Ocorreu um erro: {traducao}.'
        print('=' * 100)
        print('========== Erros / Errors =========='.center(100))
        print('-' * 100)
        print('========== Pt-Br =========='.center(100))
        print(error_message)
        print('========== En-Us =========='.center(100))
        print(f'An error has occurred: {error}.')
        print('=' * 100)
        show_error_message(error_message)
    finally:
        pygame.quit()
        sys.exit()
