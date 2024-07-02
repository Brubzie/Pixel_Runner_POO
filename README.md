# Pixel Runner

Pixel Runner é um jogo simples de corrida desenvolvido em Python usando a biblioteca Pygame. Este projeto é baseado em um vídeo de introdução ao Pygame criado pelo canal do YouTube [Clear Code](https://www.youtube.com/c/ClearCode).

## Sobre o Projeto

Este projeto serve como uma introdução ao desenvolvimento de jogos com Pygame. O jogo apresenta um personagem que corre e pula sobre obstáculos, acumulando pontos conforme o tempo passa.

## Instalação

### Requisitos

- Python 3.x
- Pygame

### Passos para Instalação

1. Clone este repositório:
    ```sh
    git clone https://github.com/seu-usuario/pixel-runner.git
    ```

2. Navegue até o diretório do projeto:
    ```sh
    cd pixel-runner
    ```

3. Instale as dependências:
    ```sh
    pip install pygame
    ```

## Como Jogar

1. Execute o jogo:
    ```sh
    python main.py
    ```

2. Use a tecla `space` para fazer o personagem pular e evitar os obstáculos.

## Compilando para um Executável

Se você quiser compilar o jogo em um executável, pode usar o PyInstaller. Aqui estão os passos:

1. Instale o PyInstaller:
    ```sh
    pip install pyinstaller
    ```

2. Execute o comando para criar o executável:
    ```sh
    pyinstaller main.spec
    ```
