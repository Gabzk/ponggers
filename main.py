import pygame

pygame.init()

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Dimensões de tela
screen_width = 800  # Define altura desejada para tela
screen_height = 400  # Define a largura desejada para tela

# Velocidade dos jogadores
player_speed = 300

# Inicializa o subsistema de vídeo
pygame.display.init()

# Cria a janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Define a fonte para o placar


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed_x = 150
        self.speed_y = 150

    def update(self, dt):
        self.rect.x += self.speed_x * dt
        self.rect.y += self.speed_y * dt

        # Verifica colisão com as bordas da tela
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

    def reset_position(self):
        self.rect.center = (screen_width // 2, screen_height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 60))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0

    def update(self, dt):
        self.rect.y += self.speed * dt

        # Verifica a colisão com as bordas da tela
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def reset_position(self):
        self.rect.center = (self.rect.centerx, screen_height // 2)

    score = 0


ball = Ball()
player_1 = Player(20, screen_height // 2)
player_2 = Player(screen_width - 20, screen_height // 2)

all_sprites = pygame.sprite.Group()
all_sprites.add(ball, player_1, player_2)


def update_score():
    # Renderiza o texto do placar
    score_text = f"{player_1.score}     {player_2.score}"
    text_surface = font.render(score_text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width // 2, 20)

    # Desenha o texto na tela
    screen.blit(text_surface, text_rect)


def reset_position():
    ball.reset_position()
    player_1.reset_position()
    player_2.reset_position()


def main():
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Tempo decorrido desde o último frame em segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_2.speed = -player_speed
                elif event.key == pygame.K_DOWN:
                    player_2.speed = player_speed
                elif event.key == pygame.K_w:
                    player_1.speed = -player_speed
                elif event.key == pygame.K_s:
                    player_1.speed = player_speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_2.speed = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player_1.speed = 0

        all_sprites.update(dt)

        # Verifica a colisão da bola com os jogadores
        if pygame.sprite.collide_rect(ball, player_1) or pygame.sprite.collide_rect(ball, player_2):
            ball.speed_x *= -1

        # Verifica a colisão da bola com as bordas
        if ball.rect.left <= 0:
            player_2.score += 1
            reset_position()

        if ball.rect.right >= screen_width:
            player_1.score += 1
            reset_position()

        # Limpa a tela
        screen.fill(black)
        pygame.draw.line(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

        # Desenha os sprites na tela
        all_sprites.draw(screen)

        # Atualiza o placar
        update_score()

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
