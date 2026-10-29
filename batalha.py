import random
from dados import EVENTOS
from utils import (linha, titulo, pausa, ler_opcao, registrar,
                exibir_historico, exibir_ficha)

MENU = ("\nSua vez! Escolha uma ação:\n"
        "1. Atacar   2. Defender   3. Habilidade   4. Poção\n"
        "5. Ver histórico   6. Ver fichas")
CHANCE_EVENTO = 0.20

class Batalha:
    """Controla uma luta entre um herói e um vilão."""

    def __init__(self, heroi, vilao):
        self.heroi = heroi
        self.vilao = vilao
        self.turno = 1

    @property
    def em_andamento(self):
        return self.heroi.esta_vivo and self.vilao.esta_vivo

    def iniciar(self):
        """Roda a batalha até alguém cair. Devolve True se o herói vencer."""
        self.abrir()
        while self.em_andamento:
            self.jogar_turno()
        return self.encerrar()
    
    def abrir(self):
        titulo(f"🔥 {self.heroi.nome}  VS  {self.vilao.nome}")
        print(self.vilao)
        registrar(f"Início da batalha: {self.heroi.nome} vs {self.vilao.nome}")
        self.heroi.dialogar("provocacao", self.vilao)
        self.vilao.dialogar("provocacao", self.heroi)

    def jogar_turno(self):
        linha("-")
        print(f"TURNO {self.turno}")
        self.sortear_evento()
        if not self.em_andamento:
            return
        print(self.heroi.status())
        print(self.vilao.status())
        while not self.turno_heroi():
            pass
        pausa()
        self.turno_vilao()
        self.fim_do_turno()

    def turno_vilao(self):
        if self.vilao.esta_vivo:
            self.vilao.agir(self.heroi)
            pausa()

    def fim_do_turno(self):
        self.heroi.fim_de_turno()
        self.vilao.fim_de_turno()
        self.turno += 1

    def sortear_evento(self):
        if random.random() >= CHANCE_EVENTO:
            return
        evento = random.choice(EVENTOS)
        print(f"\n❗ EVENTO: {evento['texto']}")
        evento["efeito"](self.heroi, self.vilao)
        registrar(f"Evento: {evento['texto']}")
        pausa()

    def turno_heroi(self):
        """Devolve True se o herói gastou o turno com uma ação válida."""
        print(MENU)
        opcao = ler_opcao("> ", ["1", "2", "3", "4", "5", "6"])
        if opcao == "1":
            self.heroi.atacar(self.vilao)
        elif opcao == "2":
            self.heroi.defender()
        elif opcao == "3":
            return self.escolher_habilidade()
        elif opcao == "4":
            return self.heroi.usar_pocao()
        elif opcao == "5":
            exibir_historico()
            return False
        else:
            exibir_ficha(self.heroi)
            exibir_ficha(self.vilao)
            return False
        return True

    def escolher_habilidade(self):
        nomes = list(self.heroi.habilidades)
        for i, nome in enumerate(nomes, start=1):
            print(f"  {i}. {nome} (custo {self.heroi.habilidades[nome]['custo']} mana)")
        escolha = ler_opcao("  Habilidade: ", [str(i) for i in range(1, len(nomes) + 1)])
        return self.heroi.usar_habilidade(self.vilao, nomes[int(escolha) - 1])

    def encerrar(self):
        linha()
        if self.heroi.esta_vivo:
            self.vilao.dialogar("derrota")
            registrar(f"{self.heroi.nome} venceu {self.vilao.nome}!")
            print(f"🏆 {self.heroi.nome} venceu!")
            self.heroi.salvar_refem(self.vilao.refens)
            return True
        self.heroi.dialogar("derrota")
        registrar(f"{self.heroi.nome} foi derrotado por {self.vilao.nome}.")
        print("💀 Você foi derrotado...")
        return False