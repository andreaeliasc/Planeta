#Andrea

import struct
import math
import collections
import time
from random import randint as random
from random import uniform as randomDec

#Estructura de tamanio caracter
def char(c):
	return struct.pack("=c", c.encode('ascii'))
#Estructura de tamanio word
def word(c):
	return struct.pack("=h", c)
#Estructura de tamanio dword
def dword(c):
	return struct.pack("=l", c)
#Asignar un color RGB
def color(r,g,b):
	return bytes([b,g,r])

#Metodo para crear ruido a partir de Perlin Noise
#Basado en el codigo C llamado perlin.c
#Creamos variables de tipo constantes para tomar valores al azar para el ruido
SEED = 0;
hasho = [208,34,231,213,32,248,233,56,161,78,24,140,71,48,140,254,245,255,247,247,40,
                     185,248,251,245,28,124,204,204,76,36,1,107,28,234,163,202,224,245,128,167,204,
                     9,92,217,54,239,174,173,102,193,189,190,121,100,108,167,44,43,77,180,204,8,81,
                     70,223,11,38,24,254,210,210,177,32,81,195,243,125,8,169,112,32,97,53,195,13,
                     203,9,47,104,125,117,114,124,165,203,181,235,193,206,70,180,174,0,167,181,41,
                     164,30,116,127,198,245,146,87,224,149,206,57,4,192,210,65,210,129,240,178,105,
                     228,108,245,148,140,40,35,195,38,58,65,207,215,253,65,85,208,76,62,3,237,55,89,
                     232,50,217,64,244,157,199,121,252,90,17,212,203,149,152,140,187,234,177,73,174,
                     193,100,192,143,97,53,145,135,19,103,13,90,135,151,199,91,239,247,33,39,145,
                     101,120,99,3,186,86,99,41,237,203,111,79,220,135,158,42,30,154,120,67,87,167,
                     135,176,183,191,253,115,184,21,233,58,129,233,142,39,128,211,118,137,139,255,
                     114,20,218,113,154,27,127,246,250,1,8,198,250,209,92,222,173,21,88,102,219]


#Se crea un metodo noise para hacer un mapeo dentro del array anterior de un valor, en modulo 256 y devolvemos el valor
def noise2(x, y):
    tmp = hasho[(y + SEED) % 256]
    return hasho[(tmp + x) % 256]

#Metodo que aplica una funcion X a los parametros mandados
def lin_inter(x, y, s):
    return float(x + s * (y-x))

#Medodo para aplicar una funcion X a los parametros mandados
def smooth_inter(x, y, s):
    return lin_inter(float(x), float(y), float(s * s * (3-2*s)))

#Metodo para crear ruido a partir del metodo noise2 y del smooth_inter
def noise2d(x, y):
    x_int = int(x)
    y_int = int(y)
    x_frac = float(x - x_int)
    y_frac = float(y - y_int)
    s = int(noise2(x_int, y_int))
    t = int(noise2(x_int+1, y_int))
    u = int(noise2(x_int, y_int+1))
    v = int(noise2(x_int+1, y_int+1))
    low = float(smooth_inter(s, t, x_frac))
    high = float(smooth_inter(u, v, x_frac))
    return float(smooth_inter(low, high, y_frac))

#Metodo para crear el valor entre 0 y 1 basados en Perlin2D, mandando un valor x y y entre 0 y 1,
#una frecuencia y una profundidad
def perlin2d(x, y, freq, depth):
    xa = float(x*freq)
    ya = float(y*freq)
    amp = float(1.0)
    fin = float(0)
    div = float(0.0)

    for i in range(depth):
        div += 256 * amp
        fin += noise2d(xa, ya) * amp
        amp /= 2
        xa *= 2
        ya *= 2

    return float(fin/div)

#Constantes y funciones sobre vectores
V2 = collections.namedtuple('Vertex2',['x','y'])
V3 = collections.namedtuple('Vertex3',['x','y','z'])

def sum(v0, v1):
        return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
        return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
        return V3(v0.x * k, v0.y * k, v0.z * k)

def dot(v0, v1):
        return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
        return V3(v0.y * v1.z - v0.z * v1.y, v0.z * v1.x - v0.x * v1.z, v0.x * v1.y - v0.y * v1.x)

def length(v0):
        return (v0.x**2 + v0.y**2 + v0.z**2)**0.5
        
def norm(v0):
        l = length(v0)
        if l == 0:
                return V3(0, 0, 0)
        else:
                return V3(v0.x/l, v0.y/l, v0.z/l)

#Funcion que multiplica matrices, que cumpla con la condicion de que el numero de
#columnas de la primer matriz sea igual al numero de filas de la segunda matriz, y
#si no las tiene regresa un mensaje de que no se pudo y retorna un cero
def multMatrices(primeraMatriz,segundaMatriz):
    #Se revisa si el numero de columnas de la primer matriz es igual al numero de
    #filas de la segunda matriz, en caso que no se regresa un mensaje que no se pudo y retorna un cero
    if len(primeraMatriz[0]) == len(segundaMatriz):
        #Se crea una matriz con el numero de filas de la primer matriz y el numero de columnas de la segunda matriz
        matrizResultado = [[0] * len(segundaMatriz[0]) for i in range(len(primeraMatriz))]
        #Se recorren las filas de la matriz
        for x in range(len(primeraMatriz)):
            #Se recorren las columnas de la matriz
            for y in range(len(segundaMatriz[0])):
                #Se recorre el valor comun de fila y columna para realizar las multiplicaciones de la operacion
                for z in range(len(primeraMatriz[0])):
                    #Probamos si se puede recorrer una posicion de la nueva matriz, si no se salta dicha posicion (que no existe)
                    try:
                        #Se hace la sumatoria de las multiplicaciones necesarias por pocision de la matriz
                        matrizResultado[x][y] += primeraMatriz[x][z] * segundaMatriz[z][y]
                    except IndexError:
                        pass
        #Se retorna la matriz resultante
        return matrizResultado
    else:
        print("No se pudo hacer la multiplicacion de matrices\ndebido a que el numero de columnas de la primer\nmatriz no es igual al numero de filas de la segunda matriz")
        return 0

#Se busca la caja mas pequena que contenga un triangulo dados sus vertices
def bbox(A, B, C):
    xs = sorted([int(A.x), int(B.x), int(C.x)])
    ys = sorted([int(A.y), int(B.y), int(C.y)])
    a = V2(int(xs[0]), int(ys[0]))
    b = V2(int(xs[2]), int(ys[2]))    
    return a, b

#Transforma a coordenadas baricentricas los vertices
def barycentric(A, B, C, P):
    cx, cy, cz = cross(V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y))

    if cz == 0: #cz no puede ser menor que 1
        return -1, -1, -1

    #Calculamos las coordenadas baricentricas
    u = cx/cz
    v = cy/cz
    w = 1 - (u + v)

    #Regresamos las coordenadas
    return  w, v, u

#Objeto que nos permite darle lectura a un archivo bmp y utilizarlo como textura de un modelo 3D
#Se crea un objeto de textura para Renderizar la textura BMP
#Basado en codigo Dennis Aldana
class Textura(object):
    def __init__(self, path):
        self.path = path
        self.read()

    #Leemos el archivo bmp y extraemos todos los valores del encabezado y pixeles
    def read(self):
        img = open(self.path, "rb")
        img.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", img.read(4))[0]
        img.seek(2 + 4 + 4 + 4 + 4)
        self.width = struct.unpack("=l", img.read(4))[0]
        self.height = struct.unpack("=l", img.read(4))[0]
        self.pixels = []
        img.seek(header_size)

        #Se hace un recorrido por el alto y ancho de la imagen y se lee el pixel
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(img.read(1))
                g = ord(img.read(1))
                r = ord(img.read(1))
                self.pixels[y].append(color(r, g, b))

        img.close()

    #Obtenemos los colores de cada pixel del archivo leido
    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        
        #Devolvemos el color de los bytes que tiene cada pixel de la imagen
        try:
                return bytes(
                    map(
                        lambda b: int(round(b*intensity)) if (b * intensity) > 0 else 0,
                        self.pixels[y][x]
                        )
                    )
        except IndexError:
                return bytes(
                    map(
                        lambda b: int(round(b*intensity)) if (b * intensity) > 0 else 0,
                        self.pixels[y-1][x-1]
                        )
                    )


    #Obtenemos el alto y ancho de la imagen bmp    
    def get_alto_ancho(self):
        a,b = self.height, self.width
        return a,b

#Objeto ArchivoObj para poder dar lectura a un archivo Obj y guardar sus valores de vertices y caras
#Referencia: Basado en ejemplo Dennis Aldana 
class ArchivoObj(object):
    def __init__(self,filename,mtl = None):
        #Se mantiene abierto el archivo hasta leer todas las lineas
        self.verificador = False
        with open(filename) as f:
            self.lines = f.read().splitlines()
        if mtl:
            self.verificador = True
            with open(mtl) as x:
                    self.lines2 = x.read().splitlines()

        #Se crean los arreglos para guardar las colecciones de vertices y caras del .obj
        self.vertices = []
        self.faces = []
        self.tvertices = []
        self.nvertices = []
        self.tipoMat = []
        self.kD = []
        self.ordenMateriales = []
        self.contadorCaras = []
        #Se crea un diccionario para guardar el material y su valor
        self.material = {}
        
        #Se da lectura al archivo .obj
        self.lectura()

    #Funcion para eliminar espacios vacios en los datos de las caras si existen
    def eliminarEspacio(self,cara):
        #Se guardan los datos de la cara separados en una lista
        almacenarDatos = cara.split('/')

        #Si hay datos "vacio" almacenados en la lista se eliminan
        if ("") in almacenarDatos:
                almacenarDatos[1] = 0
                #almacenarDatos.remove("")

        #Se devuelven los valores de la lista todos convertidos a enteros
        return map(int,almacenarDatos)

    #Funcion que lee cada una de las lineas del .obj extrayendo los valores de vertices y caras
    def lectura(self):
        if self.verificador:
             for line2 in self.lines2:
                if line2:
                     prefix2, value2 = line2.split(' ', 1)
                     if prefix2 == 'newmtl':
                             self.tipoMat.append(value2)
                     if prefix2 == 'Kd':
                             self.kD.append(list(map(float,value2.split(' '))))
             for indice in range(len(self.tipoMat)-1):
                self.material[self.tipoMat[indice]] = self.kD[indice]  

        self.mater = ""
        #self.ordenMateriales = []
        #Se lee cada una de las lineas guardadas
        for line in self.lines:
            #En caso exista la linea esta se separa en 2 en el primer lugar donde haya un espacio ' ' guardando la primera mitad en prefix y la segunda en value
            if line:
                prefix, value = line.split(' ', 1)

                #Si el prefix es una v es que estamos leyendo los vertices del cual sus coordenadas son mapeados en el value separados por espacios ' '
                if prefix == 'v':
                    self.vertices.append(list(map(float,value.split(' '))))
                if prefix == 'vt':
                    self.tvertices.append(list(map(float,value.split(' '))))
                #Si el prefix es un f es que estamos leyendo una cara de la cual guardaremos una coleccion de datos que nos brindaran los vertices que se usan para formar la cara separados por una diagonal en bloques separados por espacios
                if prefix == 'f':
                    if self.verificador:
                            listita = [list(self.eliminarEspacio(face)) for face in value.split(' ')]
                            listita.append(self.mater)
                            self.faces.append(listita)
                            #self.faces.append([list(self.eliminarEspacio(face)) for face in value.split(' ')])
                            #self.ordenMateriales.append(self.mater)
                    else:
                            self.faces.append([list(self.eliminarEspacio(face)) for face in value.split(' ')])
                if prefix == 'vn':
                    self.nvertices.append(list(map(float,value.split(' '))))
                if prefix == 'usemtl':
                    self.mater = value
                 
#Objeto Bitmap para controlar renderizado
class Bitmap(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.zbuffer = []
        self.clearColor = color(0,0,0)
        self.vertexColor = color(255,255,0)
        self.glClear()
        
    #Inicia el bitmap
    def glInit(self):
            pass
        
    #Crea una ventana guardando sus variables de ancho y altura
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    #Llena el framebuffer de pixeles de un solo color haciendo un limpiado de imagen
    def glClear(self):
        self.framebuffer = [
            [
                self.clearColor	for x in range(self.width)
                ]
            for y in range(self.height)
            ]
        self.zbuffer = [
            [
                 -1*float('inf') for x in range(self.width)
                 ]
            for y in range(self.height)
            ]
        
    #Cambia el color con que funcionara glClear en formato RGB
    def glClearColor(self,r,g,b):
        try:
                self.rc = round(255*r)
                self.gc = round(255*g)
                self.bc = round(255*b)
                self.clearColor = color(self.rc,self.gc,self.bc)
        except ValueError:
                print("No puede ingresar un numero mayor a 1 ni menor que 0 en el color")

    #Cambia el color de los pixeles que se renderizaran en formato RGB
    def glColor(self,r,g,b):
        try:
                self.rv = round(255*r)
                self.gv = round(255*g)
                self.bv = round(255*b)
                self.vertexColor = color(self.rv,self.gv,self.bv)
        except ValueError:
                print("No puede ingresar un numero mayor a 1 ni menor que 0 en el color")

    #Coloca un Pixel dentro del framebuffer para colocarlo en el renderizado con valores entre -1 y 1
    def glPoint(self,x,y,color):
        #Convertimos los valores entre -1 y 1 a valores enteros de acuerdo a las dimensiones del window
        x = int(round((x+1) * self.width / 2))
        y = int(round((y+1) * self.height / 2))
        try:
                self.framebuffer[y][x] = color
        except IndexError:
                #print("No fue imposible imprimir el punto dado que esta fuera de los limites de la imagen")
                pass
        
    #Crea una linea formada por la sucesion de puntos equivalentes a pixeles mandando una coordenada x,y inicia y una x,y final, osea 2 pixeles con valores x,y entre -1 y 1
    def glLine(self,x0, y0, x1, y1):
        #Convertimos los valores entre -1 y 1 a valores enteros de acuerdo a las dimensiones del window
        x0 = int(round((x0+1) * self.width / 2))
        y0 = int(round((y0+1) * self.height / 2))
        x1 = int(round((x1+1) * self.width / 2))
        y1 = int(round((y1+1) * self.height / 2))

        #Calulamos las diferencias entre las x y y        
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Creamos un boolean que nos permita conocer cual es la mayor diferencia
        steep = dy > dx

        #Si dy es mayor a dx entonces intercambiamos cada una de las coordenadas
        if steep:
                x0,y0 = y0,x0
                x1,y1 = y1,x1

        #Si el punto inicial en x es mayor que el final entonces intercambiamos los puntos
        if x0 > x1:
                x0,x1 = x1,x0
                y0,y1 = y1,y0

        #Calculamos nuevamente las diferencias
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Realizamos el calculo de los puntos que formaran la linea
        offset = 0 * 2 * dx 
        threshold = 0.5 * 2 * dx
        y = y0
        #Ciclo for para rellenar la linea con puntos sucesivos sin dejar espacio
        for x in range(x0, x1 + 1):
                if steep:
                        self.glPoint((float(y)/(float(self.width)/2))-1,(float(x)/(float(self.height)/2))-1,self.vertexColor)
                else:
                        self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertexColor)
                offset += dy
                if offset >= threshold:
                        y += 1 if y0 < y1 else -1
                        threshold += 1 * dx

    #Transformar un vertice a tuple
    def glTransform(self, vertex, translate=(0,0,0), scale=(1,1,1)):
        try:
                return V3(
                        (int(round((vertex[0]+1) * self.width / 2)) + translate[0]) * scale[0],
                        (int(round((vertex[1]+1) * self.height / 2)) + translate[1]) * scale[1],
                        (int(round((vertex[2]+1) * self.width / 2)) + translate[2]) * scale[2])
        except IndexError:
                return V3(
                        (int(round((vertex[0]+1) * self.width / 2)) + translate[0]) * scale[0],
                        (int(round((vertex[1]+1) * self.height / 2)) + translate[1]) * scale[1],
                        (int(round((0.0+1) * self.width / 2)) + translate[2]) * scale[2])
        
    #Transformar un vertice a tuple
    def glTransformT(self, vertex, anchoT=800, altoT=600,translate=(0,0,0), scale=(1,1,1)):
        try:
                return V3(
                        (int(round((vertex[0]) * anchoT)) + translate[0]) * scale[0],
                        (int(round((vertex[1]) * altoT)) + translate[1]) * scale[1],
                        (int(round((vertex[2]) * anchoT)) + translate[2]) * scale[2])
        except IndexError:
                return V3(
                        (int(round((vertex[0]) * anchoT)) + translate[0]) * scale[0],
                        (int(round((vertex[1]) * altoT)) + translate[1]) * scale[1],
                        (int(round((0.0) * anchoT)) + translate[2]) * scale[2])

    #Algorimo para rellenar triangulos se mandan 3 vertices en forma de tupla para rellenar un triangulo
    def glTriangle(self, a, b, c):
        if a.y > b.y:
                a, b = b, a
        if a.y > c.y:
                a, c = c, a
        if b.y > c.y:
                b, c = c, b

        pendientexAC = c.x - a.x
        pendienteyAC = c.y - a.y

        if pendienteyAC == 0:
                pendienteInversaAC = 0
        else:
                pendienteInversaAC = pendientexAC/pendienteyAC

        pendientexAB = b.x - a.x
        pendienteyAB = b.y - a.y
        
        if pendienteyAB == 0:
                pendienteInversaAB = 0
        else:
                pendienteInversaAB = pendientexAB/pendienteyAB

        for y in range(a.y, b.y + 1):
                xinicial = int(round(a.x - pendienteInversaAC * (a.y - y)))
                xfinal = int(round(a.x - pendienteInversaAB * (a.y - y)))

                if xinicial > xfinal:
                        xinical, xfinal = xfinal, xinicial

                for x in range(xinicial, xfinal + 1):
                        self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertexColor)

        pendientexBC = c.x - b.x
        pendienteyBC = c.y - b.y

        if pendienteyBC == 0:
                pendienteInversaBC = 0

        else:
                pendienteInversaBC = pendientexBC/pendienteyBC

        for y in range(b.y, c.y + 1):
                xinicial = int(round(a.x - pendienteInversaAC * (a.y - y)))
                xfinal = int(round(b.x - pendienteInversaBC * (b.y - y)))

                if xinicial > xfinal:
                        xinical, xfinal = xfinal, xinicial
                for x in range(xinicial, xfinal + 1):
                        self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertexColor)        

    #Algoritmo para rellenar triangulos
    #Basado en codigo Dennis Aldana
    def triangle(self, A, B, C, lucecita, color=None, texture=None, texture_coords=(), intensity = 1, normals_coords = ()):
        #Se calculan los valores maximos y minimos de x y y que contienen al triangulo
        bbox_min, bbox_max = bbox(A,B,C)
        #Recorremos a partir de los valores minimos y maximos la caja que contiene al triangulo 
        for x in range(bbox_min.x, bbox_max.x + 1):
                for y in range(bbox_min.y, bbox_max.y +1):
                        #Hacemos el calculo de las coordenadas baricentricas
                        w, v, u = barycentric(A, B, C, V2(x,y))

                        #Se comprueba que los valores de las coordenadas baricentricas no sean menores a cero
                        if w < 0 or v < 0 or u < 0:
                                continue
                        
                        if color:
                                self.vertexColor =  color
                             
                        #Aplicamos el metodo de gourad para objetos sin textura donde mandamos las
                        #coordenadas X y Y que vamos recorriendo, las coordenadas baricentricas,
                        #las coordenadas normales (V3) y la luz (V3) que se le dara al modelo
                        colorin = self.gourad2(
                                xy = (x,y),
                                bar = (w,v,u),
                                varing_normals = normals_coords,
                                light = lucecita)
                        self.vertexColor = colorin
                                
                        #En caso de haber textura se toma esta como el color del pixel
                        if texture:
                                tA, tB, tC = texture_coords

                                tx = tA.x * w + tB.x * v + tC.x * u
                                ty = tA.y * w + tB.y * v + tC.y * u

                                colorcito = texture.get_color(tx, ty, intensity)
                                self.vertexColor = colorcito

                                #Aplicamos el metodo de gourad para texturas donde mandamos las
                                #coordenadas baricentricas, las coordenadas de la textura
                                #un objeto de tipo textura, las coordenadas normales (V3)
                                #y la luz (V3) que se le dara al modelo
                                colorin = self.gourad(
                                        bar = (w,v,u),
                                        texture_coord=(tx,ty),
                                        textu = texture,
                                        varing_normals = normals_coords,
                                        light = lucecita)
                                self.vertexColor = colorin

                        #Se calcula la posicion en z del punto a pintar
                        z = A.z * w + B.z * v + C.z * u        

                        #Se verifica si se pinta el punto en caso su coordenada en z sea mayor a la anteriormente pintada en el mismo lugar

                        try:
                                if z > self.zbuffer[y][x]:
                                        self.glPoint((float(x)/(float(self.width)/2))-1, (float(y)/(float(self.height)/2))-1,self.vertexColor)
                                        self.zbuffer[y][x] = z
                        except IndexError:
                                pass
                        #Se pinta el punto     
                        #self.glPoint((float(x)/(float(self.width)/2))-1, (float(y)/(float(self.height)/2))-1, self.vertexColor)

    #Metodo para aplicar un shader a un modelo con textura
    def gourad(self, **kwargs):
        #Primero tomamos los parametros que nos mandan desde triangle
        w, v, u = kwargs['bar']

        #Tomamos los vectores normales
        nA, nB, nC = kwargs['varing_normals']

        #Tomamos la coordenadas de la textura
        tx, ty = kwargs['texture_coord']

        #Tomamos el vector de luz
        light = kwargs['light']

        #Tomamos un objeto de tipo textura para aplicar el metodo de get_color
        tex = kwargs['textu']

        #Calculamos el vector del color que corresponde el punto de la textura
        tcolor = tex.get_color(tx,ty)

        #Calculamos con las coordenadas baricentricas los valores de las normales para el nuevo vector normal
        nx = nA.x * w + nB.x * v + nC.x * u
        ny = nA.y * w + nB.y * v + nC.y * u
        nz = nA.z * w + nB.z * v + nC.z * u

        #Inicializamos el vector normal
        vn = V3(nx,ny,nz)

        #Se calcula la intensidad a partir de la nueva normal y la luz que le mandamos
        intensity = dot(vn, light)

        #Regresamos el color en modo byte para el objeto en modo b,g,r
        return bytes([
                int(tcolor[2] * intensity) if tcolor[2] * intensity > 0 else 0,
                int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
                int(tcolor[0] * intensity) if tcolor[0] * intensity > 0 else 0
       
        ])

    #Metodo para aplicar un shader fijo a un modelo sin textura
    def gourad2(self, **kwargs):
        #Se toman las coordenadas baricentricas mandadas en el triangle
        w, v, u = kwargs['bar']

        #Se toman las coordenadas X y Y desde triangle
        x, y = kwargs['xy']

        #Se toman las normales desde triangle
        nA, nB, nC = kwargs['varing_normals']

        #Se toma la luz desde triangle
        light = kwargs['light']

        #Se calculan los valores de las normales a partir de los vectores normales y las coord. baricentricas
        nx = nA.x * w + nB.x * v + nC.x * u
        ny = nA.y * w + nB.y * v + nC.y * u
        nz = nA.z * w + nB.z * v + nC.z * u

        #Se crea el vector de las normales calculadas
        vn = V3(nx,ny,nz)

        #Se calcula un valor entre 0 y 1 dependiendo el valor de X y Y, para mandarle al metodo Perlin 2D
        xi = float(float(x)/float(self.width))
        yi = float(float(y)/float(self.height))

        #Generamos el ruido a partir del Perlin 2D con frecuencia 10 y Profundidad 20
        ruido = perlin2d(xi,yi,10,20)

        #Calculamos el valor de Y de manera semi random con Perlin 2D y Random para que no se vea tan abrupto el cambio entre colores
        y = y + int(perlin2d(xi,yi,15,10)* random(0,40))

        #Se genera la intensidad del modelo por color        
        intensity = dot(vn, light)

        #Dependiendo la Y generada, vamos a pintar ese pixel del color del rango del if en donde caiga la Y
        if y > 765:
                
                return bytes([
                        int(204 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(150 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(6 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 755:
                
                return bytes([
                        int(255 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(255 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(255 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 745:
                
                return bytes([
                        int(204 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(113 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(0 * intensity * ruido) if 194 * intensity > 0 else 0
                ])
        if y > 715:
                return bytes([
                        int(204 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(113 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(0 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 700:
                return bytes([
                        int(253 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(159 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(83 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 690:
                
                return bytes([
                        int(253 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(159 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(83 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 670:
                
                return bytes([
                        int(254 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(218 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(188 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 650:
                
                return bytes([
                        int(236 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(171 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(0 * intensity * ruido) if 194 * intensity > 0 else 0
                ])
        if y > 640:
                
                return bytes([
                        int(236 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(171 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(0 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 560:
                
                return bytes([
                         int(255 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(200 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(85 * intensity * ruido) if 194 * intensity > 0 else 0       
                ])
        if y > 510:
                
                return bytes([
                       int(255 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(174 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(102 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 470:
                
                return bytes([
                       int(255 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(204 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(157* intensity * ruido) if 194 * intensity > 0 else 0
       

       
                ])
        if y > 430:
                
                return bytes([
                        int(255 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(153 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(62 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 410:
                
                return bytes([
                        int(230 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(140 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(81 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 400:
                
                return bytes([
                        int(180 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(188 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(24 * intensity * ruido) if 194 * intensity > 0 else 0
                ])
        if y > 380:
                
                return bytes([
                        int(241 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(173 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(31 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 360:
                
                return bytes([
                        int(221 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(225 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(62 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 340:
                
                return bytes([
                        int(255 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(255 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(255 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 320:
                
                return bytes([
                        int(226 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(156 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(61 * intensity * ruido) if 194 * intensity > 0 else 0
                ])
        if y > 300:
                
                return bytes([
                        int(223 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(145 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(38 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 280:
                
                return bytes([
                        int(207 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(184 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(54 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])
        if y > 260:
                
                return bytes([
                        int(219 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(72 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(51 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])        
        if y > 0:
                
                return bytes([
                        int(132 * intensity * ruido) if 120 * intensity > 0 else 0,
                        int(37 * intensity * ruido) if 176 * intensity > 0 else 0,
                        int(23 * intensity * ruido) if 194 * intensity > 0 else 0
       
                ])

    #Transforma el vector por uno pasado por un pipeline
    def glTransformMatrix(self, vector):
        vector_nuevo = [[vector.x],[vector.y],[vector.z],[1]]
        nuevo_vector = multMatrices(self.laMatriz,vector_nuevo)
        return V3(nuevo_vector[0][0]/nuevo_vector[3][0],nuevo_vector[1][0]/nuevo_vector[3][0],nuevo_vector[2][0]/nuevo_vector[3][0])
        
        
    #Creamos la matriz pipeline
    def glmatrizFinal(self):
        a = multMatrices(self.Model,self.View)
        b = multMatrices(self.Proyection,a)
        c = multMatrices(self.Viewport,b)
        self.laMatriz = c
        #print(self.laMatriz)
        
    #Funcion para cargar un archivo .obj para renderizarlo
    def glLoad(self, filename, mtl=None ,textura=None, translate=(0,0,0), scale=(1,1,1), rotate =(0,0,0)):
        #Se realiza la lectura del archivo .obj
        self.loadModelMatrix(translate,scale,rotate)
        self.glmatrizFinal()
        if not mtl:
                modelo3D = ArchivoObj(filename)
                modelo3D.lectura()
        else:
                modelo3D = ArchivoObj(filename,mtl)
                modelo3D.lectura()

        luz = V3(0,0.5,1)
        
        #Se realiza un recorrido de las caras del modelo para conocer su numero de vertices
        for face in modelo3D.faces:
                if mtl:
                        contadorVertices = len(face)-1
                else:
                        contadorVertices = len(face)
                #Revisamos que los vertices que conforman una cara sean 3
                if contadorVertices == 3:
                        #Se extraen los valores de los vertices de la cara
                        f1 = face[0][0] - 1
                        f2 = face[1][0] - 1
                        f3 = face[2][0] - 1

                        #Se extraen las coordenadas de los vertices
                        a = self.glTransform(modelo3D.vertices[f1],translate,scale)
                        b = self.glTransform(modelo3D.vertices[f2],translate,scale)
                        c = self.glTransform(modelo3D.vertices[f3],translate,scale)
                        #print("1",a)
                        a = self.glTransformMatrix(a)
                        b = self.glTransformMatrix(b)
                        c = self.glTransformMatrix(c)
                        #print("2",a)
                        #Se calcula el vector normal de la cara
                        n1 = face[0][2] - 1
                        n2 = face[1][2] - 1
                        n3 = face[2][2] - 1
                        normal = V3(*modelo3D.nvertices[n1])
                        ##print(normal)
                        #print(normal)
                        #normal = norm(cross(sub(b,a),sub(c,a)))
                        #print(normal)
                        #Se normalizan los valores de la luz
                        luz = norm(luz)
                        #Se calcula la intensidad de la luz
                        intensity = dot(normal,luz)
                        #print(intensity)
                        nA = V3(*modelo3D.nvertices[n1])
                        nB = V3(*modelo3D.nvertices[n2])
                        nC = V3(*modelo3D.nvertices[n3])
                        #Se revisa que la intensidad no se menor que cero para que no hayan problemas con el color
                        if intensity < 0:
                               continue

                        #En caso de haber una textura se manda a leer los valores de los vertices de la textura en el bmp
                        if textura:
                                #Se extraen los valores de los vertices de la cara de la tetura
                                tv1 = face[0][1] - 1
                                tv2 = face[1][1] - 1
                                tv3 = face[2][1] - 1
                                #print("***********")
                                #Se extraen las coordenadas de los vertices de la textura
                                #print(modelo3D.tvertices[tv1])
                                tvA = V2(*modelo3D.tvertices[tv1])
                                tvB = V2(*modelo3D.tvertices[tv2])
                                tvC = V2(*modelo3D.tvertices[tv3])
                                self.triangle(a,b,c,luz,texture = textura, texture_coords = (tvA, tvC, tvB),intensity = intensity, normals_coords = (nA, nC, nB))

                        #En caso de no haber textura solo se rellenan las caras con tonalidades de grises por la intensidad de luz
                        elif mtl:
                                material2 = face[3]
                                valorcito = modelo3D.material[material2]
                                self.triangle(a,b,c,luz,color = glColor(valorcito[0]*intensity,valorcito[1]*intensity, valorcito[2]*intensity))
                        else:
                                self.glColor(intensity, intensity, intensity)
                                self.triangle(a,b,c,luz,color = glColor(intensity, intensity, intensity), normals_coords = (nA, nC, nB))
                                #glColor(randomDec(0,1),randomDec(0,1),randomDec(0,1))
                                #self.glTriangle(a,b,c)
                                
                #Se recorre la cantidad de vertices para hacer las lineas del renderizado
                #for j in range(contadorVertices):
                        #Se obtienen un par de vertices de las caras
                        #f1 = face[j][0]
                        #f2 = face[(j+1)%contadorVertices][0]

                        #Se obtiene cada vertice indicado anteriormente del modelo, obteniendo asi sus coordenadas
                        #v1 = modelo3D.vertices[f1 - 1]
                        #v2 = modelo3D.vertices[f2 - 1]

                        #Se obtienen los valores de los vertives x,z guardados en la posicion 0 y 1 de los vertices y se le da escala y traslacion a estos
                        #x1 = (v1[0] + translate[0]) * scale[0]
                        #y1 = (v1[1] + translate[1]) * scale[1]
                        #x2 = (v2[0] + translate[0]) * scale[0]
                        #y2 = (v2[1] + translate[1]) * scale[1]

                        #Se dibuja la linea con los puntos obtenidos
                        #self.glLine(x1,y1,x2,y2)


    def loadModelMatrix(self, translate=(0,0,0),scale=(1,1,1),rotate=(0,0,0)):
        #translate = V3(*translate)
        #scale = V3(*scale)
        #rotate = V3(*rotate)
        
        translate_matrix = [
                [1,0,0,translate[0]],
                [0,1,0,translate[1]],
                [0,0,1,translate[2]],
                [0,0,0,1]
        ]
        
        scale_matrix = [
                [scale[0],0,0,0],
                [0,scale[1],0,0],
                [0,0,scale[2],0],
                [0,0,0,1]
        ]
        
        a = rotate[0]
        rotation_matrix_x = [
                [1,0,0,0],
                [0,math.cos(a),-1*(math.sin(a)),0],
                [0,math.sin(a),math.cos(a),0],
                [0,0,0,1]
        ]
        
        a = rotate[1]
        rotation_matrix_y = [
                [math.cos(a),0,math.sin(a),0],
                [0,1,0,0],
                [-1*(math.sin(a)),0,math.cos(a),0],
                [0,0,0,1]
        ]

        a = rotate[2]
        rotation_matrix_z = [
                [math.cos(a),-1*(math.sin(a)),0,0],
                [math.sin(a),math.cos(a),0,0],
                [0,0,1,0],
                [0,0,0,1]
        ]

        primera = multMatrices(rotation_matrix_z,rotation_matrix_y)
        rotation_matrix = multMatrices(primera,rotation_matrix_x)
        
        segunda = multMatrices(rotation_matrix,scale_matrix)
        self.Model = multMatrices(translate_matrix,segunda)
        
    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up,z))
        y = norm(cross(z,x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProyectionMatrix(1/length(sub(eye,center)))
        
    def loadViewMatrix(self, x, y, z, center):
        M = [
                [x.x,x.y,x.z,0],
                [y.x,y.y,y.z,0],
                [z.x,z.y,z.z,0],
                [0,0,0,1]
        ]
        O = [
                [1,0,0,-1*center.x],
                [0,1,0,-1*center.y],
                [0,0,1,-1*center.z],
                [0,0,0,1]
        ]
        self.View = multMatrices(M,O)

    def loadProyectionMatrix(self, coeff):
        self.Proyection = [
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,coeff,1]
        ]

    def loadViewportMatrix(self, x, y):
        self.Viewport = [
                [self.width/2,0,0,x+self.width/2],
                [0,self.height/2,0,y+self.height/2],
                [0,0,128,128],
                [0,0,0,1]
        ]

    #Funcion para cargar un archivo .obj para renderizarlo
    def glLoadTexture(self, filename,translate=(0,0), scale=(1,1)):
        #Se realiza la lectura del archivo .obj
        modelo3D = ArchivoObj(filename)
        modelo3D.lectura()

        #Se realiza un recorrido de las caras del modelo para conocer su numero de vertices
        for face in modelo3D.faces:
                contadorVertices = len(face)
                if contadorVertices == 3:

                        tv1 = face[0][1] - 1
                        tv2 = face[1][1] - 1
                        tv3 = face[2][1] - 1

                        tvA = V2(*modelo3D.tvertices[tv1])
                        tvB = V2(*modelo3D.tvertices[tv2])
                        tvC = V2(*modelo3D.tvertices[tv3])
                        tvAx, tvAy = tvA.x,tvA.y
                        tvBx, tvBy = tvB.x,tvB.y
                        tvCx, tvCy = tvC.x,tvC.y
                        
                        tvAx = (tvAx * 2) - 1
                        tvAy = (tvAy * 2) - 1
                        tvBx = (tvBx * 2) - 1
                        tvBy = (tvBy * 2) - 1
                        tvCx = (tvCx * 2) - 1
                        tvCy = (tvCy * 2) - 1

                        self.glLine(tvAx, tvAy,tvBx, tvBy)
                        self.glLine(tvBx, tvBy,tvCx, tvCy)
                        self.glLine(tvCx, tvCy,tvAx, tvAy)
                        
    #Conversion de numero normal a -1 a 1
    def glConvert(self, number, coordenada):
        if coordenada == "x":
                numeroNuevo = (float(number)/((self.width)/2))-1
        elif coordenada =="y":
                numeroNuevo = (float(number)/((self.height)/2))-1
        return float(numeroNuevo)

    #Rellena una figura delimitada por vertices que se unen en el orden que se mandan
    #Basado en Algoritmo Punto en Poligono y modificado para pintar los puntos dentro del poligono
    def glFill(self, poligono):
        #Se recorre cada punto de la imagen por coordenadas x,y con ciclos for
        for y in range(self.height):
                for x in range(self.width): 
                        i = 0
                        j = len(poligono) - 1
                        resultado = False
                        #Se realiza un ciclo que revisa si el punto siempre se encuentra entre los limites de los vertices planteados
                        for i in range(len(poligono)):
                                #Si el poligono se encuentra dentro de los limites la variable resultado esta dentro de los limites obtiene un valor True 
                                if (poligono[i][1] < y and poligono[j][1] >= y) or (poligono[j][1] < y and poligono[i][1] >= y):
                                        if poligono[i][0] + (y - poligono[i][1]) / (poligono[j][1] - poligono[i][1]) * (poligono[j][0] - poligono[i][0]) < x:
                                                resultado = not resultado
                                j = i
                        #Si el resultado es True entonces se pinta el punto 
                        if resultado == True:
                                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertexColor)
                        else:
                                pass

    #Genera la imagen renderizada en formato bmp recibiendo el nombre de la imagen como imagen.bmp
    def glFinish(self, filename):
        f = open(filename, 'wb')
        #file header 14
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(54 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(54))

        #image headear 40
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        for x in range(self.height):
            for y in range(self.width):
                    self.framebuffer[x][y]
                    f.write(self.framebuffer[x][y])

        f.close()

#Se crea un objeto para manejo de renderizados
objeto = Bitmap(1364,1020)
#pielGato = Textura("Textura1.bmp")
#rocas = Textura("Textura2.bmp")

#Funciones SR2
def glInit():
        objeto = Bitmap(800,600)
        
def glCreateWindow(width,height):
        objeto.glCreateWindow(width,height)
        
def glClear():
        objeto.glClear()

def glClearColor(r,g,b):
        objeto.glClearColor(r,g,b)

#Funcion de linea que recibe coordenadas de un punto inicial y uno final con valores x,y entre -1 y 1
def glLine(x0,y0,x1,y1):
        objeto.glLine(x0,y0,x1,y1)
#Funcion de punto que recibe una coordenada x,y con valores entre -1 y 1
def glPoint(x,y,color):
        objeto.glPoint(x,y,color)
        
def glColor(r,g,b):
        objeto.glColor(r,g,b)

#Funcion para cargar un archivo .obj para ser renderizado con traslado de sus puntos y a cierta escala
def glLoad(filename,textura=None, mtl = None ,translate=(0,0,0),scale=(1,1,1),rotate=(0,0,0)):
        objeto.glLoad(filename,textura=textura,mtl = mtl,translate=translate,scale=scale, rotate=rotate)
        
def glFinish(filename):
        objeto.glFinish(filename)

def glConvert(number,coordenada):
        num = objeto.glConvert(number,coordenada)
        return num

#Funcion para pintar un poligono internamente mandandole las coordenadas de los vertices del poligono en el orden en que se unen
def glFill(poligono):
        objeto.glFill(poligono)

def glTransform(a,b,c=10):
        a = objeto.glTransform([a,b,c])
        return a  

def glTriangle(a,b,c):
        objeto.glTriangle(a,b,c)

        
def glLookAt(eye,center,up):
        objeto.lookAt(eye, center, up)

def glLoadViewportMatrix(x, y):
        objeto.loadViewportMatrix(x, y)
        
