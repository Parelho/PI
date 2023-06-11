import pygame
import pygame_textinput
import time
import psycopg
import os
import random
import openai
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("api_key")

# Inicializa o pygame
pygame.init()
pygame.display.set_caption('CodeQuiz')
# Utilizados como workaround de um bug que estava impedindo a classe Login de pegar os valores atualizados de acertos, level e streak, se conseguir resolver o bug irei remover essa mostruosidade
acertos = 0
level = 0
streak = 0
coins = 0
logoff = False
boost = False
boost_ok = False
shield = False
shield_ok = False
fechar = False

def gerar_texto_chatgpt():
    try:
        global completion
        completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "Uma pergunta simples com respostas curtas sobre programar em Python. de 4 alternativas, sendo apenas 1 correta informe a resposta correta na primeira alternativa"}
                    ]
                    )
    except:
        print("erro de conexao a api da openai")

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
        self.tema = "oldlace"
        self.tema_rect = pygame.Rect(675, 100, 200, 100)
        self.tema_roxo_rect = pygame.Rect(450, 100, 200, 100)
        self.tema_verde_rect = pygame.Rect(450, 250, 200, 100)
        self.tema_azul_rect = pygame.Rect(675, 250, 200, 100)
        self.engrenagem_rect = pygame.Rect(20, 500, 100, 100)
        self.loja_rect = pygame.Rect(120, 500, 100, 100)
        self.voltar_rect = pygame.Rect(400, 500, 100, 30)
        self.boost_rect = pygame.Rect(20, 20, 80, 80)
        self.shield_rect = pygame.Rect(20, 220, 128, 128)
        self.logout_rect = pygame.Rect(20, 450, 128, 128)
        self.opcoes_aberto = False
        self.loja_aberta = False
        self.login = Login()

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

        mensagem = FONT_MASCOTE.render("Bem Vindo ao CodeQuiz!", True, "black")
        win.blit(mensagem, (0, 0))

        #Opcoes
        engrenagem = pygame.image.load(os.path.join("imgs", "engrenagem.png"))
        win.blit(engrenagem, (20, 500))

        if self.engrenagem_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.opcoes_aberto = True
            time.sleep(0.2)

    def opcoes(self):
        mpos = pygame.mouse.get_pos()
        if self.tema_roxo_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.tema = "mediumpurple4"
        elif self.tema_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.tema = "oldlace"
        elif self.tema_verde_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.tema = "lightgreen"
        elif self.tema_azul_rect.collidepoint(mpos):
            if pygame.mouse.get_pressed()[0]:
                self.tema = "royalblue3"


        pygame.draw.rect(win, self.tema, self.tema_roxo_rect)
        win.fill(self.tema, self.tema_roxo_rect)

        pygame.draw.rect(win, "black",[445, 95, 210, 110])
        pygame.draw.rect(win, "mediumpurple4",[450, 100, 200, 100])
        pygame.draw.rect(win, "black",[670, 95, 210, 110])
        pygame.draw.rect(win, "oldlace",[675, 100, 200, 100])
        pygame.draw.rect(win, "black",[445, 245, 210, 110])
        pygame.draw.rect(win, "lightgreen",[450, 250, 200, 100])
        pygame.draw.rect(win, "black",[670, 245, 210, 110])
        pygame.draw.rect(win, "royalblue3",[675, 250, 200, 100])

        temas = FONT_LOGIN.render("Clique para mudar de tema", True, "black")
        win.blit(temas,(450, 0))

        voltar = FONT_LOGIN.render("Voltar", True, "black")
        win.blit(voltar,(400, 500))
        if self.voltar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.opcoes_aberto = False
        
        logout = pygame.image.load(os.path.join("imgs", "Exit.png"))
        win.blit(logout, (20, 450))
        if self.logout_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.opcoes_aberto = False
            global logoff
            logoff = True
            time.sleep(0.2)
        
    def loja(self):
        mpos = pygame.mouse.get_pos()

        voltar = FONT_LOGIN.render("Voltar", True, "black")
        win.blit(voltar,(400, 500))
        if self.voltar_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.loja_aberta = False
        
        bonus = pygame.image.load(os.path.join("imgs", "Boost.png"))
        win.blit(bonus, (20, 20))
        bonus_texto = FONT_LOGIN.render("Boost de Pontos", True, "black")
        win.blit(bonus_texto,(100, 20))
        global boost
        if self.boost_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0] and boost == False:
            boost = True
        
        protecao = pygame.image.load(os.path.join("imgs", "shield.png"))
        win.blit(protecao, (20, 220))
        protecao_texto = FONT_LOGIN.render("Proteção de Streak", True, "black")
        win.blit(protecao_texto, (150, 220))
        global shield
        if self.shield_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0] and shield == False:
            shield = True

class SeletorDeNivel():
    def __init__(self):
        self.voltar_rect_pergunta = pygame.Rect(400, 500, 100, 30)
        self.lv1 = pygame.Rect(270, 70, 160, 160)
        self.lv2 = pygame.Rect(470, 70, 160, 160)
        self.lv3 = pygame.Rect(270, 245, 160, 160)
        self.lv_endless = pygame.Rect(470, 245, 160, 160)
        self.lv1_aberto = False
        self.lv2_aberto = False
        self.lv3_aberto = False
        self.lv_endless_aberto = False
        self.lv_aberto = False
        self.lv2_desbloqueado = False
        self.lv3_desbloqueado = False
    
    def selecionar_nivel(self, xp):
        if xp >= 1000:
            self.lv2_desbloqueado = True
            if xp >= 2000:
                self.lv3_desbloqueado = True
    
        cadeado = pygame.image.load(os.path.join("imgs", "Lock.png"))
        pygame.draw.rect(win, "dimgrey",[250, 0, 5 ,600])
        pygame.draw.rect(win, "dimgrey",[650, 0, 5 ,600])
        win.blit(FONT_LOGIN.render("Selecionar nivel", True, "black"), (350, 0))
        pygame.draw.circle(win, "black",[350, 150], 80)
        win.blit(FONT_NIVEL.render("1", True, "white"), (325, 90))
        pygame.draw.circle(win, "black",[550, 325], 80)
        win.blit(FONT_NIVEL.render("INF", True, "white"), (490, 265))
        
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
        elif self.lv_endless.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            self.lv_aberto = True
            self.lv_endless_aberto = True
        
        if self.lv_aberto == False:
            self.lv1_aberto = False
            self.lv2_aberto = False
            self.lv3_aberto = False
            self.lv_endless_aberto = False

class Pergunta(SeletorDeNivel, Jogador):
    def __init__(self):
        self.voltar_ok = False
        self.perguntas_lv1 = ["7 // 2 vale quanto?", "print 'Hello, ', 'world', tera qual resultado no console?'", "10 % 2 vale quanto?", "Qual o simbolo utilizado para adicionar comentarios?", "100 / 0 vale quanto?"]
        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
        self.perguntas_lv2 = ["print('Hello' + 'world') terá qual resultado?", "idade = 7 + 5 = 4, idade terá qual valor?", "7.5 // 2 vale quanto", "Como posso criar uma função em Python?", "Como posso contar a frequência de elementos em uma lista em Python?"]
        self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
        self.perguntas_lv3 = ["Como posso verificar se uma lista está vazia em Python?", "Como posso converter uma string em maiúsculas em Python?", "Como posso criar um dicionário vazio em Python?", "Como posso criar uma classe em python?", "Como faço para instalar um pacote externo em Python usando o pip?"]
        self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
        self.resp1 = pygame.Rect(10, 170, 200, 100)
        self.resp2 = pygame.Rect(250, 170, 200, 100)
        self.resp3 = pygame.Rect(10, 300, 200, 100)
        self.resp4 = pygame.Rect(250, 300, 200, 100)
        self.nova_pergunta = pygame.Rect(325, 425, 250, 30)
        self.resposta = Resposta()
        self.respostas_ok = False
        self.pergunta_ok = False
        self.correta = 0
        self.acerto = False
        self.erro = False
        self.shuffle_ok = False
        self.resp_certa = ""
        self.respostas = []
    
    def nivel(self, lv1_aberto, lv2_aberto, lv3_aberto, lv_endless_aberto, voltar_rect_pergunta, lv_aberto):
        troca_ok = False
        global level
        global acertos
        global streak
        global shield
        win.blit(FONT_LOGIN.render("Streak: " + str(streak), True, "black"), (600, 0))
        mpos = pygame.mouse.get_pos()
        if lv1_aberto:
            level = 1
            pygame.draw.rect(win, "azure4",[10, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[10, 300, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 300, 200, 100])
            win.blit(FONT_LOGIN.render("Nivel 1", True, "black"), (400, 0))
            win.blit(FONT_PERGUNTA.render(self.perguntas_lv1[self.lv1_index], True, "black"), (20, 40))
            if self.perguntas_lv1[self.lv1_index] == "7 // 2 vale quanto?":
                win.blit(FONT_PERGUNTA.render("3.5", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("3", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("4", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                        if self.lv1_index != 0:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv1[self.lv1_index] == "print 'Hello, ', 'world', tera qual resultado no console?'":
                win.blit(FONT_PERGUNTA.render("Hello, world", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("Hello, ", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("world", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                        if self.lv1_index != 1:
                            troca_ok = True
                            time.sleep(0.5)
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv1[self.lv1_index] == "10 % 2 vale quanto?":
                win.blit(FONT_PERGUNTA.render("0", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("5, ", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("0.2", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                        if self.lv1_index != 2:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv1[self.lv1_index] == "Qual o simbolo utilizado para adicionar comentarios?":
                win.blit(FONT_PERGUNTA.render("#", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("//", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("/*   */", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("<!--   -->", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                        if self.lv1_index != 3:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv1[self.lv1_index] == "100 / 0 vale quanto?":
                win.blit(FONT_PERGUNTA.render("0", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("100", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("False", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                        if self.lv1_index != 4:
                            troca_ok = True
                            time.sleep(0.5)
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
        elif lv2_aberto:
            level = 2
            pygame.draw.rect(win, "azure4",[10, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[10, 300, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 300, 200, 100])
            win.blit(FONT_LOGIN.render("Nivel 2", True, "black"), (400, 0))
            win.blit(FONT_PERGUNTA.render(self.perguntas_lv2[self.lv2_index], True, "black"), (20, 40))
            if self.perguntas_lv2[self.lv2_index] == "print('Hello' + 'world') terá qual resultado?":
                win.blit(FONT_PERGUNTA.render("Hello world", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("Helloworld", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("Hello+world", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
                        if self.lv2_index != 0:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv2[self.lv2_index] == "idade = 7 + 5 = 4, idade terá qual valor?":
                win.blit(FONT_PERGUNTA.render("idade = 4", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("idade = 12", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de sintaxe", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("idade = 8", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
                        if self.lv2_index != 1:
                            troca_ok = True
                            time.sleep(0.5)
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv2[self.lv2_index] == "7.5 // 2 vale quanto":
                win.blit(FONT_PERGUNTA.render("3", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("3.5, ", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("4", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("Vai dar erro de compilação", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
                        if self.lv2_index != 2:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv2[self.lv2_index] == "Como posso criar uma função em Python?":
                win.blit(FONT_PERGUNTA.render("def", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("func", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("method", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("class", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
                        if self.lv2_index != 3:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv2[self.lv2_index] == "Como posso contar a frequência de elementos em uma lista em Python?":
                win.blit(FONT_PERGUNTA.render("len()", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("sum()", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("count()", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("find()", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
                        if self.lv2_index != 4:
                            troca_ok = True
                            time.sleep(0.5)
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
        elif lv3_aberto:
            level = 3
            pygame.draw.rect(win, "azure4",[10, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[10, 300, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 300, 200, 100])
            win.blit(FONT_LOGIN.render("Nivel 3", True, "black"), (400, 0))
            win.blit(FONT_PERGUNTA.render(self.perguntas_lv3[self.lv3_index], True, "black"), (20, 40))
            if self.perguntas_lv3[self.lv3_index] == "Como posso verificar se uma lista está vazia em Python?":
                win.blit(FONT_PERGUNTA.render("is_empty()", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("len()", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("check_empty()", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("empty()", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
                        if self.lv3_index != 0:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv3[self.lv3_index] == "Como posso converter uma string em maiúsculas em Python?":
                win.blit(FONT_PERGUNTA.render("uppercase()", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("convert_upper()", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("upper()", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("to_upper()", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
                        if self.lv3_index != 1:
                            troca_ok = True
                            time.sleep(0.5)
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv3[self.lv3_index] == "Como posso criar um dicionário vazio em Python?":
                win.blit(FONT_PERGUNTA.render("dicionario = {}", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("dicionario = dict", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("dicionario = dict()", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("dicionario = []", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
                        if self.lv3_index != 2:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv3[self.lv3_index] == "Como posso criar uma classe em python?":
                win.blit(FONT_PERGUNTA.render("class", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("def", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("public class", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("<nome_da_classe>", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    acertos += 1
                    streak += 1
                    while troca_ok == False:
                        self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
                        if self.lv3_index != 3:
                            troca_ok = True
                            time.sleep(0.5)
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
            elif self.perguntas_lv3[self.lv3_index] == "Como faço para instalar um pacote externo em Python usando o pip?":
                win.blit(FONT_PERGUNTA.render("pip install 'nomedopacote'", True, "black"), (10, 170))
                win.blit(FONT_PERGUNTA.render("python -m pip install nomedopacote", True, "black"), (250, 170))
                win.blit(FONT_PERGUNTA.render("pip install nomedopacote", True, "black"), (10, 300))
                win.blit(FONT_PERGUNTA.render("pip install nomedopacote==versao", True, "black"), (250, 300))
                if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
                elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    while troca_ok == False:
                        self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
                        if self.lv3_index != 4:
                            troca_ok = True
                            time.sleep(0.5)
                    acertos += 1
                    streak += 1
                elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    if shield:
                        shield = False
                        time.sleep(0.5)
                    else:
                        streak = 0
        elif lv_endless_aberto:
            win.blit(FONT_LOGIN.render("Nivel INF", True, "black"), (400, 0))
            win.blit(FONT_LOGIN.render("Gerar outra pergunta", True, "black"), (325, 425))
            pygame.draw.rect(win, "azure4",[10, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 170, 200, 100])
            pygame.draw.rect(win, "azure4",[10, 300, 200, 100])
            pygame.draw.rect(win, "azure4",[250, 300, 200, 100])
            if self.nova_pergunta.collidepoint(mpos) and pygame.mouse.get_pressed()[0] or self.pergunta_ok == False:
                self.pergunta_ok = True
                self.shuffle_ok = False
                gerar_texto_chatgpt()

            global completion
            pattern = r"\n|\?|a\)|b\)|c\)|d\)"
            string = completion.choices[0].message.content
            elementos = re.split(pattern, string)
            elementos = [element for element in elementos if element.strip()]
            
            
            if not self.shuffle_ok:
                self.resp_certa = elementos[1]
                self.respostas.clear()
                self.respostas.append(elementos[1])
                self.respostas.append(elementos[2])
                self.respostas.append(elementos[3])
                self.respostas.append(elementos[4])
                random.shuffle(self.respostas)

                if self.resp_certa in self.respostas[0]:
                    self.correta = 1
                elif self.resp_certa in self.respostas[1]:
                    self.correta = 2
                elif self.resp_certa in self.respostas[2]:
                    self.correta = 3
                elif self.resp_certa in self.respostas[3]:
                    self.correta = 4
                
                self.shuffle_ok = True

            pergunta = elementos[0]
            win.blit(FONT_PERGUNTA.render(pergunta, True, "black"), (0, 50))
            win.blit(FONT_PERGUNTA.render(self.respostas[0], True, "black"), (10, 170))
            win.blit(FONT_PERGUNTA.render(self.respostas[1], True, "black"), (250, 170))
            win.blit(FONT_PERGUNTA.render(self.respostas[2], True, "black"), (10, 300))
            win.blit(FONT_PERGUNTA.render(self.respostas[3], True, "black"), (250, 300))
            
            if self.resp1.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                if self.correta == 1:
                    self.acerto = True
                else:
                    self.erro = True
            elif self.resp2.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                if self.correta == 2:
                    self.acerto = True
                else:
                    self.erro = True
            elif self.resp3.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                if self.correta == 3:
                    self.acerto = True
                else:
                    self.erro = True
            elif self.resp4.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                if self.correta == 4:
                    self.acerto = True
                else:
                    self.erro = True

            if self.acerto and self.erro == False:
                msg = FONT_MOEDAS.render("Acertou :)", True, "black")
                win.blit(msg, (720, 110))
                self.erro = False
                
            if self.erro and self.acerto == False:
                msg = FONT_MOEDAS.render("Errou :(", True, "black")
                win.blit(msg, (720, 110))
                self.acerto = False
            
            if self.erro == True and self.acerto == True:
                self.erro = False
                self.acerto = False
        
        if lv_aberto:
                voltar = FONT_LOGIN.render("Voltar", True, "black")
                win.blit(voltar,(400, 500))
                if voltar_rect_pergunta.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
                    self.voltar_ok = True
                    login.banco_de_dados(login.moedas, login.xp)
                    acertos = 0
                    streak = 0
                    level = 0
                    self.lv1_index = random.randint(0, len(self.perguntas_lv1) - 1)
                    self.lv2_index = random.randint(0, len(self.perguntas_lv2) - 1)
                    self.lv3_index = random.randint(0, len(self.perguntas_lv3) - 1)
                    self.respostas_ok = False
    
class Resposta(Pergunta):
    def __init__(self):
        pass

    def calcular_pontos(self, acertos, streak, level):
        formula = acertos * 100 * level * (1 + streak / 10)
        global boost
        global boost_ok
        if boost and formula != 0:
            pontos = formula * 1.25
            boost = False
            boost_ok = False
        else:
            pontos = formula
        return pontos

    def calcular_xp(self): 
        xp_novo = self.calcular_pontos(acertos, streak, level) / 10
        return xp_novo
    
    def calcular_moedas(self):
        moedas_novo = self.calcular_pontos(acertos, streak, level) / 4
        return moedas_novo

class Login(Pergunta):
    global coins
    # Método utilizado para permitir a sobrecarga de métodos no Python
    def __init__(self):
        self.inicio = True
        self.login = False
        self.cadastro = False
        self.sair_rect = pygame.Rect(830, 0, 64, 64)
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
        self.resposta = Resposta()
        self.moedas = coins
        self.xp = 0
    
    def mostrar_xpmoedas(self):
        xp = FONT_MOEDAS.render(str(self.xp), True, "black")
        win.blit(xp, (765, 110))
        moedas = FONT_MOEDAS.render(str(self.moedas), True, "black")
        win.blit(moedas, (765, 210))
        xp_img = pygame.image.load(os.path.join("imgs", "Xp.png"))
        win.blit(xp_img, (700, 100))
        moedas_img = pygame.image.load(os.path.join("imgs", "Coin.png"))
        win.blit(moedas_img, (700, 200))

    def banco_de_dados(self, moedas, xp):
        try:
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
                                self.moedas = int(row[3])
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
                        xp_nova = int(self.xp + self.resposta.calcular_xp())
                        query = f"UPDATE usuario SET xp = '{xp_nova}' WHERE username = '{self.usuario}';"
                        cursor.execute(query)
                        self.xp = xp_nova
                        moedas_nova = int(self.moedas + self.resposta.calcular_moedas())
                        query = f"UPDATE usuario SET moedas = '{moedas_nova}' WHERE username = '{self.usuario}';"
                        cursor.execute(query)
                        self.moedas = moedas_nova
                        coins = self.moedas
                    
                    global boost
                    if boost:
                        if self.moedas < 100:
                            boost = False
                        else:
                            coins_novo = self.moedas - 100
                            query = f"UPDATE usuario SET moedas = '{coins_novo}' WHERE username = '{self.usuario}';"
                            cursor.execute(query)
                            self.moedas = coins_novo
                    global shield
                    global shield_ok
                    if shield:
                        if self.moedas < 100:
                            shield = False
                        else:
                            coins_novo = self.moedas - 100
                            query = f"UPDATE usuario SET moedas = '{coins_novo}' WHERE username = '{self.usuario}';"
                            cursor.execute(query)
                            self.moedas = coins_novo
                            shield_ok = True
        except:
            print("Erro de conexao com o banco de dados")

    def fazer_login(self):
        # Mostrando os campos de usuário e senha para o jogador
        usuario = FONT_LOGIN.render("Usuario: ", True, "black")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "black")
        win.blit(senha, (100, 192))
        voltar = FONT_LOGIN.render("Voltar", True, "black")
        win.blit(voltar,(400, 500))
        enviar = FONT_LOGIN.render("Enviar", True, "black")
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
            textinput_usuario.value = ""
            textinput_senha.value = ""

       # Similar ao método de login, fora a parte que está comentada
    def fazer_cadastro(self):
        usuario = FONT_LOGIN.render("Usuario: ", True, "black")
        win.blit(usuario, (95, 92))
        senha = FONT_LOGIN.render("Senha: ", True, "black")
        win.blit(senha, (100, 192))
        voltar = FONT_LOGIN.render("Voltar", True, "black")
        win.blit(voltar,(400, 500))
        enviar = FONT_LOGIN.render("Enviar", True, "black")
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
            textinput_usuario.value = ""
            textinput_senha.value = ""
    def tela_inicio(self):
        mpos = pygame.mouse.get_pos()
        sair = pygame.image.load(os.path.join("imgs", "Close.png"))
        win.blit(sair, (830, 0))
        if self.sair_rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
            global fechar
            fechar = True

        bem_vindo = FONT.render("CodeQuiz", True, "black")
        win.blit(bem_vindo, (350, 100))

        cadastrar = FONT.render("Cadastrar", True, "black")
        win.blit(cadastrar, (500, 300))
        login = FONT.render("Login", True, "black")
        win.blit(login, (200, 300))

        # Checa se o mouse está em cima do botão de cadastro
        global logoff
        if logoff:
            self.inicio = True
            logoff = False
    
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
        if event.type == pygame.QUIT or fechar == True:
            running = False
    # Coloca o tema do fundo na tela atrás de todo o resto que for desenhado
    win.fill(jogador.tema)

    if logoff == True:
        login.tela_inicio()
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
    
    elif login.inicio == False and login.login == False and login.cadastro == False:
        if jogador.opcoes_aberto == False and jogador.loja_aberta == False and nivel.lv_aberto == False:
            jogador.menu_principal()
            login.mostrar_xpmoedas()
            nivel.selecionar_nivel(login.xp)
        elif jogador.opcoes_aberto:
            jogador.opcoes()
        elif jogador.loja_aberta:
            jogador.loja()
            if boost == True and login.moedas >= 100 and boost_ok == False:
                login.banco_de_dados(login.moedas, login.xp)
                boost_ok = True
            if shield == True and login.moedas >= 100 and shield_ok == False:
                login.banco_de_dados(login.moedas, login.xp)
        elif nivel.lv_aberto:
            pergunta.nivel(nivel.lv1_aberto, nivel.lv2_aberto, nivel.lv3_aberto, nivel.lv_endless_aberto , nivel.voltar_rect_pergunta, nivel.lv_aberto)
            if pergunta.voltar_ok:
                nivel.lv_aberto = False
                pergunta.voltar_ok = False
                time.sleep(0.5)


    # Da update nos métodos do pygame
    pygame.display.update()
    # Taxa de FPS, atualmente está 30 FPS
    clock.tick(30)
# Para as operações do pygame para garantir que o código vai terminar de ser executado
pygame.quit()