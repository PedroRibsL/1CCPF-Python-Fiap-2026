palavras =  {"frutas": ["banana", "morango", "abacaxi", "melancia"],
             "cores": ["azul", "vermelho", "verde", "amarelo"]}

resposta = input("Escolha uma categoria \n"
                 "1 - Frutas, 2 - Cores: ")

if resposta == "1":
    categoria = palavras["frutas"]
elif resposta == "2":
    categoria = palavras["cores"]
else:
    print("Erro, Opção invalida!")

print("A categoria escolhida foi : ", resposta)
print("A categoria possui", len(categoria), "palavras.")

posicao = int(input("Escolha a posição da palavra: "))

palavra = categoria[posicao - 1]

print("Palavra:", "_" * len(palavra))

tentativas = 6
letras_descobertas = ["_"] * len(palavra)

print("Você terá 6 tentativas para descobrir a palavra.")

while tentativas > 0:
    print("\nPalavra:", " ".join(letras_descobertas))
    print("Tentativas restantes:", tentativas)

    letra = input("Digite uma letra: ")

    if letra in palavra:
        print("A letra está presente na palavra!")

        for i in range(len(palavra)):
            if palavra[i] == letra:
                letras_descobertas[i] = letra
    else:
        print("Você errou!")
        tentativas -= 1

    if "_" not in letras_descobertas:
        print("\nParabéns! Você descobriu a palavra!")
        break

if "_" in letras_descobertas:
    print("\nVocê perdeu!")
    print("A palavra era:", palavra)