from tkinter import *
from tkinter.font import Font
from threading import Thread
import time
import os
import pyttsx3
import speech_recognition as sr

class ventana(Tk):
    speedS = 1
    speedF = 0
    carpetaImagenes = 'Grafo_Letras'

    def __init__(self, aPila):
        Tk.__init__(self)
        self.automataPila = aPila

        self.title('Automata de pila')
        #self.geometry('990x630')
        self.resizable(False, False)
        self.config(bg='white')
        
        self.__initUi()
        

    def __initUi(self):
        #Frame principal
        self.frame = Frame(self, width=990, height=630)
        self.frame.config(bg='white')
        self.frame.pack()
        
        #Frame en donde estara el diagrama de estados
        self.frame_diag = Frame(self.frame, width=700, height=400)
        self.frame_diag.config(bg='black')
        self.frame_diag.place(x=30, y=30)

        #Frame en donde estara la pila
        self.frame_pila = Frame(self.frame, width=200, height=400)#anchura altura
        self.frame_pila.config(bg='white')
        self.frame_pila.place(x=760, y=30)

        #Frame en donde estara el arbol de descripciones
        self.frame_arbol = Frame(self.frame, bg='white')
        self.frame_arbol.place(x=450, y=350)

        #Cargando imagen
        self.imagen = PhotoImage(file='%s/Grafo.png'%self.carpetaImagenes)
        self.diagrama = Label(self.frame_diag, image=self.imagen, bg='white')
        self.diagrama.pack()


        #Añadiendo pila
        self.tituloPila = Label(self.frame_pila, text='Representacion de la pila', bg='white')
        self.tituloPila.pack()
        scrollbar = Scrollbar(self.frame_pila, orient=VERTICAL) #Crear el scroll para la listaP que se encuetnra dentro self.frame_pila
        self.listaP = Listbox(self.frame_pila, borderwidth=0, activestyle=NONE, highlightcolor='lightgray', highlightbackground='lightgray',font=Font(size=10), yscrollcommand=scrollbar.set, justify=CENTER)
        scrollbar.config(command=self.listaP.yview)
        scrollbar.pack(side=RIGHT, fill=Y) #Ubicarla a la derecha de la listaP
        self.listaP.pack()
        
        #Añadiendo botones
        self.botonL = Button(self.frame, bg='lightgray', text='Lento', justify=CENTER, width=20, relief="flat",bd=4, command=lambda: self.__iniciar(self.speedS, self.automataPila))
        self.botonL.place(x=30, y=500)
        self.botonR = Button(self.frame, bg='lightgray',text='Rapido', justify=CENTER, width=20, relief="flat",bd=4, command=lambda: self.__iniciar(self.speedF, self.automataPila))
        self.botonR.place(x=200, y=500) 
        self.botonA = Button(self.frame, text='Ayuda',justify=CENTER, width=10, relief="flat", bg='gray', highlightcolor='lightgray', highlightbackground='lightgray', activebackground='white', bd=5, command=self.ayuda)
        self.botonA.place(x=10, y=10)
#---------------------------------
        self.botonE = Button(self.frame, bd=4, text='Escuchar',width=10,relief="flat", bg='gray',command=self.escuchar)
        self.botonE.place(x=30, y=450)
#---------------------------------
        #Añadiendo field text(Entry)
        self.entrada = Entry(self.frame, justify=CENTER, width=34, font=Font(size=13), highlightcolor='black', highlightbackground='lightgray', relief=RIDGE, borderwidth=3)
        self.entrada.place(x=35, y=540)

        #Añadiendo informacion en el diagrama estado ; aca puedo modificar las posiciones y el color de las label de transicion
        self.infoP = Label(self.frame_diag, bg='white')
        self.infoP.place(x=150, y=100)
        self.infoPQ = Label(self.frame_diag, bg='white')
        self.infoPQ.place(x=220, y=200)
        self.infoQ = Label(self.frame_diag, bg='white')
        self.infoQ.place(x=390, y=100)
        self.infoQR = Label(self.frame_diag, bg='white')
        self.infoQR.place(x=450, y=200)

        #Añadiendo historial del arbol de descripciones instantáneas
        self.tituloArbol = Label(self.frame_arbol, text='Arbol de descripciones instantáneas', bg='white')
        #self.tituloArbol.place(x=600, y=325)
        self.tituloArbol.pack()
        yscrollbarArbol = Scrollbar(self.frame_arbol, orient=VERTICAL)
        xscrollbarArbol = Scrollbar(self.frame_arbol, orient=HORIZONTAL)

        self.listaArbol = Listbox(self.frame_arbol, borderwidth=0, activestyle=NONE, highlightcolor='lightgray', highlightbackground='lightgray',font=Font(size=10), width=70, height=12, xscrollcommand=xscrollbarArbol.set, yscrollcommand=yscrollbarArbol.set)
        xscrollbarArbol.config(command=self.listaArbol.xview)
        yscrollbarArbol.config(command=self.listaArbol.yview)
        xscrollbarArbol.pack(side=BOTTOM, fill=X)
        yscrollbarArbol.pack(side=RIGHT, fill=Y)
        #self.listaArbol.place(x=450, y=350)
        self.listaArbol.pack()


        #Añadiendo label de PALABRA ACEPTADA o NO ACEPTADA
        self.estado = Label(self.frame, text='', font=Font(size=20), bg='white')
        self.estado.place(x=100, y=400)
        #self.listaP.insert(END, '#')
        
        
    def __iniciar(self, seconds, aPila):
        self.seconds = seconds
        self.listaArbol.delete(0, END)
        self.listaP.delete(0, END)
        self.estado.config(text='')
        self.infoP.config(text='')
        self.infoPQ.config(text='')
        self.infoQ.config(text='')
        self.infoQR.config(text='')

        palabra = self.entrada.get()
        

        hiloComprobandoP = Thread(name='Hilo_ComprobandoPalabra', target=lambda: aPila._comprobarPalabra(palabra, self))
        hiloComprobandoP.start()
        
        self._changeStateEntrada()
        #aPila._comprobarPalabra(palabra, self)



    def _añadirInfoPila(self, info):
        self.listaP.insert(END, info)
        self.listaP.see(END)
        #time.sleep(self.seconds)
        

    def _quitarInfoPila(self):
        self.listaP.delete(END)
        #time.sleep(self.seconds)
        

    def _añadirInfoArbol(self, info):
        self.listaArbol.insert(END, info)
        self.listaArbol.see(END)
        #time.sleep(self.seconds)

    def _changeStateEntrada(self):
        if self.entrada['state'] == 'readonly':
            self.entrada.config(state=NORMAL)
            self.botonL.config(state=NORMAL)
            self.botonR.config(state=NORMAL)
            self.botonE.config(state=NORMAL)
        else:
            self.entrada.config(state='readonly')
            self.botonL.config(state=DISABLED)
            self.botonR.config(state=DISABLED)
            self.botonE.config(state=DISABLED)

    def _drawNodo(self, estado):
        if estado != None:
            self.imagen = PhotoImage(file='%s/%s.png' %(self.carpetaImagenes, estado))
            self.diagrama.config(image=self.imagen)
            time.sleep(self.seconds)
        else:
            self.estado.config(text='NO ACEPTADA')
            self.mainloop('NO ACEPTADA')
            self.hablar("NO ACEPTADA")

    def _drawArista(self, origen, destino, simbolo, insercion):
        if origen != None and destino != None:
            self.imagen = PhotoImage(file='%s/%s,%s.png' %(self.carpetaImagenes, origen, destino))
            self.diagrama.config(image=self.imagen)

            #Hacemos el update al label correspondiente.
            if origen == 'p' and destino == 'p':
                self.infoP.config(text=simbolo+' \\ '+self.listaP.get(END)+' \\ '+insercion)

            if origen == 'q' and destino == 'q':
                self.infoQ.config(text=simbolo+' \\ '+self.listaP.get(END)+' \\ '+insercion)

            if origen == 'p' and destino == 'q':
                self.infoPQ.config(text=simbolo+' \\ '+self.listaP.get(END)+' \\ '+insercion)

            if origen == 'q' and destino == 'r':
                self.infoQR.config(text=simbolo+' \\ '+self.listaP.get(END)+' \\ '+insercion)

        else:
            self.estado.config(text='NO ACEPTADA')
            self.hablar('NO ACEPTADA')

    def escuchar(self):
        speak = pyttsx3.init('sapi5')
        phrase = "te escucho"
        speak.say(phrase)
        speak.runAndWait()

        reconocer = sr.Recognizer()

        with sr.Microphone() as source:

            print('Di algo: ')
            audio = reconocer.listen(source)
            try:
                # vamos a convertir el audio a texto
                text = reconocer.recognize_google(audio, language='es_CO')
                print('Dijiste esto: {}'.format(text))

                if (text == "Rapido"):
                    print("rapido 1")
                    self.__iniciar(0.5, self.automataPila)
                elif (text == "rápido"):
                    print("rapido 2")
                    self.__iniciar(0.5, self.automataPila)
                elif (text == "Lento"):
                    print("lento 1")
                    self.__iniciar(2, self.automataPila)
                elif (text == "lento"):
                    print("lento 2")
                    self.__iniciar(2, self.automataPila)
                elif (text == "Ayuda"):
                     self.ayuda()
                elif (text == "ayuda"):
                     self.ayuda()
            except Exception:
                    print('lo siento, no pude reconocer tu voz')
                    self.hablar('lo siento, no pude reconocer tu voz')

    def hablar(self, str):
        speak = pyttsx3.init('sapi5')
        phrase = str
        speak.say(phrase)
        speak.runAndWait()

    def ayuda(self):
        os.popen("ayuda.pdf")

    def _runApp(self):
        self.mainloop()
        