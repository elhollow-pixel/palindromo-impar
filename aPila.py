import pyttsx3 ##Implementar voces al momento de que ocurra un error, o no se acepte la palabra.
import time

class automataPila():
    def __init__(self, eInicial, eFinal, lSimbolos, lTransicion, mTransicion, pVacia):
        self.eInicial = eInicial
        self.eFinal = eFinal
        self.lSimbolos = lSimbolos
        self.lTransicion = lTransicion
        self.mTransicion = mTransicion
        self.pila = pVacia

    def _comprobarPalabra(self, palabra, windows):
        self.windows = windows #Variable que contiene la referencia de la ventana

        # Configuracion inicial
        estadoActual = self.eInicial
        pilaActual = self.pila.copy()
        palabra_leida = ''
        booleanError = False

        self.windows._drawNodo('inicio')
        print('[(%s, %s, %s)] Configuración inicial' %(estadoActual, palabra, pilaActual))
        self.windows._añadirInfoArbol('[(%s, %s, %s)] Configuración inicial' %(estadoActual, palabra, pilaActual))
        self.windows._añadirInfoPila(pilaActual[0]) #Añadimos el caracter con el que empieza la pila
        self.windows._drawNodo(estadoActual)

        #time.sleep(1)
        # Proceso de aceptacion
        #self.windows._drawNodo(estadoActual)

        for i in range(len(palabra)):
            try:
                palabra_leida = palabra_leida + palabra[i]
                cabezaPila = pilaActual[len(pilaActual)-1]
                indexColumna = self.lSimbolos.index(palabra[i])
                indexFila = self.lTransicion.index([estadoActual, cabezaPila])
                estadoDestino = self.mTransicion[indexFila][indexColumna][0]
                insercion = self.mTransicion[indexFila][indexColumna][1]
                pilaActual.pop()

                #time.sleep(1)
                self.windows._drawArista(estadoActual, estadoDestino, palabra[i], insercion)
                self.windows._quitarInfoPila() #Retiramos la cabeza de la pila, una vez se haya leido

                estadoActual = estadoDestino

                pilaActual = self.__updatePila(pilaActual, insercion) 
                self.windows._drawNodo(estadoActual)
            except (ValueError, IndexError) as inst:
                print('Opps! %s. Palabra no aceptada' % (inst.args))
                self.windows.estado.config(text='NO ACEPTADA')
                booleanError = True
                self.hablar("¡QUE MAL!, La palabra no ha sido aceptada")
                break
            
            

            #------Para prueba por consola-------#
            if palabra[i+1:len(palabra)] != '':
                print('(%s, %s, %s)' %(estadoActual, palabra[i+1:len(palabra)], pilaActual))
                self.windows._añadirInfoArbol('(%s, %s, %s)' %(estadoActual, palabra[i+1:len(palabra)], pilaActual))
            else:
                print('(%s, λ, %s)' %(estadoActual, pilaActual))
                self.windows._añadirInfoArbol('(%s, λ, %s)' %(estadoActual, pilaActual))
        
        if palabra_leida == palabra and estadoActual != self.eFinal and not booleanError:
            try:
                cabezaPila = pilaActual[len(pilaActual)-1]
                indexColumna = self.lSimbolos.index('λ') #3
                indexFila = self.lTransicion.index([estadoActual, cabezaPila]) #4
                estadoDestino = self.mTransicion[indexFila][indexColumna][0]
                insercion = self.mTransicion[indexFila][indexColumna][1]
                pilaActual.pop()

                self.windows._drawArista(estadoActual, estadoDestino, 'λ', insercion)
                self.windows._quitarInfoPila() #Retiramos la cabeza de la pila, una vez se haya leido
                
                estadoActual = estadoDestino
                
                pilaActual = self.__updatePila(pilaActual, insercion)
                self.windows._drawNodo(estadoActual)

                print('[(%s, λ, %s)] Configuración final' %(estadoActual, pilaActual))
                self.windows._añadirInfoArbol('[(%s, λ, %s)] Configuración final' %(estadoActual, pilaActual))
            except (ValueError, IndexError) as inst:
                print('Opps! %s. Palabra no aceptada' % (inst.args))
                self.windows.estado.config(text='NO ACEPTADA')
                booleanError = True
                self.hablar("¡QUE MAL!, La palabra no ha sido aceptada")

        self.windows._changeStateEntrada()
        if not booleanError:
            self.windows.estado.config(text='ACEPTADA')
            self.hablar("¡PERFECTO!... La palabra ha sido aceptada.")

    def __updatePila(self, pilaActual, str):  #Separa los caracteres del str para ingresarlos por separado en la pila(izq - der) y retornarla.
        newPila = list(pilaActual)
        for x in range(len(str)):
            if str[x] != 'λ':
                newPila.append(str[x])
                self.windows._añadirInfoPila(str[x])
                time.sleep(self.windows.seconds/len(str))
            else:  
                time.sleep(self.windows.seconds) #Se multiplica por dos para matener el ritmo de las transiciones
        #print(newPila)
        return newPila


    def hablar(self, str):
        speak = pyttsx3.init('sapi5')
        # while True:
        phrase = str # input("ingrese algo:")
        speak.say(phrase)
        speak.runAndWait()