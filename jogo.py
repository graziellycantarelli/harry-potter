import sys
from dataclasses import dataclass
from typing import Callable

import pygame

import utils
from batalha import Batalha
from dados import DADOS_HEROIS, DADOS_VILOES, criar_heroi, criar_vilao
from desenho import (ALTURA, AZUL_ESCURO, BORDA, LARANJA, LARGURA, MARROM, OURO, TEXTO,
                    VERDE, VERMELHO, VERMELHO_BOTAO, Desenho, cartas, sem_emoji)
utils.PAUSA_ATIVA = False
FPS = 60
ATRASO_VILAO = 900

@dataclass
class Botao:
    rect: pygame.Rect
    rotulo: str
    acao: Callable
    cor: tuple
    ativo: bool = True

class SaidaParaLog:
    def __init__(self, jogo):
        self.jogo = jogo
        self.pendente = ""

    def write(self, conteudo):
        self.pendente += conteudo
        while "\n" in self.pendente:
            linha, self.pendente = self.pendente.split("\n", 1)
            self.jogo.adicionar_mensagem(linha)
        return len(conteudo)

    def flush(self):
        pass

class Jogo:
    def __init__(self, desenho):
        self.desenho = desenho
        self.sair = False
        self.reiniciar()

    def reiniciar(self):
        self.estado = "escolha"
        self.mostrar_historico = False
        self.heroi = self.vilao = self.batalha = None
        self.fase = 0
        self.venceu = False
        self.espera = 0
        self.mensagens = []
        utils.HISTORICO.clear()

    def adicionar_mensagem(self, linha):
        texto = sem_emoji(linha)
        if texto and not set(texto) <= set("=-"):
            self.mensagens.append((texto, OURO if "💬" in linha else TEXTO))

    def iniciar(self, dados_heroi):
        self.heroi = criar_heroi(dados_heroi)
        self.fase = 0
        self.mensagens = []
        self.proxima_batalha()

    def proxima_batalha(self):
        self.vilao = criar_vilao(DADOS_VILOES[self.fase])
        self.batalha = Batalha(self.heroi, self.vilao)
        self.batalha.abrir()
        self.estado = "jogador"
        self.novo_turno()

    def novo_turno(self):
        self.batalha.sortear_evento()
        self.verificar_fim()

    def verificar_fim(self):
        if self.batalha.em_andamento:
            return False
        self.venceu = self.batalha.encerrar()
        ultima = self.fase + 1 >= len(DADOS_VILOES)
        self.estado = "pos_batalha" if self.venceu and not ultima else "fim"
        return True

    def descansar(self):
        self.heroi.descansar()
        print("🧪 Você descansa: +20 de vida e mana cheia.")
        self.fase += 1
        self.proxima_batalha()

    def agir(self, acao):
        if self.estado != "jogador" or acao() is False:
            return
        if not self.verificar_fim():
            self.estado = "vilao"
            self.espera = pygame.time.get_ticks() + ATRASO_VILAO

    def atualizar(self):
        if self.estado != "vilao" or pygame.time.get_ticks() < self.espera:
            return
        self.batalha.turno_vilao()
        if not self.verificar_fim():
            self.batalha.fim_do_turno()
            self.estado = "jogador"
            self.novo_turno()

    def botoes(self):
        if self.estado in ("jogador", "vilao"):
            return self.botoes_de_acao()
        if self.estado == "pos_batalha":
            return [Botao(pygame.Rect(620, 362, 320, 56), "Próxima batalha  >>", self.descansar, VERDE)]
        if self.estado == "fim":
            return [Botao(pygame.Rect(620, 362, 320, 56), "Jogar de novo", self.reiniciar, VERDE),
                    Botao(pygame.Rect(620, 430, 320, 56), "Sair", self.fechar, VERMELHO)]
        return []

    def botoes_de_acao(self):
        heroi, vez = self.heroi, self.estado == "jogador"
        botoes = [Botao(pygame.Rect(620, 362, 156, 44), "Atacar",
                        lambda: self.agir(lambda: heroi.atacar(self.vilao)), VERMELHO_BOTAO, vez),
                Botao(pygame.Rect(784, 362, 156, 44), "Defender",
                        lambda: self.agir(heroi.defender), MARROM, vez)]
        for i, (nome, habilidade) in enumerate(list(heroi.habilidades.items())[:2]):
            botoes.append(Botao(pygame.Rect(620, 414 + 52 * i, 320, 44),
                                f"{nome}  ({habilidade['custo']} mana)",
                                lambda n=nome: self.agir(lambda: heroi.usar_habilidade(self.vilao, n)),
                                AZUL_ESCURO, vez and heroi.mana >= habilidade["custo"]))
        pocoes = heroi.itens.count("Poção de Cura")
        botoes.append(Botao(pygame.Rect(620, 518, 320, 44), f"Poção de Cura  (x{pocoes})",
                            lambda: self.agir(heroi.usar_pocao), AZUL_ESCURO, vez and pocoes > 0))
        botoes.append(Botao(pygame.Rect(810, 10, 130, 34), "Histórico (H)", self.alternar_historico, BORDA))
        return botoes

    def alternar_historico(self):
        self.mostrar_historico = not self.mostrar_historico

    def fechar(self):
        self.sair = True

    def tratar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.sair = True
        elif evento.type == pygame.KEYDOWN:
            self.tratar_tecla(evento.key)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.tratar_clique(evento.pos)

    def tratar_tecla(self, tecla):
        if tecla == pygame.K_ESCAPE:
            if self.mostrar_historico:
                self.mostrar_historico = False
            else:
                self.sair = True
        elif tecla == pygame.K_h and self.estado != "escolha":
            self.alternar_historico()

    def tratar_clique(self, posicao):
        if self.mostrar_historico:
            self.mostrar_historico = False
        elif self.estado == "escolha":
            for dados, carta in zip(DADOS_HEROIS, cartas(len(DADOS_HEROIS))):
                if carta.collidepoint(posicao):
                    self.iniciar(dados)
        else:
            for botao in self.botoes():
                if botao.ativo and botao.rect.collidepoint(posicao):
                    botao.acao()
                    break

    def aviso(self):
        if self.estado == "jogador":
            return "Sua vez!", OURO
        if self.estado == "vilao":
            return f"Vez de {self.vilao.nome}...", LARANJA
        if self.estado == "pos_batalha":
            return "VITÓRIA! Hora de descansar.", VERDE
        return ("VITÓRIA TOTAL!", OURO) if self.venceu else ("FIM DE JOGO", VERMELHO)

    def desenhar(self):
        mouse = pygame.mouse.get_pos()
        if self.estado == "escolha":
            self.desenho.escolha(DADOS_HEROIS, mouse)
            return
        cabecalho = f"Batalha {self.fase + 1}/{len(DADOS_VILOES)}  -  Turno {self.batalha.turno}"
        self.desenho.batalha(self.heroi, self.vilao, cabecalho, self.aviso(),
                            self.mensagens, self.botoes(), mouse)
        if self.mostrar_historico:
            self.desenho.historico(utils.HISTORICO)

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Improve This Game")
    jogo = Jogo(Desenho(tela))
    relogio = pygame.time.Clock()
    saida = sys.stdout
    sys.stdout = SaidaParaLog(jogo)
    while not jogo.sair:
        for evento in pygame.event.get():
            jogo.tratar_evento(evento)
        jogo.atualizar()
        jogo.desenhar()
        pygame.display.flip()
        relogio.tick(FPS)
    sys.stdout = saida
    pygame.quit()

if __name__ == "__main__":
    main()
