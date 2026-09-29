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

print(f"A categoria escolhida foi a : {resposta}, possui: {len(categoria)} palavras")

posicao = int(input("Escolha a posição da palavra (1 - 4): "))

indice = posicao - 1

palavra = (categoria[indice])

palavra_escondida = list("_" * len(palavra))

tentativas = 6

print("Você terá 6 tentativas para descobrir a palavra.")

while "_" in palavra_escondida and tentativas > 0:
    
    palavra_atual = "".join(palavra_escondida)
    print(f"Palavra: {palavra_atual}")
    
    print(f" Você possui {tentativas} tentativas restantes.")
    
    letra = input("Digite uma letra: ")
    
    if letra in palavra:
        for i in range(len(palavra)):
            if palavra[i] == letra:
                palavra_escondida[i] = letra
    else:
        tentativas -= 1
        print(f"Você errou! Tentativas restantes: {tentativas}")
    
if "_" not in palavra_escondida:
    print(f"Parabéns! Você descobriu a palavra: {palavra}")
else:
    print(f"Você usou todas as tentativas! A palavra era: {palavra}")
