import pygame
import pygame_textinput

# Inicializa o pygame
pygame.init()

# Constantes
win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)
FONT_LOGIN = pygame.font.SysFont("timesnewroman", 30)

# Classes
class Login:
    # Método utilizado para permitir a sobrecarga de métodos no Python
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
        # Mostrando os campos de usuário e senha para o jogador
        usuario = FONT_LOGIN.render("Usuario: ", True, "white")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "white")
        win.blit(senha, (100, 192))
        mpos = pygame.mouse.get_pos()

        # Checa se o mouse está em cima do texto de usuário e se o jogador clicou com o botão esquerdo do mouse
        if self.usuario_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            # usuario_click utilizado para o jogador não ter que ficar segurando o botão esquerdo do mouse para poder digitar, provavelmente existe uma solução melhor
            self.usuario_click = True
        # Caso o jogador clique fora da caixa, ela deixa de aceitar input
        elif not self.usuario_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.usuario_click = False
            textinput_usuario.cursor_visible = False
        if self.usuario_click:
            # Checa todas as frames se ouve alguma mudança na string
            textinput_usuario.update(events)
        # Coloca a string na tela
        win.blit(textinput_usuario.surface, (200, 100))

        # Checa se o mouse está em cima do texto de senha e se o jogador clicou com o botão esquerdo do mouse
        if self.senha_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            # senha_click utilizado para o jogador não ter que ficar segurando o botão esquerdo do mouse para poder digitar, provavelmente existe uma solução melhor
            self.senha_click = True
        # Caso o jogador clique fora da caixa, ela deixa de aceitar input
        elif not self.senha_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.senha_click = False
            textinput_senha.cursor_visible = False
        
        if self.senha_click:
            # Checa todas as frames se ouve alguma mudança na string
            textinput_senha.update(events)
        # Coloca a string na tela
        win.blit(textinput_senha.surface, (200, 200))

       # Similar ao método de login, fora a parte que está comentada
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

        # Checa se o mouse está em cima do botão de cadastro
        mpos = pygame.mouse.get_pos()
        if self.cadastrar_rect.collidepoint(mpos):
            # Checa se o jogador clicou com o botão esquerdo do mouse
            if pygame.mouse.get_pressed()[0]:
                self.login = False
                self.inicio = False
        # Checa se o mouse está em cima do botão de login     
        elif self.login_rect.collidepoint(mpos):
            # Checa se o jogador clicou com o botão esquerdo do mouse
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

# Utilizado para criar a string que será utilizada pelo pygame_textinput
textinput_usuario = pygame_textinput.TextInputVisualizer()
textinput_senha = pygame_textinput.TextInputVisualizer()

running = True
jogador = Jogador()
login = Login()

while running:
    # Utilizado para ver os inputs do jogador
    events = pygame.event.get()
    # Fecha o loop caso a aba do pygame seja fechada
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    # Coloca o tema do fundo na tela atrás de todo o resto que for desenhado
    win.fill(jogador.tema)

    # Login().inicio é utilizado para ver se o a tela de boas vindas deve ser mostrada ou não
    if login.inicio:
        login.tela_inicio()
    # Se login for True, será aberta a tela de login
    elif login.login:
        login.fazer_login()
    # Se login for False, será aberta a tela de cadastro
    elif login.login == False:
        login.fazer_cadastro()

    # Da update nos métodos do pygame
    pygame.display.update()
    # Taxa de FPS, atualmente está 60 FPS
    clock.tick(60)
# Para as operações do pygame para garantir que o código vai terminar de ser executado
pygame.quit()