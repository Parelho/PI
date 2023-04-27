import pygame

pygame.init()

win = pygame.display.set_mode((900,600))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("timesnewroman", 50)

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
        

running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    win.fill("lime")
    clock.tick(60)

    Login.tela_inicio()
    pygame.display.update()

pygame.quit()