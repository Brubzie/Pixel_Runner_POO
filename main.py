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

# Inicialização do Pygame
pygame.init()

# Definindo altura e largura da tela
width, height = 800, 400
screen = pygame.display.set_mode((width, height)) # Inicializa o modo de vídeo

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

# Carrega recursos uma vez
def load_resources():
    resources = {
        'player_walk_1' : pygame.image.load(get_path('data/graphics/Player/player_walk_1.png')).convert_alpha(),
        'player_walk_2' : pygame.image.load(get_path('data/graphics/Player/player_walk_2.png')).convert_alpha(),
        'player_jump' : pygame.image.load(get_path('data/graphics/Player/jump.png')).convert_alpha(),
        'player_stand' : pygame.image.load(get_path('data/graphics/Player/player_stand.png')).convert_alpha(),
        'fly_1' : pygame.image.load(get_path('data/graphics/Fly/Fly1.png')).convert_alpha(),
        'fly_2' : pygame.image.load(get_path('data/graphics/Fly/Fly2.png')).convert_alpha(),
        'snail_1' : pygame.image.load(get_path('data/graphics/snail/snail1.png')).convert_alpha(),
        'snail_2' : pygame.image.load(get_path('data/graphics/snail/snail2.png')).convert_alpha(),
        'sky' : pygame.image.load(get_path('data/graphics/Sky.png')).convert_alpha(),
        'ground' : pygame.image.load(get_path('data/graphics/ground.png')).convert_alpha(),
        'font' : pygame.font.Font(get_path('data/font/Pixeltype.ttf'), 50),
        'jump_sound' : pygame.mixer.Sound(get_path('data/audio/jump.mp3')),
        'bg_music' : pygame.mixer.Sound(get_path('data/audio/music.wav')),
    }
    resources['jump_sound'].set_volume(0.5)
    resources['bg_music'].set_volume(0.5)
    return resources

RESOURCES = load_resources()

# Classe Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = [RESOURCES['player_walk_1'], RESOURCES['player_walk_2']]
        self.player_index = 0
        self.player_jump = RESOURCES['player_jump']
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.jump_sound = RESOURCES['jump_sound']
        
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

# Classe Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, player):
        super().__init__()
        
        if type == 'fly':
            self.frames = [RESOURCES['fly_1'], RESOURCES['fly_2']]
            y_pos = 210
        else:
            self.frames = [RESOURCES['snail_1'], RESOURCES['snail_2']]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.player = player # Referência ao jogador
        
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
            # Se o obstáculo saiu da tela sem colidir com o jogador, aumenta a pontuação
            if not pygame.sprite.collide_rect(self, self.player):
                self.player.game.score += 1
                
            self.kill()

# Classe Game (principal)
class Game:
    def __init__(self):
        """Inicializando a classe Game."""
        super().__init__()
        
        self.fps = 60 # Quadros por segundo
        self.clock = pygame.time.Clock()
        
        self.test_font = RESOURCES['font']

        # Definindo altura e largura da tela
        self.width = width
        self.height = height

        # Definindo argumentos da janela
        self.screen = screen

        # Título da janela do jogo
        pygame.display.set_caption('Pixel Runner')

        self.game_active = True
        self.start_time = 0
        self.score = 0
        self.bg_music = RESOURCES['bg_music']
        self.bg_music.play(loops = -1)
        
        # Groups | Grupos
        self.player = pygame.sprite.GroupSingle()
        player_instance = Player()
        player_instance.game = self # Adiciona referência ao jogo na instância do jogador
        self.player.add(player_instance)

        self.obstacle_group = pygame.sprite.Group()
        
        """ Carregando Sprites """
        # Background | Plano de Fundo
        self.sky_surface = RESOURCES['sky']
        self.ground_surface = RESOURCES['ground']

        # Player | Jogador
        self.player_stand = RESOURCES['player_stand']

        # Inicializa os índices de animação dos obstáculos
        self.snail_frame_index = 0
        self.fly_frame_index = 0

    def display_score(self):
        """Exibe a pontuação e a atualiza."""
        
        score_surf = self.test_font.render(f'Pontos: {self.score}', False, text_color)
        score_rect = score_surf.get_rect(center = (400, 50))
        self.screen.blit(score_surf, score_rect)
    
    def collision_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()  # Limpa os obstáculos após a colisão
            self.score = 0  # Reseta a pontuação ao colidir
            return False
        else:
            return True
    
    def start_game(self):
        """ Função onde o jogo será iniciado. """
        
        # Inicialização das variáveis
        sky_surface = self.sky_surface
        ground_surface = self.ground_surface
        player_stand = self.player_stand
        test_font = self.test_font
        screen = self.screen
        game_active = self.game_active
        fps = self.fps
        clock = self.clock
        
        # Obstáculos
        obstacle_rect_list = []
        
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
                        if event.key == pygame.K_SPACE and self.player.sprite.rect.bottom >= 300:
                            self.player.sprite.gravity = -20

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player.sprite.rect.collidepoint(event.pos) and self.player.sprite.rect.bottom >= 300:
                            self.player.sprite.gravity = -20
                
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                        self.start_time = int(pygame.time.get_ticks() / 1000)

                if game_active:
                    if event.type == obstacle_timer:
                        self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']), self.player.sprite))
                    
                    if event.type == snail_animation_timer:
                        if self.snail_frame_index == 0:
                            self.snail_frame_index = 1
                        else:
                            self.snail_frame_index = 0
                        
                        self.snail_surf = RESOURCES['snail_1'] if self.snail_frame_index == 0 else RESOURCES['snail_2']

                    if event.type == fly_animation_timer:
                        if self.fly_frame_index == 0:
                            self.fly_frame_index = 1
                        else:
                            self.fly_frame_index = 0
                        
                        self.fly_surf = RESOURCES['fly_1'] if self.fly_frame_index == 0 else RESOURCES['fly_2']
             
                
            if game_active:
                # Plano de fundo da tela | Background
                screen.blit(sky_surface, (0, 0))
                screen.blit(ground_surface, (0, 300))
                self.display_score()

                # Player | Jogador
                self.player.draw(screen)
                self.player.update()
                
                self.obstacle_group.draw(screen)
                self.obstacle_group.update()
                
                # Colisão
                game_active = self.collision_sprite()
                
            else:
                screen.fill(game_over_bg)
                screen.blit(player_stand, player_stand_rect)
                obstacle_rect_list.clear()
                self.player.sprite.rect.midbottom = (80, 300)
                self.player.sprite.gravity = 0
                
                score_message = test_font.render(f'Seus pontos: {self.score}', False, points_text_color)
                score_message_rect = score_message.get_rect(center = (400, 330))
                screen.blit(game_name, game_name_rect)
                
                if self.score == 0:
                    screen.blit(game_message, game_message_rect)
                else:
                    screen.blit(score_message, score_message_rect)
            
            pygame.display.flip()
            clock.tick(fps)

if __name__ == '__main__':
    try:
        game = Game()
        game.start_game()
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
