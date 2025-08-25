from flask import Flask, render_template, request
import random

#Inicializar aplicacion 
app = Flask(__name__)

#conjunto de caracteres para el cifrado
CONJUNTO_CARACTERES = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚáéíóúÜü0123456789 "

#Encontrar el índice de un caracter dentro del conjunto de caracteres
def encontrar_indice(c, conjunto):
    for i in range(len(conjunto)):  #recorrer el conjunto caracter por caracter
        if conjunto[i] == c:        #comparar cada caracter con el objetivo
            return i
    return -1

#Funcion para repetir la clave de Vigenere hasta igualar el tamaño del texto
def repetir_clave(clave, longitud):
    #Se multiplica la clave por el número de veces que cabe en la longitud del texto
    # se utiliza // -> para que solo regrese la parte entera 
    #se agrega los caracteres restantes para igualar la longitud
    # utilizamos slicing [start:stop] para extraer una parte de la clave
    return (clave * (longitud // len(clave)) + clave[:longitud % len(clave)])

#Funcion para cifrar (Vigenère)
def cifrar_vigenere(texto, clave):
    clave_repetida = repetir_clave(clave, len(texto)) #repite la clave si es necesario
    texto_cifrado = ""
    for i in range(len(texto)): #itera en cada caracter del texto 
        caracter= texto[i] #caracter actual 
        if caracter in CONJUNTO_CARACTERES: #verifica si el caracter esta en nuestro conjunto
            #Encuentra el indice del caracter del texto
            indice_caracter = encontrar_indice(caracter, CONJUNTO_CARACTERES)
            #se ncuentra el indice del caracter del caracter de la clave repetida
            indice_clave = encontrar_indice(clave_repetida[i], CONJUNTO_CARACTERES)
            #calculamos  el nuevo índice aplicando la suma modular.
            nuevo_indice = (indice_caracter + indice_clave) % len(CONJUNTO_CARACTERES)
            #se añade eel caracter cifrado a nuestra cadena del texto cifrado 
            texto_cifrado += CONJUNTO_CARACTERES[nuevo_indice]
        else:
            #si no tenemos el caracter lo agregamos como se ingresa 
            texto_cifrado += caracter
    return texto_cifrado

#Cifrar texto usando XOR
def cifrar_xor(texto):
    #Generamos una clave aleatoria con valores entre 0 y 255, uno por cada carácter del texto.
    clave_xor = [random.randint(0, 255) for _ in range(len(texto))] 
    texto_cifrado = []
    for i in range(len(texto)): # se itera en cada caracter 
        #Aplicamos el XOR entre el caracter y el valor correspondiente de la clave.
        byte = ord(texto[i]) ^ clave_xor[i]  #ord convierte el valor del caracter en numero
        texto_cifrado.append(chr(byte)) #se convierte el resultado del XOR de nuevo a un carácter
    #se concatenar todos los caracteres sin separacion("")
    return "".join(texto_cifrado), clave_xor 

#Descifrar texto usando XOR
def descifrar_xor(texto_cifrado, clave_xor):
    texto_descifrado = ""
    for i in range(len(texto_cifrado)):
        byte = ord(texto_cifrado[i]) ^ clave_xor[i] #Aplicamos nuevamente la operacion XOR con la clave para recuperar el valor original
        texto_descifrado += chr(byte) #Convertimos el valor XOR de nuevo a un caracter
    return texto_descifrado

#Funcion para descifrar (Vigenère)
def descifrar_vigenere(texto, clave):
    clave_repetida = repetir_clave(clave, len(texto)) #Repite la clave para igualar al tamaño del texto
    texto_descifrado = ""
    for i in range(len(texto)):
        caracter = texto[i] #obtiene el caracter actual 
        if caracter in CONJUNTO_CARACTERES: #se comprueba si el caracter esta en nuestro conjunto
            #encontramos el indice del caracter segun el conjunto
            indice_caracter = encontrar_indice(caracter, CONJUNTO_CARACTERES)
            #encontramos el indice del caracter de la clave segun el conjunto 
            indice_clave = encontrar_indice(clave_repetida[i], CONJUNTO_CARACTERES)
            #se obtiene el valor original restando modularmente
            nuevo_indice = (indice_caracter - indice_clave + len(CONJUNTO_CARACTERES)) % len(CONJUNTO_CARACTERES)
            texto_descifrado += CONJUNTO_CARACTERES[nuevo_indice]
        else:
            texto_descifrado += caracter #si no se encuentra el caracter en el conjunto no se realizan modificaciones 
    return texto_descifrado 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto_claro = request.form["texto_claro"]
        clave_vigenere = request.form["clave_vigenere"]

        # Cifrado Vigenère
        texto_cifrado_vigenere = cifrar_vigenere(texto_claro, clave_vigenere)
        # Cifrado XOR
        texto_cifrado_xor, clave_xor = cifrar_xor(texto_cifrado_vigenere)
        # Descifrado XOR
        texto_descifrado_xor = descifrar_xor(texto_cifrado_xor, clave_xor)
        # Descifrado Vigenère
        texto_descifrado = descifrar_vigenere(texto_descifrado_xor, clave_vigenere)
        #Actualiza los resultados que se obtienen
        return render_template( #Es una función de flask que renderiza una plantilla HTML
            "index.html",
            texto_claro=texto_claro,
            texto_cifrado_vigenere=texto_cifrado_vigenere,
            texto_cifrado_xor=texto_cifrado_xor,
            texto_descifrado=texto_descifrado
        )
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
