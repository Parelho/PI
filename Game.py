import pygame
import pygame_textinput
import time
import mysql.connector
from mysql.connector import errorcode
import os

# Inicializa o pygame
pygame.init()

# Constantes
win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)
FONT_LOGIN = pygame.font.SysFont("timesnewroman", 30)
FONT_MOEDAS = pygame.font.SysFont("comicsans", 35)
FONT_MASCOTE = pygame.font.SysFont("comicsans", 20)
FONT_NIVEL = pygame.font.SysFont("arial", 100)

# Classes
class Jogador:
    def __init__(self):
        self.tema = "darkgreen"
        self.tema_rect = pygame.Rect(450, 300, 100, 50)
        self.engrenagem_rect = pygame.Rect(20, 500, 100, 100)
        self.loja_rect = pygame.Rect(120, 500, 100, 100)
        self.voltar_rect = pygame.Rect(400, 500, 100, 30)
        self.moedas = 10
        self.xp = 0
        self.opcoes_aberto = False
        self.loja_aberta = False

    def menu_principal(self):
        #Loja
        loja = pygame.image.load(os.path.join("imgs", "Loja.png"))
        win.blit(loja, (120, 500))
        mpos = pygame.mouse.get_pos()

        if self.loja_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.loja_aberta = True
    
        #Mostar xp e moedas
        xp = FONT_MOEDAS.render("XP:" + str(self.xp), True, "white")
        win.blit(xp, (750, 100))
        moedas = FONT_MOEDAS.render("Moedas:" + str(self.moedas), True, "white")
        win.blit(moedas, (700, 200))
    
        #Mascote
        mascote = pygame.image.load(os.path.join("imgs", "Mascote.png"))
        win.blit(mascote, (0, 50))

        mensagem = FONT_MASCOTE.render("Bem-Vindo ao CodeQuiz!", True, "white")
        win.blit(mensagem, (0, 0))

        #Opcoes
        engrenagem = pygame.image.load(os.path.join("imgs", "engrenagem.png"))
        win.blit(engrenagem, (20, 500))

        if self.engrenagem_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.opcoes_aberto = True

    def opcoes(self):
        mpos = pygame.mouse.get_pos()
        if self.tema_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.tema = "purple"

        pygame.draw.rect(win, self.tema, self.tema_rect)
        win.fill(self.tema, self.tema_rect)

        botao = FONT.render("Tema", True, "white")
        win.blit(botao, (self.tema_rect.x, self.tema_rect.y))

        voltar = FONT_LOGIN.render("Voltar", True, "white")
        win.blit(voltar,(400, 500))
        if self.voltar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.opcoes_aberto = False
    
    def loja(self):
        mpos = pygame.mouse.get_pos()

        voltar = FONT_LOGIN.render("Voltar", True, "white")
        win.blit(voltar,(400, 500))
        if self.voltar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.loja_aberta = False

class SeletorDeNivel:
    def __init__(self):
        self.lv1 = pygame.Rect(270, 70, 160, 160)
        self.lv1_aberto = False
        self.lv_aberto = False
    
    def selecionar_nivel(self):
        pygame.draw.rect(win, "grey",[250, 0, 10 ,600])
        pygame.draw.rect(win, "grey",[650, 0, 10 ,600])
        win.blit(FONT_LOGIN.render("Selecionar nivel", True, "white"), (350, 0))
        pygame.draw.circle(win, "black",[350, 150], 80)
        pygame.draw.circle(win, "black",[550, 150], 80)
        win.blit(FONT_NIVEL.render("1", True, "white"), (325, 90))
        win.blit(FONT_NIVEL.render("2", True, "white"), (525, 90))
        mpos = pygame.mouse.get_pos()

        if self.lv1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.lv_aberto = True
            self.lv1_aberto = True

class Pergunta():
    def __init__(self):
        pass
    
    def nivel1(self):
        win.blit(FONT_LOGIN.render("Nivel 1", True, "white"), (400, 0))
class Login(Jogador):
    # Método utilizado para permitir a sobrecarga de métodos no Python
    def __init__(self):
        self.inicio = True
        self.login = False
        self.cadastro = False
        self.cadastrar_rect = pygame.Rect(500, 300, 200, 50)
        self.login_rect = pygame.Rect(200, 300, 125, 50)
        self.usuario_rect = pygame.Rect(100, 100, 100, 30)
        self.senha_rect = pygame.Rect(100, 192, 100, 30)
        self.voltar_rect = pygame.Rect(400, 500, 100, 30)
        self.enviar_rect = pygame.Rect(400, 400, 100 , 30)
        self.usuario_click = False
        self.senha_click = False
        self.login_pronto = False
        self.cadastro_pronto = False
        self.senha = ""
        self.usuario = ""
    
    def mysql(self, moedas, xp):
        db = mysql.connector.connect(
            host = "localhost",
            user="root",
            passwd="senha mysql",
        )

        db_name = "CodeQuiz"
        cursor = db.cursor()

        def create_database(cursor):
            try:
                cursor.execute("CREATE DATABASE {};".format(db_name))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)

        try:
            cursor.execute("USE {}".format(db_name))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully.".format(db_name))
                db.database = db_name

        TABLES = {}

        TABLES['Usuario'] = ("CREATE TABLE Usuario(username varchar(50) primary key, senha varchar(50), xp int, moedas int);")
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
        if self.cadastro_pronto == True:
            add_usuario = "INSERT INTO Usuario VALUES(%s, %s, %s, %s);"
            data_usuario = (self.usuario, self.senha, xp, moedas)
            cursor.execute(add_usuario, data_usuario)
            db.commit()
            self.usuario = ""
            self.senha = ""
            self.cadastro_pronto = False
        
        if self.login_pronto:
            query = "SELECT * FROM Usuario"
            cursor.execute(query)

            for row in cursor:
                if self.usuario and self.senha in row:
                    print("Usuario encontrado")
                    break
                else:
                    print("Usuario nao encontrado")
                    break
            
            self.login_pronto = False
            self.inicio = False
            self.login = False

    def fazer_login(self):
        # Mostrando os campos de usuário e senha para o jogador
        usuario = FONT_LOGIN.render("Usuario: ", True, "white")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "white")
        win.blit(senha, (100, 192))
        voltar = FONT_LOGIN.render("Voltar", True, "white")
        win.blit(voltar,(400, 500))
        enviar = FONT_LOGIN.render("Enviar", True, "white")
        win.blit(enviar, (400, 400))
        mpos = pygame.mouse.get_pos()

        # Checa se o mouse está em cima do texto de voltar e se o jogador clicou com o botão esquerdo do mouse
        if self.voltar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.inicio = True

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
        
        if self.enviar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            time.sleep(1)
            self.login_pronto = True
            self.usuario = textinput_usuario.value
            self.senha = textinput_senha.value

       # Similar ao método de login, fora a parte que está comentada
    def fazer_cadastro(self):
        usuario = FONT_LOGIN.render("Usuario: ", True, "white")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "white")
        win.blit(senha, (100, 192))
        voltar = FONT_LOGIN.render("Voltar", True, "white")
        win.blit(voltar,(400, 500))
        enviar = FONT_LOGIN.render("Enviar", True, "white")
        win.blit(enviar, (400, 400))
        mpos = pygame.mouse.get_pos()

        if self.voltar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.inicio = True
    
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

        if self.enviar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            time.sleep(1)
            self.cadastro_pronto = True
            self.usuario = textinput_usuario.value
            self.senha = textinput_senha.value

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
                self.cadastro = True
                self.inicio = False
        # Checa se o mouse está em cima do botão de login     
        elif self.login_rect.collidepoint(mpos):
            # Checa se o jogador clicou com o botão esquerdo do mouse
            if pygame.mouse.get_pressed()[0]:
                self.login = True
                self.inicio = False

# Utilizado para criar a string que será utilizada pelo pygame_textinput
textinput_usuario = pygame_textinput.TextInputVisualizer()
textinput_senha = pygame_textinput.TextInputVisualizer()

running = True
jogador = Jogador()
login = Login()
nivel = SeletorDeNivel()
pergunta = Pergunta()

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
        if login.login_pronto:
            login.mysql(jogador.moedas, jogador.xp)
    # Se login for False, será aberta a tela de cadastro
    elif login.cadastro:
        login.fazer_cadastro()
        if login.cadastro_pronto:
            login.mysql(jogador.moedas, jogador.xp)
    
    if login.inicio == False and login.login == False and login.cadastro == False:
        if jogador.opcoes_aberto == False and jogador.loja_aberta == False and nivel.lv_aberto == False:
            jogador.menu_principal()
            nivel.selecionar_nivel()
        elif jogador.opcoes_aberto:
            jogador.opcoes()
        elif jogador.loja_aberta:
            jogador.loja()
        elif nivel.lv_aberto:
            pergunta.nivel1()


    # Da update nos métodos do pygame
    pygame.display.update()
    # Taxa de FPS, atualmente está 60 FPS
    clock.tick(60)
# Para as operações do pygame para garantir que o código vai terminar de ser executado
pygame.quit()