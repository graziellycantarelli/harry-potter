import sys
import time

# Evita UnicodeEncodeError com emojis no terminal do Windows.
for _saida in (sys.stdout, sys.stderr):
    if hasattr(_saida, "reconfigure"):
        _saida.reconfigure(encoding="utf-8")

LARGURA = 54
HISTORICO = []
PAUSA_ATIVA = True

def registrar(evento):
    HISTORICO.append(evento)

def linha(char="=", tamanho=LARGURA):
    print(char * tamanho)

def titulo(texto):
    linha()
    print(texto.center(LARGURA))
    linha()

def barra_vida(vida, vida_max, tamanho=20):
    cheio = int(tamanho * max(vida, 0) / vida_max)
    return f"[{'█' * cheio}{'░' * (tamanho - cheio)}] {max(vida, 0)}/{vida_max}"

def pausa(segundos=0.7):
    if PAUSA_ATIVA:
        time.sleep(segundos)

def ler_opcao(texto, validas):
    while True:
        escolha = input(texto).strip()
        if escolha in validas:
            return escolha
        print("⚠️  Opção inválida, tente novamente.")

def exibir_historico():
    titulo("📜 HISTÓRICO DA BATALHA")
    for i, evento in enumerate(HISTORICO, start=1):
        print(f"{i:02d}. {evento}")
    linha()

def exibir_ficha(personagem):
    print(f"\n📋 FICHA DE {personagem.nome.upper()}")
    linha("-", 30)
    for chave, valor in personagem.atributos().items():
        if isinstance(valor, list):
            valor = ", ".join(valor) if valor else "nenhum"
        print(f"{chave.capitalize():<13}: {valor}")
    linha("-", 30)
