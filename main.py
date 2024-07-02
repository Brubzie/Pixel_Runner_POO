import pygame
import sys
import os
from pygame.locals import VIDEORESIZE
from colors import *

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
        
        # Sprites
        self.sky_surface = pygame.image.load(get_path('data/graphics/Sky.png')).convert_alpha()
        self.ground_surface = pygame.image.load(get_path('data/graphics/ground.png')).convert_alpha()
        self.snail_surf = pygame.image.load(get_path('data/graphics/snail/snail1.png')).convert_alpha()
        self.player_surf = pygame.image.load(get_path('data/graphics/Player/player_walk_1.png')).convert_alpha()
        self.player_stand = pygame.image.load(get_path('data/graphics/Player/player_stand.png')).convert_alpha()
        
        # Gravidade
        self.player_gravity = 0
        
    def display_score(self):
        """Exibe a pontuação e a atualiza."""
        self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        self.score_surf = self.test_font.render(f'Pontos: {self.current_time}', False, text_color)
        self.score_rect = self.score_surf.get_rect(center=(400, 50))
        self.screen.blit(self.score_surf, self.score_rect)
        return self.current_time
    
    def startGame(self):
        """Função onde o jogo será iniciado."""
        
        sky_surface = self.sky_surface
        ground_surface = self.ground_surface
        
        snail_surf = self.snail_surf
        snail_rect = snail_surf.get_rect(bottomright=(600, 300))
        
        player_surf = self.player_surf
        player_rect = player_surf.get_rect(midbottom=(80, 300))
        player_gravity = 0
        
        # Intro screen
        player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)
        player_stand_rect = self.player_stand.get_rect(center=(400, 200))
        
        game_name = self.test_font.render('Pixel Runner', False, (111, 196, 169))
        game_name_rect = game_name.get_rect(center=(400, 80))
        
        game_message = self.test_font.render('Pressione "space" para correr', False, (111, 196, 169))
        game_message_rect = game_message.get_rect(center=(400, 340))
        
        pygame.display.flip()
        while True:
            pygame.display.update()
            for event in pygame.event.get(): # Usuário realiza uma ação
                if event.type == pygame.QUIT: # Se o usuário clica para fechar a janela
                    pygame.quit()
                    sys.exit()

                if event.type == VIDEORESIZE:
                    old_screen_saved = self.screen
                    self.screen = pygame.display.set_mode((event.w, event.h))
                    self.screen.blit(old_screen_saved, (0,0))
                    del old_screen_saved

                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                            player_gravity = -20

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                            player_gravity = -20
                
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_active = True
                        snail_rect.left = 800
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                
            if self.game_active:
                # Plano de fundo da tela
                self.screen.fill(BLACK)

                # Desenha os sprites na tela
                self.screen.blit(sky_surface, (0, 0))
                self.screen.blit(ground_surface, (0, 300))
                score = self.display_score()

                snail_rect.x -= 4
                if snail_rect.right <= 0: snail_rect.left = 800
                self.screen.blit(snail_surf, snail_rect)

                # Player
                player_gravity += 1
                player_rect.y += player_gravity
                if player_rect.bottom >= 300: player_rect.bottom = 300
                self.screen.blit(player_surf, player_rect)
                
                # Colisão
                if snail_rect.colliderect(player_rect):
                    self.game_active = False
            else:
                self.screen.fill(game_over_bg)
                self.screen.blit(player_stand, player_stand_rect)
                
                score_message = self.test_font.render(f'Seus pontos: {score}', False, (111, 196, 169))
                score_message_rect = score_message.get_rect(center=(400, 330))
                self.screen.blit(game_name, game_name_rect)
                
                if score == 0:
                    self.screen.blit(game_message, game_message_rect)
                else:
                    self.screen.blit(score_message, score_message_rect)
            
            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    try:
        game = Game()
        game.startGame()
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
    finally:
        pygame.quit()
        sys.exit()
