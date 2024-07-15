# Importando bibliotecas/módulos
import pygame
import sys
import os

from random import randint
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

class Game:

    def __init__(self):
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
        
        self.fullscreen = False
        
        """ Carregando Sprites """
        # Background / Fundo
        self.sky_surface = pygame.image.load(get_path('data/graphics/Sky.png')).convert_alpha()
        self.ground_surface = pygame.image.load(get_path('data/graphics/ground.png')).convert_alpha()

        # Snail / Lesma
        self.snail_surf = pygame.image.load(get_path('data/graphics/snail/snail1.png')).convert_alpha()

        # Player / Jogador
        self.player_walk_1 = pygame.image.load(get_path('data/graphics/Player/player_walk_1.png')).convert_alpha()
        self.player_walk_2 = pygame.image.load(get_path('data/graphics/Player/player_walk_2.png')).convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(get_path('data/graphics/Player/jump.png')).convert_alpha()
        self.player_stand = pygame.image.load(get_path('data/graphics/Player/player_stand.png')).convert_alpha()
        self.player_surf = self.player_walk[self.player_index]

        self.fly_surf = pygame.image.load(get_path('data/graphics/Fly/Fly1.png')).convert_alpha()
        
        # Gravidade
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
    
    def player_animation(self):
        """ 
            Reproduz a animação de caminhada se o jogador estiver no chão.
            Exibe a superfície do salto quando o jogador não estiver no chão. 
        """
    
    def startGame(self):
        """ Função onde o jogo será iniciado. """
        
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
        
        # Obstáculos
        snail_surf = self.snail_surf
        fly_surf = self.fly_surf

        obstacle_rect_list = []
        
        player_rect = player_walk_1.get_rect(midbottom = (80, 300))
        player_gravity = 0
        
        # Tela de introdução
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rect = player_stand.get_rect(center = (400, 200))
        
        game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
        game_name_rect = game_name.get_rect(center = (400, 80))
        
        game_message = test_font.render('Pressione "espaco" para correr', False, (111, 196, 169))
        game_message_rect = game_message.get_rect(center = (400, 330))

        # Timer
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer, 1500)
        
        pygame.display.flip()
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
                        start_time = int(pygame.time.get_ticks() / 1000)

                if event.type == obstacle_timer:
                    if randint(0, 2):
                        obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
                    else:
                        obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))
             
                
            if game_active:
                # Plano de fundo da tela
                screen.blit(sky_surface, (0, 0))
                screen.blit(ground_surface, (0, 300))
                score = self.display_score()

                # snail_rect.x -= 4
                # if snail_rect.right <= 0: snail_rect.left = 800
                # screen.blit(snail_surf, snail_rect)

                # Player / Jogador
                player_gravity += 1
                player_rect.y += player_gravity
                
                if player_rect.bottom >= 300:
                    player_rect.bottom = 300

                screen.blit(player_walk_1, player_rect)
                
                # Movimentação dos obstáculos/inimigos
                obstacle_rect_list = self.obstacle_movement(obstacle_rect_list)
                
                # Colisão
                game_active = self.collisions(player_rect, obstacle_rect_list)
                
            else:
                screen.fill((game_over_bg))
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
        traducao = tradutor.translate(error)
        print('=' * 50)
        print('=== Erros / Errors ==='.center(50))
        print('-' * 50)
        print('=== Pt-Br ==='.center(50))
        print(f'Ocorreu um erro: {traducao}.')
        print('=== En-Us ==='.center(50))
        print(f'An error has occurred: {error}.')
        print('=' * 50)
    finally:
        pygame.quit()
        sys.exit()
