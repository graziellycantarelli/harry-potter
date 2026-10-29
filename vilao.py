import random
from personagem import Personagem
from utils import registrar

BONUS_MALDADE = {"Baixa": 1.0, "Média": 1.3, "Alta": 1.6}

class Vilao(Personagem):
    """Vilão: tem nível de maldade, ataque especial, reféns e age sozinho."""

    def __init__(self, nome, idade, vida, maldade, ataque=12, defesa=4,
                ataque_especial=None, refens=None, falas=None):
        super().__init__(nome, idade, vida, ataque, defesa, falas)
        niveis_validos = list(BONUS_MALDADE)
        if maldade not in niveis_validos:
            raise ValueError(f"Nível de maldade inválido! Escolha entre {niveis_validos}")
        self.maldade = maldade
        self.ataque_especial = ataque_especial or {"nome": "Golpe Sombrio", "mult": 1.8}
        self.refens = refens or []

    def atributos(self):
        dados = super().atributos()
        dados["maldade"] = self.maldade
        dados["habilidades"] = [self.ataque_especial["nome"]]
        return dados

    def calcular_dano(self, multiplicador=1.0):
        return super().calcular_dano(multiplicador * BONUS_MALDADE[self.maldade])

    def usar_ataque_especial(self, alvo):
        self.dialogar("ataque", alvo)
        dano, _ = self.calcular_dano(self.ataque_especial["mult"])
        dano_final = alvo.receber_dano(dano)
        msg = (f"{self.nome} usou {self.ataque_especial['nome']} e causou "
            f"{dano_final} de dano em {alvo.nome}!")
        print(f"🔥 {msg}")
        registrar(msg)
        if alvo.esta_vivo:
            alvo.dialogar("dano")

    def agir(self, alvo):
        sorteio = random.random()
        if sorteio < 0.60:
            self.atacar(alvo)
        elif sorteio < 0.85:
            self.usar_ataque_especial(alvo)
        else:
            self.defender()

    def __str__(self):
        return (f"Vilão: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, "
                f"Maldade: {self.maldade}")