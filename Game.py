import pygame
import pygame_textinput
import time
import psycopg
import os
import random

# Inicializa o pygame
pygame.init()

# Utilizados como workaround de um bug que estava impedindo a classe Login de pegar os valores atualizados de acertos, level e streak, se conseguir resolver o bug irei remover essa mostruosidade
acertos = 0
level = 0
streak = 0

# Constantes
win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)
FONT_LOGIN = pygame.font.SysFont("timesnewroman", 30)
FONT_MOEDAS = pygame.font.SysFont("comicsans", 35)
FONT_MASCOTE = pygame.font.SysFont("comicsans", 20)
FONT_PERGUNTA = pygame.font.SysFont("arial", 20)
FONT_NIVEL = pygame.font.SysFont("arial", 100)

# Classes
class Jogador:
    def __init__(self):
        self.tema = "darkgreen"
        self.tema_rect = pygame.Rect(450, 300, 100, 50)
        self.engrenagem_rect = pygame.Rect(20, 500, 100, 100)
        self.loja_rect = pygame.Rect(120, 500, 100, 100)
        self.voltar_rect = pygame.Rect(400, 500, 100, 30)
        self.opcoes_aberto = False
        self.loja_aberta = False

    def menu_principal(self):
        #Loja
        loja = pygame.image.load(os.path.join("imgs", "Loja.png"))
        win.blit(loja, (120, 500))
        mpos = pygame.mouse.get_pos()

        if self.loja_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.loja_aberta = True
    
        #Mascote
        mascote = pygame.image.load(os.path.join("imgs", "Mascote.png"))
        win.blit(mascote, (0, 50))

        mensagem = FONT_MASCOTE.render("Bem Vindo ao CodeQuiz!", True, "white")
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

class SeletorDeNivel():
    def __init__(self):
        self.voltar_rect_pergunta = pygame.Rect(400, 500, 100, 30)
        self.lv1 = pygame.Rect(270, 70, 160, 160)
        self.lv2 = pygame.Rect(470, 70, 160, 160)
        self.lv3 = pygame.Rect(270, 245, 160, 160)
        self.lv4 = pygame.Rect(470, 245, 160, 160)
        self.lv5 = pygame.Rect(270, 420, 160, 160)
        self.lv_endless = pygame.Rect(470, 420, 160, 160)
        self.lv1_aberto = False
        self.lv2_aberto = False
        self.lv3_aberto = False
        self.lv4_aberto = False
        self.lv5_aberto = False
        self.lv_endless_aberto = False
        self.lv_aberto = False
        self.lv2_desbloqueado = False
        self.lv3_desbloqueado = False
        self.lv4_desbloqueado = False
        self.lv5_desbloqueado = False
        self.login = Login()
    
    def selecionar_nivel(self, xp):
        if xp >= 4000:
            self.lv5_desbloqueado = True
        elif xp >= 3000:
            self.lv4_desbloqueado = True
        elif xp >= 2000:
            self.lv3_desbloqueado = True
        elif xp >= 1000:
            self.lv2_desbloqueado = True
    
        cadeado = pygame.image.load(os.path.join("imgs", "Lock.png"))
        pygame.draw.rect(win, "dimgrey",[250, 0, 5 ,600])
        pygame.draw.rect(win, "dimgrey",[650, 0, 5 ,600])
        win.blit(FONT_LOGIN.render("Selecionar nivel", True, "white"), (350, 0))
        pygame.draw.circle(win, "black",[350, 150], 80)
        win.blit(FONT_NIVEL.render("1", True, "white"), (325, 90))
        pygame.draw.circle(win, "black",[550, 500], 80)
        win.blit(FONT_NIVEL.render("INF", True, "white"), (490, 440))
        
        if self.lv2_desbloqueado:
            pygame.draw.circle(win, "black",[550, 150], 80)
            win.blit(FONT_NIVEL.render("2", True, "white"), (525, 90))
        else:
            pygame.draw.circle(win, "azure4",[550, 150], 80)
            win.blit(cadeado, (525, 125))
        if self.lv3_desbloqueado:
            pygame.draw.circle(win, "black",[350, 325], 80)
            win.blit(FONT_NIVEL.render("3", True, "white"), (325, 265))
        else:
            pygame.draw.circle(win, "azure4",[350, 325], 80)
            win.blit(cadeado, (325, 300))
        if self.lv4_desbloqueado:
            pygame.draw.circle(win, "black",[550, 325], 80)
            win.blit(FONT_NIVEL.render("4", True, "white"), (525, 265))
        else:
            pygame.draw.circle(win, "azure4",[550, 325], 80)
            win.blit(cadeado, (525, 300))
        if self.lv5_desbloqueado:
            pygame.draw.circle(win, "black",[350, 500], 80)
            win.blit(FONT_NIVEL.render("5", True, "white"), (325, 440))
        else:
            pygame.draw.circle(win, "azure4",[350, 500], 80)
            win.blit(cadeado, (325, 475))
        mpos = pygame.mouse.get_pos()

        if self.lv1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.lv_aberto = True
            self.lv1_aberto = True
        elif self.lv2.collidepoint(mpos) and pygame.mouse.get_pressed()[0] and xp >= 1000:
            self.lv_aberto = True
            self.lv2_aberto = True
        elif self.lv3.collidepoint(mpos) and pygame.mouse.get_pressed()[0] and xp >= 2000:
            self.lv_aberto = True
            self.lv3_aberto = True
        elif self.lv4.collidepoint(mpos) and pygame.mouse.get_pressed()[0] and xp >= 3000:
            self.lv_aberto = True
            self.lv4_aberto = True
        elif self.lv5.collidepoint(mpos) and pygame.mouse.get_pressed()[0] and xp >= 4000:
            self.lv_aberto = True
            self.lv5_aberto = True
        elif self.lv_endless.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.lv_aberto = True
            self.lv_endless_aberto = True
        
        if self.lv_aberto == False:
            self.lv1_aberto = False
            self.lv2_aberto = False
            self.lv3_aberto = False
            self.lv4_aberto = False
            self.lv5_aberto = False
            self.lv_endless_aberto = False

class Pergunta(SeletorDeNivel, Jogador):
    def __init__(self):
        self.voltar_ok = False
        self.perguntas_lv1 = ["7 // 2 vale quanto?", "print 'Hello, ', 'world', tera qual resultado no console?'"]
        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
        self.resp1 = pygame.Rect(10, 170, 200, 100)
        self.resp2 = pygame.Rect(250, 170, 200, 100)
        self.resp3 = pygame.Rect(10, 300, 200, 100)
        self.resp4 = pygame.Rect(250, 300, 200, 100)
    
    def nivel(self, lv1_aberto, lv2_aberto, lv3_aberto, lv4_aberto, lv5_aberto, lv_endless_aberto, voltar_rect_pergunta, lv_aberto):
        troca_ok = False
        global level
        global acertos
        global streak
        mpos = pygame.mouse.get_pos()
        if lv1_aberto:
            level = 1
            pygame.draw.rect(win, "azure4",[10, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[10, 300, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 300, 200, 100])
            win.blit(FONT_LOGIN.render("Nivel 1", True, "white"), (400, 0))
            win.blit(FONT_PERGUNTA.render(self.perguntas_lv1[self.lv1_index], True, "white"), (20, 40))
            if self.perguntas_lv1[self.lv1_index] == "print 'Hello, ', 'world', tera qual resultado no console?'":
                win.blit(FONT_PERGUNTA.render("Hello, world", True, "white"), (10, 170))
                win.blit(FONT_PERGUNTA.render("Hello, ", True, "white"), (250, 170))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "white"), (10, 300))
                win.blit(FONT_PERGUNTA.render("world", True, "white"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    streak = 1
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    streak = 1
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                        if self.lv1_index != 1:
                            troca_ok = True
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    streak = 1
        elif lv2_aberto:
            level = 2
            win.blit(FONT_LOGIN.render("Nivel 2", True, "white"), (400, 0))
        elif lv3_aberto:
            level = 3
            win.blit(FONT_LOGIN.render("Nivel 3", True, "white"), (400, 0))
        elif lv4_aberto:
            level = 4
            win.blit(FONT_LOGIN.render("Nivel 4", True, "white"), (400, 0))
        elif lv5_aberto:
            level = 5
            win.blit(FONT_LOGIN.render("Nivel 5", True, "white"), (400, 0))
        elif lv_endless_aberto:
            win.blit(FONT_LOGIN.render("Nivel INF", True, "white"), (400, 0))
        
        if lv_aberto:
                voltar = FONT_LOGIN.render("Voltar", True, "white")
                win.blit(voltar,(400, 500))
                if voltar_rect_pergunta.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    self.voltar_ok = True
                    self.xp_novo = self.calcular_xp(acertos, streak, level)
                    login.banco_de_dados(login.moedas, login.xp)
                    acertos = 0
                    streak = 0
                    level = 0
                    self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
    
    def calcular_xp(self, acertos, streak, level): 
        xp_novo =  acertos * 10 * level * (1 + streak / 10)
        return xp_novo
    
    def calcular_moedas(self):
        return self.acertos * 25 * self.level * (self.streak / 10)
class Login(Pergunta):
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
        self.pergunta = Pergunta()
        self.moedas = 0
        self.xp = 0
    
    def mostrar_xpmoedas(self):
        xp = FONT_MOEDAS.render("XP:" + str(self.xp), True, "white")
        win.blit(xp, (750, 100))
        moedas = FONT_MOEDAS.render("Moedas:" + str(self.moedas), True, "white")
        win.blit(moedas, (700, 200))

    def banco_de_dados(self, moedas, xp):
        with psycopg.connect(
            dbname="neondb",
            user="Parelho",
            password="ns3Nolki1RzC",
            host="ep-little-field-610508.us-east-2.aws.neon.tech",
            port= '5432'
            ) as db:
            with db.cursor() as cursor:

                if self.cadastro_pronto == True:
                    add_usuario = "INSERT INTO Usuario VALUES(%s, %s, %s, %s);"
                    data_usuario = (self.usuario, self.senha, xp, moedas)
                    cursor.execute(add_usuario, data_usuario)
                    db.commit()
                    self.cadastro_pronto = False
                
                if self.login_pronto:
                    query = "SELECT * FROM Usuario"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    usuario_encontrado = False

                    for row in rows:
                        if self.usuario == row[0] and self.senha == row[1]:
                            print("Usuario encontrado")
                            self.xp = int(row[2])
                            self.login_pronto = False
                            self.inicio = False
                            self.login = False
                            usuario_encontrado = True
                            break
                    else:
                        if not usuario_encontrado:
                            print("Usuario nao encontrado")
                            self.login_pronto = False

                if pergunta.voltar_ok:
                    global acertos
                    global level
                    global streak
                    xp_nova = int(self.xp + self.calcular_xp(acertos, streak, level))
                    query = f"UPDATE usuario SET xp = '{xp_nova}' WHERE username = '{self.usuario}';"
                    cursor.execute(query)
                    self.xp = xp_nova
          

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
            self.login = False

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
            self.cadastro = False
    
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
            self.cadastro = False
            self.inicio = True

    def tela_inicio(self):
        bem_vindo = FONT.render("CodeQuiz", True, "white")
        win.blit(bem_vindo, (350, 100))

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
            login.banco_de_dados(login.moedas, login.xp)
    # Se login for False, será aberta a tela de cadastro
    elif login.cadastro:
        login.fazer_cadastro()
        if login.cadastro_pronto:
            login.banco_de_dados(login.moedas, login.xp)
    
    if login.inicio == False and login.login == False and login.cadastro == False:
        if jogador.opcoes_aberto == False and jogador.loja_aberta == False and nivel.lv_aberto == False:
            jogador.menu_principal()
            login.mostrar_xpmoedas()
            nivel.selecionar_nivel(login.xp)
        elif jogador.opcoes_aberto:
            jogador.opcoes()
        elif jogador.loja_aberta:
            jogador.loja()
        elif nivel.lv_aberto:
            pergunta.nivel(nivel.lv1_aberto, nivel.lv2_aberto, nivel.lv3_aberto, nivel.lv4_aberto, nivel.lv5_aberto, nivel.lv_endless_aberto , nivel.voltar_rect_pergunta, nivel.lv_aberto)
            if pergunta.voltar_ok:
                nivel.lv_aberto = False
                pergunta.voltar_ok = False
                time.sleep(0.5)


    # Da update nos métodos do pygame
    pygame.display.update()
    # Taxa de FPS, atualmente está 60 FPS
    clock.tick(60)
# Para as operações do pygame para garantir que o código vai terminar de ser executado
pygame.quit()