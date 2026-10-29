from batalha import Batalha
from dados import DADOS_HEROIS, DADOS_VILOES, criar_heroi, criar_vilao
from utils import titulo, ler_opcao, exibir_historico

def escolher_heroi():
    titulo("⚔️  ESCOLHA SEU HERÓI")
    for i, d in enumerate(DADOS_HEROIS, start=1):
        print(f"{i}. {d['nome']}  (vida {d['vida']}, ataque {d['ataque']}, "
            f"defesa {d['defesa']}, mana {d['mana']})")
    opcoes = [str(i) for i in range(1, len(DADOS_HEROIS) + 1)]
    escolha = ler_opcao("Número do herói: ", opcoes)
    return criar_heroi(DADOS_HEROIS[int(escolha) - 1])

def main():
    titulo("🏰 IMPROVE THIS GAME 🏰")
    heroi = escolher_heroi()
    print(heroi)

    venceu = True
    for dados in DADOS_VILOES:
        if not Batalha(heroi, criar_vilao(dados)).iniciar():
            venceu = False
            break
        heroi.descansar()

    titulo("🎉 VITÓRIA TOTAL!" if venceu else "FIM DE JOGO")
    if heroi.refens_salvos:
        print("Reféns salvos:", ", ".join(heroi.refens_salvos))
    exibir_historico()

if __name__ == "__main__":
    main()
