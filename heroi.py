import random
from personagem import Personagem
from utils import registrar

class Heroi(Personagem):
    """Herói: tem mana, habilidades, poções e salva reféns."""

    def __init__(self, nome, idade, vida, ataque, defesa, mana, habilidades, falas=None):
        super().__init__(nome, idade, vida, ataque, defesa, falas)
        self.mana = mana
        self.mana_max = mana
        self.habilidades = habilidades
        self.itens = ["Poção de Cura"] * 2
        self.refens_salvos = []

    def atributos(self):
        dados = super().atributos()
        dados["mana"] = f"{self.mana}/{self.mana_max}"
        return dados

    def status(self):
        return super().status() + f"  🔷 Mana {self.mana}/{self.mana_max}"

    def usar_habilidade(self, alvo, nome_habilidade):
        habilidade = self.habilidades[nome_habilidade]
        if self.mana < habilidade["custo"]:
            print("⚠️  Mana insuficiente!")
            return False
        self.mana -= habilidade["custo"]
        self.dialogar("ataque", alvo)
        dano, critico = self.calcular_dano(habilidade["mult"])
        dano_final = alvo.receber_dano(dano)
        extra = " 💥 CRÍTICO!" if critico else ""
        msg = f"{self.nome} usou {nome_habilidade} em {alvo.nome}: {dano_final} de dano.{extra}"
        print(f"✨ {msg}")
        registrar(msg)
        if alvo.esta_vivo:
            alvo.dialogar("dano")
        return True

    def usar_pocao(self):
        if "Poção de Cura" not in self.itens:
            print("⚠️  Você não tem poções!")
            return False
        self.itens.remove("Poção de Cura")
        curado = self.curar(random.randint(25, 40))
        msg = f"{self.nome} bebeu uma poção e recuperou {curado} de vida."
        print(f"🧪 {msg} (restam {self.itens.count('Poção de Cura')})")
        registrar(msg)
        return True

    def salvar_refem(self, refens):
        if not refens:
            print(f"   {self.nome} não encontrou ninguém para salvar.")
            return
        while refens:
            refem = refens.pop(0)
            self.refens_salvos.append(refem)
            msg = f"{self.nome} salvou o refém {refem}!"
            print(f"🙏 {msg}")
            registrar(msg)

    def descansar(self):
        self.curar(20)
        self.mana = self.mana_max

    def __str__(self):
        return (f"Herói: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, "
                f"Mana: {self.mana}")
