import pygame
import pygame_textinput

pygame.init()

win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)
FONT_LOGIN = pygame.font.SysFont("timesnewroman", 30)

class Login:
    BOTAO_WIDTH = 200
    BOTAO_HEIGHT =  300

    def __init__(self):
        self.inicio = True
        self.login = True
        self.cadastrar_rect = pygame.Rect(500, 300, 200, 50)
        self.login_rect = pygame.Rect(200, 300, 125, 50)
        self.usuario_rect = pygame.Rect(100, 100, 100, 20)
        self.senha_rect = pygame.Rect(100, 192, 100, 20)
        self.usuario_click = False
        self.senha_click = False

    def fazer_login(self):
        usuario = FONT_LOGIN.render("Usuario: ", True, "white")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "white")
        win.blit(senha, (100, 192))
        mpos = pygame.mouse.get_pos()
    
        if self.usuario_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.usuario_click = True
        elif not self.usuario_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.usuario_click = False
            textinput_usuario.cursor_visible = False
        
        if self.usuario_click:
            textinput_usuario.update(events)
        win.blit(textinput_usuario.surface, (200, 100))

        if self.senha_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.senha_click = True
        elif not self.senha_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.senha_click = False
            textinput_senha.cursor_visible = False
        
        if self.senha_click:
            textinput_senha.update(events)
        win.blit(textinput_senha.surface, (200, 200))
    
    def fazer_cadastro(self):
        usuario = FONT_LOGIN.render("Usuario: ", True, "white")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "white")
        win.blit(senha, (100, 192))
        mpos = pygame.mouse.get_pos()
    
        if self.usuario_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.usuario_click = True
        elif not self.usuario_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.usuario_click = False
            textinput_usuario.cursor_visible = False
        
        if self.usuario_click:
            textinput_usuario.update(events)
        win.blit(textinput_usuario.surface, (200, 100))

        if self.senha_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.senha_click = True
        elif not self.senha_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.senha_click = False
            textinput_senha.cursor_visible = False
        
        if self.senha_click:
            textinput_senha.update(events)
        win.blit(textinput_senha.surface, (200, 200))

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
                self.login = False
                self.inicio = False
                
        elif self.login_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.login = True
                self.inicio = False

class Jogador:
    def __init__(self):
        self.tema = "purple"
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

textinput_usuario = pygame_textinput.TextInputVisualizer()
textinput_senha = pygame_textinput.TextInputVisualizer()
running = True
jogador = Jogador()
login = Login()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    win.fill(jogador.tema)

    if login.inicio:
        login.tela_inicio()
    elif login.login:
        login.fazer_login()
    elif login.login == False:
        login.fazer_cadastro()


    pygame.display.update()
    clock.tick(60)
pygame.quit()