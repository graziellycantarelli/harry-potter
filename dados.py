from heroi import Heroi
from vilao import Vilao

DADOS_HEROIS = [
    {"nome": "Harry Potter", "idade": 17, "vida": 110, "ataque": 18, "defesa": 6, "mana": 50,
    "habilidades": {"Expelliarmus": {"custo": 12, "mult": 1.8},
                    "Patronus": {"custo": 30, "mult": 3.0}},
    "falas": {"provocacao": ["Já enfrentei coisa pior que você!",
                            "Solte os reféns ou vai ter que lidar comigo!"],
            "ataque": ["Varinha em punho!", "Toma essa!", "Pelo castelo!"],
            "dano": ["Isso queimou... mas não me para!", "Já levei tombos piores no Quadribol!"],
            "defesa": ["Protego!", "Escudo erguido!"],
            "derrota": ["Desculpem... eu não consegui..."]}},
    {"nome": "Hermione Granger", "idade": 17, "vida": 90, "ataque": 20, "defesa": 4, "mana": 70,
    "habilidades": {"Petrificus Totalus": {"custo": 15, "mult": 2.0},
                    "Fogo Mágico Azul": {"custo": 28, "mult": 2.8}},
    "falas": {"provocacao": ["Li sobre gente como você, e nunca termina bem pra vocês.",
                            "Última chance: liberte os reféns!"],
            "ataque": ["Estudei esse feitiço a noite toda!", "Precisão acima de tudo!",
                        "Tome isto!"],
            "dano": ["Auch! Isso não estava no livro!", "Ainda estou de pé!"],
            "defesa": ["Protego!", "Eu previ esse golpe!"],
            "derrota": ["Eu devia ter estudado mais..."]}},
]

DADOS_VILOES = [
    {"nome": "Draco Malfoy", "idade": 17, "vida": 60, "maldade": "Baixa", "ataque": 12, "defesa": 3,
    "ataque_especial": {"nome": "Serpensortia", "mult": 1.8},
    "refens": ["Neville Longbottom"],
    "falas": {"provocacao": ["Você não devia estar aqui!",
                            "Vai se arrepender de ter me desafiado!"],
            "ataque": ["Tome isto!", "Vai chorar pra quem?"],
            "dano": ["Ai! Meu cabelo!", "Isso foi golpe baixo!"],
            "defesa": ["Não me acerta!"],
            "derrota": ["Eu... eu volto mais forte!"]}},
    {"nome": "Bellatrix Lestrange", "idade": 45, "vida": 90, "maldade": "Média", "ataque": 14, "defesa": 5,
    "ataque_especial": {"nome": "Crucio", "mult": 2.0},
    "refens": ["Luna Lovegood", "Sr. Olivaras"],
    "falas": {"provocacao": ["Que gracinha, mais um herói para brincar!",
                            "Vamos ver quanto você aguenta..."],
            "ataque": ["Dance pra mim!", "Hahaha, sinta isso!"],
            "dano": ["Ora, você morde!", "Uma arranhadinha, só isso..."],
            "defesa": ["Feitiços fracos não me tocam!"],
            "derrota": ["Meu mestre... vai me vingar..."]}},
    {"nome": "Voldemort", "idade": 70, "vida": 130, "maldade": "Alta", "ataque": 16, "defesa": 6,
    "ataque_especial": {"nome": "Avada Kedavra", "mult": 2.2},
    "refens": ["Gina Weasley", "Rony Weasley"],
    "falas": {"provocacao": ["Todos os que resistem acabam esquecidos.",
                            "Sua coragem é só ilusão."],
            "ataque": ["Sinta o poder das trevas!", "Nem sua varinha vai te salvar!"],
            "dano": ["Impossível... um mero aluno?", "Você vai pagar por isso!"],
            "defesa": ["Seus feitiços não passam de faíscas!"],
            "derrota": ["Não... é... possível..."]}},
]

def evento_pocao(heroi, vilao):
    heroi.itens.append("Poção de Cura")

def evento_terremoto(heroi, vilao):
    heroi.downgrade_vida(6, mostrar=False)
    vilao.downgrade_vida(6, mostrar=False)

def evento_bencao(heroi, vilao):
    heroi.mana = min(heroi.mana_max, heroi.mana + 15)

EVENTOS = [
    {"texto": "🧪 Você encontra uma Poção de Cura esquecida num armário de Hogwarts!", "efeito": evento_pocao},
    {"texto": "🌋 O castelo treme! Ambos perdem 6 de vida.", "efeito": evento_terremoto},
    {"texto": "🌟 Uma pena de fênix brilha e restaura 15 de mana!", "efeito": evento_bencao},
]

def criar_heroi(d):
    return Heroi(d["nome"], d["idade"], d["vida"], d["ataque"], d["defesa"],
                d["mana"], d["habilidades"], d["falas"])

def criar_vilao(d):
    return Vilao(d["nome"], d["idade"], d["vida"], d["maldade"], d["ataque"],
                d["defesa"], d["ataque_especial"], list(d["refens"]), d["falas"])