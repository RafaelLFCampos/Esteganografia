import cv2
import numpy as np

while(1):
    entrada = (input("Selecione uma das opções:\n\
    1 - Escrever em uma imagem\n\
    2 - Ler uma esteganografia\n\
    0 - Sair\n"))
    
    if entrada == '0':
        print("\nEncerrando... Bye")
        break
    
    if entrada != '1' and entrada != '2':
        print("Digite um número válido!")
        
    else:
        nomeImg = (input("Digite o nome e a extensão da imagem: "))
        nome = nomeImg.split(".")
        
        if nome[1] == 'ppm':
            imagem = cv2.imread(nomeImg)
            ext = 0
        elif nome[1] == 'pgm':
            imagem = cv2.imread(nomeImg,0)
            ext = 1
        else:
            print("Extensão não encontrada")
            break
        
        if imagem is None:
            print("Digite uma imagem válida!\n")

        else:

            #caso opção seja escrever mensagem
            if entrada == '1':
                masc = 1
                
                palavra = (input("Digite a palavra: "))
                string = ''

                #laço utilizado para converter o caracter da palavra em número
                for x in palavra:
                    masc = 1
                    masc = masc  << 7
                    palavraBin = ord(x)
                    i = 7

                    #laço usado para transformar o número em uma string binária
                    while i > -1:
                        result = masc & palavraBin
                        if result != 0:
                            string = string + str(1)
                        else:
                            string = string + str(0)
                        masc = masc >> 1        
                        i = i - 1
               
                i = 0
                tam = len(string)
                print(string, tam, "\n")
                masc = 1
                #flag utilizada para indicar o final da string binária
                flag = 0

                #laços usados na escrita nos pixels da imagem
                for y in range(imagem.shape[0]):
                    for x in range(imagem.shape[1]):
                        k = 0
                        #laço para imagem com 3 canais de cor
                        while k < 3:

                            #verifica se já foram escritos todos os valores binários na imagem
                            if i < tam:
                                #caso extensão seja PGM
                                if ext == 1:
                                    r = masc & imagem.item(y, x)
                                    
                                #caso extensão seja PPM
                                else:
                                    r = masc & imagem.item(y, x, k)

                                #caso o último bit comparado seja 0
                                if r == 0:
                                    #caso deva ser escrito o valor 1
                                    if string[i] == '1':
                                        #fará a escrita
                                        if ext == 1:
                                            imagem[y,x] = imagem[y,x] + 1
                                            k = 3
                                            i += 1

                                        else:
                                            imagem[y,x,k] = imagem[y,x,k] + 1    
                                            i += 1
                                            k += 1

                                    #caso valor do último bit seja o mesmo do valor que deve ser escrito  
                                    else:
                                        #não fará a escrita
                                        if ext == 1:
                                            k = 3
                                        else:
                                            
                                            k += 1
                                        i += 1

                                #caso o bit seja 1        
                                else:
                                    #caso deva ser escrito o valor 0
                                    if string[i] == '0':
                                        #fará a escrita
                                        if ext == 1:
                                            imagem[y,x] = imagem[y,x] + 1
                                            k = 3
                                            i += 1
                                        else:
                                            imagem[y,x,k] = imagem[y,x,k] + 1
                                            i += 1
                                            k += 1

                                    #caso valor do último bit seja o mesmo do valor que deve ser escrito
                                    else:
                                        #não fará a escrita
                                        if ext == 1:
                                            k = 3
                                        else:
                                            k += 1
                                        i += 1

                            #caso já tenha escrito todos os caracteres binários da mensagem            
                            else:
                                #flag que indica a escrita de toda a string binária
                                flag = 1
                                #quebra o laço
                                break
                        if flag == 1:
                            break
                    if flag == 1:
                        break

                #se a extensão da imagem for PPM
                if ext == 0:
                    #grava imagem como ppm
                    cv2.imwrite("imagemPpmOut.ppm", imagem)
                    print("Imagem com mensagem oculta gravada com sucesso!\n")

                #se for PGM 
                else:
                    #grava imagem como pgm
                    cv2.imwrite("imagemPgmOut.pgm", imagem)
                    print("Imagem com mensagem oculta gravada com sucesso!\n")
                

            #caso opção seja de leitura da mensagem    
            elif entrada == '2':
                cv2.imshow("Imagem", imagem)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                masc = 1
                i = 0
                x = 0
                y = 0
                flag = 0
                #variável auxiliar
                string = ''
                #variável que armazenará a mensagem final
                stringFinal = ''
                for y in range(imagem.shape[0]):
                    for x in range(imagem.shape[1]):
                        k = 0
                        #laço para percorrer os três canais
                        while k < 3:
                            #verificação se já foram realizadas 8 iterações
                            #indicando que já possui um byte para ser convertido em caractere
                            if i == 8:
                                i = 0
                                #converte de binário para inteiro
                                stringComp = int(string, 2)
                                #reseta a variável auxiliar que armazena o caracter em binário
                                string = ''

                                #verifica se é o caractere que indica o final da string ou barra invertida '\'
                                if stringComp == 00 or stringComp == 47:
                                    #caso seja, ativa a flag que encontrou o final e para o laço while
                                    flag = 1
                                    break

                                #se não for o final da string
                                else:
                                    #armazena os caracteres da mensagem na variável
                                    stringFinal = stringFinal + chr(stringComp)

                            #caso seja pgm
                            if ext == 1:
                                r = masc & imagem.item(y, x)
                                k = 3
                                
                            #caso seja ppm    
                            else:
                                r = masc & imagem.item(y, x, k)

                            #caso último bit seja 0
                            if r == 0:
                                #armazena o caracter 0 na variável auxiliar
                                if ext == 1:
                                    string = string + '0'
                                    i += 1
                                if ext == 0:
                                    string = string + '0'
                                    k += 1
                                    i += 1

                            #caso último bit seja 1
                            else:
                                #armazena o caracter 1 na variável auxiliar
                                if ext == 1:
                                    string = string + '1'
                                    i += 1
                                if ext == 0:
                                    string = string + '1'
                                    k += 1
                                    i += 1             
                        #flags usadas para quebrar os laços for indicando
                        #o final da leitura da mensagem
                        if flag == 1:
                            break
                    if flag == 1:
                            break

                #exibe a mensagem que estava oculta
                print(stringFinal, "\n")


            #caso usuário tenha digitado uma opção inválida no menu
            else:
                print("Digite uma opção válida")
