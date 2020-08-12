#Andrea Elias 17048

from Lab3 import *

#Definicion de funcion para renderizar Modelo shpere3 con un shader para hacerlo como Jupiter
def renderizarPlaneta():
    glInit()
    glCreateWindow(1000,1000)
    glClear()
    glColor(1,1,1)
    #Hacemos unas estrellas para el fondo
    for i in range(300):
        try:
            glColor(1,1,1)
            glPoint(randomDec(-1,1),randomDec(-1,1),color(255,255,255))
        except IndexError:
            pass
    for i in range(150):
        try:
            glColor(1,1,1)
            posEstrellaX = randomDec(-1,1)
            posEstrellaY = randomDec(-1,1)
            for q in range(2):
                for n in range(2):
                    glPoint(posEstrellaX + q*(2.0/1000.0),posEstrellaY + n *(2.0/1000.0),color(255,255,255))
        except IndexError:
            pass
    for i in range(10):
        try:
            glColor(1,1,1)
            posEstrellaX = randomDec(-1,1)
            posEstrellaY = randomDec(-1,1)
            for q in range(3):
                for n in range(3):
                    glPoint(posEstrellaX + q*(2.0/1000.0),posEstrellaY + n *(2.0/1000.0),color(255,255,255))
        except IndexError:
             pass
    for i in range(35):
        try:
            glColor(1,1,1)
            posEstrellaX = randomDec(-1,1)
            posEstrellaY = randomDec(-1,1)
            for q in range(5):
                for n in range(5):
                    if (q == 0 and n == 0) or (q == 0 and n == 1) or (q == 0 and n == 3) or (q == 0 and n == 4) or (q == 4 and n == 0) or (q == 4 and n == 1) or (q == 4 and n == 3) or (q == 4 and n == 4) or (q == 1 and n == 0) or (q == 1 and n == 4) or (q == 3 and n == 0) or (q == 3 and n == 4):
                        pass
                    else:
                        glPoint(posEstrellaX + n*(2.0/1000.0),posEstrellaY + q *(2.0/1000.0),color(255,255,255))
        except IndexError:
            pass
    #Se renderiza el modelo
    glLookAt(V3(-0.2,0,5),V3(0,0,0),norm(V3(0,1,0)))
    glLoadViewportMatrix(0, 0)
    glLoad("sphere3.obj", translate=(-1.0,-0.9,0), scale=(0.04,0.04,0.04), rotate=(0,0.2,0))
    glFinish("Pandita.bmp")


#Menu para Interaccion
opcion = 1
while opcion != 2: 
        print("Hola: \n1.Shader Neptuno \n2. Salir")
        opcion = input("Ingrese la opcion que desea renderizar: ")
        try:
                opcion = int(opcion)
                if opcion == 1:
                    renderizarPlaneta()
                else: 
                        print("Ha ingresado una opcion invalida")
        except ValueError:
                print("El dato que ingreso no es valido")
print("Hasta Pronto\n")
