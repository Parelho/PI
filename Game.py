import pygame

pygame.init()

win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)

class Login:
    BOTAO_WIDTH = 200
    BOTAO_HEIGHT =  300

    def __init__(self):
        self.inicio = True
        self.cadastrar_rect = pygame.Rect(500, 300, 200, 50)
        self.login_rect = pygame.Rect(200, 300, 125, 50)

    def fazer_login(self):
        win.fill(jogador.tema)
        self.inicio = False

    def fazer_cadastro(self):
        win.fill(jogador.tema)
        self.inicio = False
        

    def tela_inicio(self):
        bem_vindo = FONT.render("Bem-vindo ao CodeQuiz!", True, "white")
        win.blit(bem_vindo, (200, 100))

        cadastrar = FONT.render("Cadastrar", True, "white")
        win.blit(cadastrar, (500, 300))
        login = FONT.render("Login", True, "white")
        win.blit(login, (200, 300))

        mpos = pygame.mouse.get_pos()
        if self.cadastrar_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.fazer_cadastro()
        elif self.login_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.fazer_login()

class Jogador:
    def __init__(self):
        self.tema = "black"
        self.tema_rect = pygame.Rect(450, 300, 100, 50)

    def obter_tema(self):
        mpos = pygame.mouse.get_pos()
        if self.tema_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.tema = "green"

        pygame.draw.rect(win, self.tema, self.tema_rect)
        win.fill(self.tema, self.tema_rect)

        botao = FONT.render("Tema", True, "white")
        win.blit(botao, (self.tema_rect.x, self.tema_rect.y))


running = True
jogador = Jogador()
login = Login()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.fill(jogador.tema)

    if login.inicio:
        login.tela_inicio()


    pygame.display.update()

pygame.quit()