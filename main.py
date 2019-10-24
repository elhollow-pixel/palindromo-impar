from aPila import automataPila
from interfaz import ventana

if __name__ == "__main__":
    lista_estados = [['p','#'],['p','a'],['p','b'],['q','#'],['q','a'],['q','b']]
    lista_simbolos = ['a','b','c','λ']
    estado_inicial = 'p'
    estado_final = 'r'
    matriz_transicion = [
        [['p','#a'],['p','#b'],['q','#'],[None]],
        [['p','aa'],['p','ab'],['q','a'],[None]],
        [['p','ba'],['p','bb'],['q','b'],[None]],
        [[None],[None],[None],['r','#']],
        [['q','λ'],[None],[None],[None]],
        [[None],['q','λ'],[None],[None]],    
    ]
    pilaVacia = ['#']
    aP = automataPila(estado_inicial,estado_final,lista_simbolos,lista_estados,matriz_transicion,pilaVacia)
    #aP._comprobarPalabra('aacaa')
    
    
    ventana(aP)._runApp()