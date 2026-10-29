import re
import unicodedata
from pathlib import Path
import pygame
from heroi import Heroi

LARGURA, ALTURA = 960, 640
PASTA_IMAGENS = Path(__file__).parent / "imagens"
ALTURA_SPRITE = 190
CHAO = 338
ESPELHAR_VILOES = True
TEXTO, SUAVE, PAINEL, BORDA = (240, 240, 250), (170, 175, 200), (20, 22, 34), (90, 96, 130)
VERDE, VERMELHO, AZUL = (80, 200, 120), (220, 70, 70), (80, 150, 235)
OURO, ROXO, LARANJA, CINZA = (240, 200, 80), (150, 100, 220), (235, 140, 70), (70, 72, 90)
VERMELHO_BOTAO, MARROM, AZUL_ESCURO, AMARELO = (190, 40, 40), (120, 72, 40), (30, 50, 120), (255, 220, 60)

def sem_emoji(texto):
    return re.sub(r"[^\u0000-\u1FFF]", "", texto).strip()

def nome_arquivo(nome):
    base = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return "_".join(base.lower().split())

def carregar_imagem(nome):
    for extensao in ("png", "jpg"):
        caminho = PASTA_IMAGENS / f"{nome}.{extensao}"
        if caminho.exists():
            return pygame.image.load(str(caminho)).convert_alpha()
    return None

def cor_vida(personagem):
    proporcao = personagem.vida / personagem.vida_max
    return VERDE if proporcao > 0.5 else OURO if proporcao > 0.25 else VERMELHO

def cartas(quantidade):
    largura, espaco = 380, 40
    x0 = (LARGURA - quantidade * largura - (quantidade - 1) * espaco) // 2
    return [pygame.Rect(x0 + i * (largura + espaco), 110, largura, 480) for i in range(quantidade)]

class Desenho:
    def __init__(self, tela):
        self.tela = tela
        fontes = "segoeui,arial,helvetica,dejavusans"
        self.f_titulo = pygame.font.SysFont(fontes, 30, bold=True)
        self.f_grande = pygame.font.SysFont(fontes, 22, bold=True)
        self.f_texto = pygame.font.SysFont(fontes, 18)
        self.f_botao = pygame.font.SysFont(fontes, 18, bold=True)
        self.f_pequena = pygame.font.SysFont(fontes, 16)
        self.sprites = {}
        self.fundo = carregar_imagem("fundo")
        if self.fundo:
            self.fundo = pygame.transform.smoothscale(self.fundo, (LARGURA, ALTURA))

    def sprite(self, nome):
        if nome not in self.sprites:
            imagem = carregar_imagem(nome_arquivo(nome))
            if imagem:
                largura = imagem.get_width() * ALTURA_SPRITE // imagem.get_height()
                imagem = pygame.transform.smoothscale(imagem, (largura, ALTURA_SPRITE))
            self.sprites[nome] = imagem
        return self.sprites[nome]

    def texto(self, conteudo, x, y, cor=TEXTO, fonte=None, centro=False, sombra=False):
        if sombra:
            self.texto(conteudo, x + 2, y + 2, (0, 0, 0), fonte, centro)
        imagem = (fonte or self.f_texto).render(conteudo, True, cor)
        posicao = imagem.get_rect(midtop=(x, y)) if centro else imagem.get_rect(topleft=(x, y))
        self.tela.blit(imagem, posicao)

    def painel(self, rect, alpha=185, borda=BORDA):
        rect = pygame.Rect(rect)
        camada = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(camada, (*PAINEL, alpha), camada.get_rect(), border_radius=12)
        self.tela.blit(camada, rect)
        pygame.draw.rect(self.tela, borda, rect, 2, border_radius=12)

    def barra(self, x, y, largura, altura, valor, maximo, cor):
        pygame.draw.rect(self.tela, CINZA, (x, y, largura, altura), border_radius=6)
        cheio = int(largura * max(0, valor) / maximo)
        if cheio:
            pygame.draw.rect(self.tela, cor, (x, y, cheio, altura), border_radius=6)
        pygame.draw.rect(self.tela, BORDA, (x, y, largura, altura), 2, border_radius=6)

    def botao(self, botao, mouse):
        cor = botao.cor if botao.ativo else CINZA
        if botao.ativo and botao.rect.collidepoint(mouse):
            cor = tuple(min(255, c + 35) for c in cor)
        pygame.draw.rect(self.tela, cor, botao.rect, border_radius=10)
        imagem = self.f_botao.render(botao.rotulo, True, AMARELO if botao.ativo else SUAVE)
        self.tela.blit(imagem, imagem.get_rect(center=botao.rect.center))

    def cenario(self):
        if self.fundo:
            self.tela.blit(self.fundo, (0, 0))
        else:
            self.tela.fill((30, 34, 52))

    def figura(self, nome, x, chao=CHAO, espelhar=False, cor=AZUL):
        imagem = self.sprite(nome)
        if imagem is None:
            corpo = pygame.Rect(0, 0, 70, 100)
            corpo.midbottom = (x, chao)
            pygame.draw.rect(self.tela, cor, corpo, border_radius=14)
            pygame.draw.circle(self.tela, (240, 215, 185), (x, corpo.top - 18), 28)
            return corpo
        if espelhar:
            imagem = pygame.transform.flip(imagem, True, False)
        area = imagem.get_rect(midbottom=(x, chao))
        self.tela.blit(imagem, area)
        return area

    def personagem(self, personagem, x, vilao=False):
        area = self.figura(personagem.nome, x, espelhar=vilao and ESPELHAR_VILOES,
                        cor=VERMELHO if vilao else AZUL)
        if personagem.defendendo:
            pygame.draw.ellipse(self.tela, AZUL, area.inflate(50, 30), 4)

    def hud(self, personagem, x):
        self.painel((x, 52, 320, 88))
        self.texto(personagem.nome, x + 12, 58)
        numeros = f"{personagem.vida}/{personagem.vida_max}"
        self.texto(numeros, x + 308 - self.f_texto.size(numeros)[0], 58, SUAVE)
        self.barra(x + 12, 84, 296, 16, personagem.vida, personagem.vida_max, cor_vida(personagem))
        if isinstance(personagem, Heroi):
            self.barra(x + 12, 110, 200, 10, personagem.mana, personagem.mana_max, AZUL)
            self.texto(f"Mana {personagem.mana}/{personagem.mana_max}", x + 222, 106, SUAVE, self.f_pequena)
        else:
            self.texto(f"Maldade: {personagem.maldade}", x + 12, 106, LARANJA, self.f_pequena)

    def quebrar(self, conteudo, largura):
        linhas, atual = [], ""
        for palavra in conteudo.split():
            teste = f"{atual} {palavra}".strip()
            if self.f_pequena.size(teste)[0] <= largura:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        return linhas + [atual]

    def mensagens(self, mensagens):
        self.painel((20, 350, 580, 280))
        visiveis = []
        for conteudo, cor in reversed(mensagens[-12:]):
            visiveis = [(parte, cor) for parte in self.quebrar(conteudo, 552)] + visiveis
        for i, (parte, cor) in enumerate(visiveis[-12:]):
            self.texto(parte, 34, 362 + i * 20, cor, self.f_pequena)

    def batalha(self, heroi, vilao, cabecalho, aviso, mensagens, botoes, mouse):
        self.cenario()
        self.texto(cabecalho, 20, 14, fonte=self.f_grande, sombra=True)
        self.personagem(heroi, 200)
        self.personagem(vilao, 760, vilao=True)
        self.hud(heroi, 24)
        self.hud(vilao, 616)
        self.texto(aviso[0], LARGURA // 2, 150, aviso[1], self.f_titulo, centro=True, sombra=True)
        self.mensagens(mensagens)
        for botao in botoes:
            self.botao(botao, mouse)

    def escolha(self, herois, mouse):
        self.cenario()
        self.texto("HARRY-POTTER, a batalha filosofal", LARGURA // 2, 24, MARROM, self.f_titulo, True, True)
        self.texto("Escolha seu herói", LARGURA // 2, 68, centro=True, sombra=True)
        for dados, carta in zip(herois, cartas(len(herois))):
            em_cima = carta.collidepoint(mouse)
            self.painel(carta, 215 if em_cima else 185, OURO if em_cima else BORDA)
            self.figura(dados["nome"], carta.centerx, carta.y + 235)
            self.texto(dados["nome"], carta.centerx, carta.y + 250, TEXTO, self.f_grande, True)
            resumo = (f"Vida {dados['vida']}   Ataque {dados['ataque']}   "
                    f"Defesa {dados['defesa']}   Mana {dados['mana']}")
            self.texto(resumo, carta.centerx, carta.y + 284, SUAVE, self.f_pequena, True)
            for i, (nome, habilidade) in enumerate(dados["habilidades"].items()):
                self.texto(f"{nome}  (custo {habilidade['custo']})", carta.centerx,
                           carta.y + 322 + i * 28, ROXO, centro=True)

    def historico(self, eventos):
        camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        camada.fill((0, 0, 0, 170))
        self.tela.blit(camada, (0, 0))
        area = pygame.Rect(100, 50, 760, 540)
        self.painel(area, 235)
        self.texto("Histórico da batalha", area.centerx, 64, OURO, self.f_grande, True)
        for i, evento in enumerate(eventos[-22:]):
            self.texto(sem_emoji(evento), 124, 104 + i * 21, fonte=self.f_pequena)
        self.texto("Clique ou aperte Esc para fechar", area.centerx, area.bottom - 28,
                SUAVE, self.f_pequena, True)