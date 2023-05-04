import pygame

pygame.init()

win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)
tema = "red"

class Login:
    BOTAO_WIDTH = 200
    BOTAO_HEIGHT =  300

    def tela_inicio():
        bem_vindo = FONT.render("Bem-vindo ao CodeQuiz!", True, "white")
        win.blit(bem_vindo, (200, 100))


        cadastrar = FONT.render("Cadastrar", True, "white")
        win.blit(cadastrar, (500, 300))
        login = FONT.render("Login", True, "white")
        win.blit(login, (200, 300))

class Jogador:
    tema = "red"

    def __init__(self, var):
        self.var = var

    def obter_tema():
        botao = FONT.render("Tema", True, "white")
        hitbox = botao.get_rect()
        hitbox.x = 450
        hitbox.y = 300
        win.blit(botao, hitbox)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            Jogador.tema = "green"  # Update class-level variable
        else:
            pass
        

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.fill(tema)
    instancia_jogador = Jogador(tema)
    Jogador.obter_tema()
    pygame.display.update()