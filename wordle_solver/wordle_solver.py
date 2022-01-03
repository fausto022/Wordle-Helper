def cumple_requisitos(palabra, verdes, amarillas, descartadas) -> bool:
    """Se fija si determinada palabra cumple con las letras verdes,
    faltan descartadas y amarillas. (todo)"""    

    # Comparamos las verdes
    for k, v in verdes.items():
        if v != '' and palabra[k] != v:
            return False   
    
    # Tiene que contener las amarillas pero no en el lugar que van
    for k, v in amarillas.items():
        for letra in v:
            if not(letra in palabra and palabra[k] != letra):
                return False
    
    # Falso si contiene una letra descartada        
    for letra in descartadas:
        if letra in palabra and letra not in verdes.values():
            return False

    return True       
 

def filtrar_palabras(lista: list[str], verdes: dict[int, chr], amarillas: dict[int, list], descartadas: list[chr]) -> list[str]:
    """Filtra las palabras según cumplan con los requisitos"""
    print("Filtrando palabras . . .")
    lista = [palabra for palabra in lista if cumple_requisitos(palabra, verdes, amarillas, descartadas)]
    print("Palabras han sido filtradas . . .")
    return lista

def elegir_palabra(lista: list[str], verdes: dict[int, chr], restantes: list[chr]) -> str:
    """Dada una lista de palabras posibles, devuelve la palabra mas óptima.
    Óptima siendo aquella palabra que descarta la mayor cantidad de palabras en la lista, fijándose que contenga las letras
    que mas aparecen en la mayor cantidad de palabras en la lista."""
    print("Eligiendo palabra . . .")
    palabras_con_letra = dict.fromkeys(restantes, set()) #{i: ("incas", "arids")}
    print("Recorriendo palabras de la lista . . .")
    for palabra in lista:        
        for i, letra in enumerate(palabra):
            if letra != verdes[i]:
                palabras_con_letra[letra] = palabras_con_letra[letra] | {palabra}

    print("Viendo cuantas palabras descarta cada palabra . . .")
    cuales_descarta_palabra = dict.fromkeys(lista, set())
    for palabra in lista:        
        for letra in palabra:
            cuales_descarta_palabra[palabra] = cuales_descarta_palabra[palabra] | palabras_con_letra[letra]
    
    print(f"cuantas palabras quedan: {len(lista)}")
    if len(lista) < 20:
        print(lista)

    max = lista[0]
    for palabra in lista:
        if len(cuales_descarta_palabra[palabra]) > len(cuales_descarta_palabra[max]):
            max = palabra
    return max



def main():
    with open("words_5.txt", "r") as f:
        lista_palabras_1 = f.read().split("\n") # todas las palabras de 5 letras del idioma inglés
    
    with open("words_5_2.txt", "r") as f:
        lista_palabras_2 = f.read().split(' ')

    alfabeto = list(string.ascii_lowercase) # las 26 letras del alfabeto inglés, en una lista.   


    verdes = dict_de_verdes_usuario("Letras en verde (en formato 'a _ b c _) -> ")
    print(f"verdes: {verdes}")

    amarillas = {0:[], 1:[], 2:[], 3:[], 4:[]}           
    for k in amarillas:
        amarillas[k] = lista_de_chars_usuario(f"¿Cuáles tenés amarillas en {k+1}?: ")
    print(f"amarillas: {amarillas}")    

    # pedirle al usuario las letras que ya descartó (grises)
    descartadas = lista_de_chars_usuario("Letras descartadas (en formato 'abc') -> ") 
    print(f"descartadas: {descartadas}")
    descartadas = [letra for letra in descartadas if letra not in verdes.values()]

    # nos quedamos solo con las letras que no descartamos
    restantes = [letra for letra in alfabeto if letra not in descartadas] 
    

    lista_final = (filtrar_palabras(lista_palabras_2, verdes, amarillas, descartadas))
    resultado = elegir_palabra(lista_final, verdes, restantes)
    print(f"La mejor palabra es: {resultado}")  