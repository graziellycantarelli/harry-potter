import random
from utils import registrar, barra_vida, pausa

FALAS_PADRAO = {
    "provocacao": ["Prepare-se!"],
    "ataque": ["Toma essa!"],
    "dano": ["Argh!"],
    "defesa": ["Não vai passar!"],
    "derrota": ["Eu... perdi..."],
}

class Personagem:
    """Personagem genérico: base para Heroi e Vilao."""

    def __init__(self, nome, idade, vida, ataque=10, defesa=3, falas=None):
        self.nome = nome
        self.idade = idade
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.defendendo = False
        self.itens = []
        self.habilidades = {}
        self.falas = falas or FALAS_PADRAO

    @property
    def esta_vivo(self):
        return self.vida > 0

    def atributos(self):
        return {"nome": self.nome, "idade": self.idade, "vida": self.vida,
                "ataque": self.ataque, "defesa": self.defesa,
                "itens": list(self.itens), "habilidades": list(self.habilidades)}

    def status(self):
        return f"{self.nome:<20} {barra_vida(self.vida, self.vida_max)}"

    def upgrade_vida(self, incremento=10):
        self.vida += incremento
        self.vida_max += incremento
        print(f"Vida de {self.nome} após upgrade: {self.vida}")
        registrar(f"{self.nome} recebeu upgrade de vida (+{incremento}).")

    def downgrade_vida(self, dano=15, mostrar=True):
        self.vida = max(0, self.vida - dano)
        if mostrar:
            print(f"Vida de {self.nome} após downgrade: {self.vida}")

    def update_nome(self, nome_editado):
        self.nome = nome_editado

    def curar(self, valor):
        antes = self.vida
        self.vida = min(self.vida_max, self.vida + valor)
        return self.vida - antes

    def dialogar(self, tipo="ataque", alvo=None):
        frase = random.choice(self.falas.get(tipo, ["..."]))
        destino = f" (para {alvo.nome})" if alvo else ""
        print(f'   💬 {self.nome}{destino}: "{frase}"')
        pausa(0.4)

    def calcular_dano(self, multiplicador=1.0):
        dano = (self.ataque + random.randint(-3, 3)) * multiplicador
        critico = random.random() < 0.15
        return int(dano * 2 if critico else dano), critico

    def receber_dano(self, dano):
        reducao = self.defesa * (2 if self.defendendo else 1)
        dano_final = max(1, dano - reducao)
        self.downgrade_vida(dano_final, mostrar=False)
        return dano_final

    def atacar(self, alvo):
        self.dialogar("ataque", alvo)
        dano, critico = self.calcular_dano()
        dano_final = alvo.receber_dano(dano)
        extra = " 💥 CRÍTICO!" if critico else ""
        msg = f"{self.nome} atacou {alvo.nome} e causou {dano_final} de dano.{extra}"
        print(f"⚔️  {msg}")
        registrar(msg)
        if alvo.esta_vivo:
            alvo.dialogar("dano")

    def defender(self):
        self.defendendo = True
        self.dialogar("defesa")
        msg = f"{self.nome} assumiu postura de defesa."
        print(f"🛡️  {msg}")
        registrar(msg)

    def fim_de_turno(self):
        self.defendendo = False

    def __str__(self):
        return f"Personagem: {self.nome}, Idade: {self.idade}, Vida: {self.vida}"