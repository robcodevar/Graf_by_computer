import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import math
import numpy as np

def flood_fill_puntos(canvas, x, y, color_reemplazo, color_borde1="#dddfef", color_borde2="black"):
    # Implementa el algoritmo de relleno por difusión (flood fill) para pintar un área delimitada por
    # un color de borde en un objeto canvas. La función toma como entrada un objeto canvas, las
    # coordenadas (x, y) del punto de inicio, el color de reemplazo para llenar el área y dos colores
    # de borde.
    
    # canvas: El objeto canvas en el que se realizará el relleno.
    # x: Coordenada x del punto de inicio.
    # y: Coordenada y del punto de inicio.
    # color_reemplazo: Color con el que se llenará el área.
    # color_borde1: Primer color de borde del área a rellenar.
    # color_borde2: Segundo color de borde del área a rellenar.
    color_inicial = canvas.obtener_color_pixel(x, y)
    
    pila = [(x, y)]
    visitados = set()
    en_pila = set([(x, y)])
    
    while pila:
        x, y = pila.pop()
        en_pila.remove((x, y))
    
        if (x, y) in visitados:
            continue
    
        # Pinta el rectángulo actual
        canvas.create_rectangle(x-5, y-5, x + 5, y+5, outline=color_reemplazo, fill=color_reemplazo)
    
        visitados.add((x, y))
    
        # Recorre los vecinos del punto actual
        for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5)]:
            nx, ny = x + dx, y + dy
            pixel_color = canvas.obtener_color_pixel(nx, ny)
    
            # Verifica si el vecino no es un borde y no ha sido visitado ni agregado a la pila
            if pixel_color != color_borde1 and pixel_color != color_borde2:
                if (nx, ny) not in visitados and (nx, ny) not in en_pila:
                    pila.append((nx, ny))
                    en_pila.add((nx, ny))
    return

def bresenham(x1, y1, x2, y2, line_style='dashed'):
    
    # Implementa el algoritmo de Bresenham para trazar una línea entre dos puntos en un espacio discreto
    # de coordenadas. La función toma como entrada las coordenadas de los puntos inicial y final, y un
    # estilo de línea opcional (línea continua o discontinua).

    # :param x1: Coordenada x del punto inicial.
    # :param y1: Coordenada y del punto inicial.
    # :param x2: Coordenada x del punto final.
    # :param y2: Coordenada y del punto final.
    # :param line_style: Estilo de línea, 'dashed' para línea discontinua o cualquier otro valor para línea continua.
    # :return: Lista de puntos que forman la línea trazada.
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 10 if x1 < x2 else -10
    sy = 10 if y1 < y2 else -10
    err = dx - dy
    x, y = x1, y1
    puntos = []

    segment_length = 1
    current_length = 0
    current_color = "black"

    while True:
        color = current_color if line_style == 'dashed' else 'black'
        puntos.append((x, y, color))

        if x == x2 and y == y2:
            break

        e2 = 2 * err
        # Mueve el punto en el eje x
        if e2 > -dy:
            err -= dy
            x += sx
        # Mueve el punto en el eje y
        if e2 < dx:
            err += dx
            y += sy

        # Cambia el color para simular una línea discontinua
        if line_style == 'dashed':
            current_length += 1
            if current_length % 4 == 1 or current_length % 4 == 2 or current_length % 4 == 3:
                current_color = "black"
            else:
                current_color = "#dddfef"

    return puntos

# !
def line(x1, y1, x2, y2, color='black', segment_length=1, line_style='solid'):
    puntos = []
    square_size = 10

    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    a = y2 - y1
    b = x1 - x2
    c = x2*y1 - x1*y2

    if abs(b) > abs(a):
        if x2 < x1:
            x1, x2 = x2, x1
        current_length = 0
        current_color = color
        for x in range(x1, x2+1, square_size):
            y = round((-a*x - c) / b)
            y = (y // square_size) * square_size + square_size // 2
            if line_style == 'dashed':
                if current_length == 0:
                    current_color = color if current_color != color else 'white'
                    current_length = segment_length
                else:
                    current_length -= 1
            puntos.append((x, y, current_color))
        if x2 % square_size != 0:
            y = round((-a*x2 - c) / b)
            y = (y // square_size) * square_size + square_size // 2
            puntos.append((x2, y, current_color))
    else:
        if y2 < y1:
            y1, y2 = y2, y1
        current_length = 0
        current_color = color
        for y in range(y1, y2+1, square_size):
            x = round((-b*y - c) / a)
            x = (x // square_size) * square_size + square_size // 2
            if line_style == 'dashed':
                if current_length == 0:
                    current_color = color if current_color != color else 'white'
                    current_length = segment_length
                else:
                    current_length -= 1
            puntos.append((x, y, current_color))
        if y2 % square_size != 0:
            x = round((-b*y2 - c) / a)
            x = (x // square_size) * square_size + square_size // 2
            puntos.append((x, y2, current_color))

    return puntos
# !
# !
def punto_medio(x0, y0, radio):
    radio_en_pixeles = math.ceil(radio / 10)
    x = 0
    y = radio_en_pixeles
    d = 1 - radio_en_pixeles
    puntos = []
    while x <= y:
        puntos.append((x0 + x * 10, y0 + y * 10))
        puntos.append((x0 + y * 10, y0 + x * 10))
        puntos.append((x0 - y * 10, y0 + x * 10))
        puntos.append((x0 - x * 10, y0 + y * 10))
        puntos.append((x0 - x * 10, y0 - y * 10))
        puntos.append((x0 - y * 10, y0 - x * 10))
        puntos.append((x0 + y * 10, y0 - x * 10))
        puntos.append((x0 + x * 10, y0 - y * 10))
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    return puntos
# !
def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

class Figura:
    # Clase base para representar figuras geométricas en un espacio bidimensional. Esta clase contiene
    # atributos comunes a todas las figuras, como coordenadas, color, grosor, tipo de línea, escala y rotación.

    # :param x: Coordenada x de la figura.
    # :param y: Coordenada y de la figura.
    # :param color: Color de la figura.
    # :param grosor: Grosor del borde de la figura.
    # :param tipo_linea: Tipo de línea para el borde de la figura ('solid' u otros).
    
    def __init__(self, x, y, color='White', grosor=10, tipo_linea='solid'):
        self.x = x
        self.y = y
        self.color = color
        self.grosor = grosor
        self.tipo_linea = tipo_linea
        self.escala = 1
        self.borde_seleccionado = False
        self.rotacion = 0

    def set_rotacion(self, angulo):
        # Establece la rotación de la figura en grados.
        self.rotacion = angulo % 360

    def escalar(self, factor):
        # Establece el factor de escala de la figura.
        self.escala = factor

    def get_escala(self):
        # Obtiene el factor de escala de la figura.
        return self.escala

    def get_rotacion(self):
        # Obtiene la rotación de la figura en grados.
        return self.rotacion

    def rotar(self, rotacion):
        # Rota la figura en grados.
        self.rotacion = rotacion

    def cambiar_color(self, color):
        # Cambia el color de la figura.
        self.color = color

    def trasladar(self, dx, dy):
        # Traslada la figura en el eje x e y.
        self.x += dx
        self.y += dy

    def imprimir_atributos(self):
        # Imprime los atributos de la figura.
        pass

    def colorear(self, canvas):
        # Método para colorear la figura en un objeto canvas.
        pass
      
class Cuadrado(Figura):
    
    # Clase que representa un cuadrado en un espacio bidimensional. Hereda de la clase Figura.

    # :param color: Color del cuadrado.
    # :param grosor: Grosor del borde del cuadrado.
    # :param tipo_linea: Tipo de línea para el borde del cuadrado ('solid' u otros).
    
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, color='black', grosor=1, tipo_linea='solid'):
        super().__init__(x1, y1, color, grosor, tipo_linea)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.escala = 1
        self.rotacion = 0

    def colisiona_con_punto(self, x, y):
        # """
        # Determina si un punto dado (x, y) colisiona con la figura utilizando el algoritmo de ray casting.
        # Este algoritmo traza un rayo horizontal desde el punto (x, y) hacia la derecha y cuenta cuántas
        # veces cruza los bordes de la figura. Si el número de cruces es impar, el punto está dentro de la
        # figura, de lo contrario, está fuera.

        # :param x: Coordenada x del punto.
        # :param y: Coordenada y del punto.
        # :return: Verdadero (True) si el punto colisiona con la figura, Falso (False) en caso contrario.
        # """
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = self.coordenadas_escaladas()
        x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = self.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

        puntos = [(x1_rotado, y1_rotado), (x2_rotado, y2_rotado), (x3_rotado, y3_rotado), (x4_rotado, y4_rotado)]
        n_puntos = len(puntos)

        intersecciones = 0
        p1_x, p1_y = puntos[0]

        # Recorre los lados de la figura
        for i in range(1, n_puntos + 1):
            p2_x, p2_y = puntos[i % n_puntos]

            # Verifica si el punto está dentro de la región acotada por el par de puntos (lado) actual
            if y > min(p1_y, p2_y) and y <= max(p1_y, p2_y) and x <= max(p1_x, p2_x):
                if p1_y != p2_y:
                    x_intersect = (y - p1_y) * (p2_x - p1_x) / (p2_y - p1_y) + p1_x
                if p1_x == p2_x or x <= x_intersect:
                    intersecciones += 1

            p1_x, p1_y = p2_x, p2_y

        return intersecciones % 2 == 1
    
    def coordenadas_escaladas(self):
        # """
        # Calcula y devuelve las coordenadas escaladas de la figura en función del factor de escala.
        # La función escala la figura alrededor del punto superior izquierdo, es decir, el punto con la
        # coordenada x más pequeña y la coordenada y más pequeña.

        # :return: Las 8 coordenadas escaladas de la figura.
        # """
        x1, y1, x2, y2, x3, y3, x4, y4 = self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4

        # Identifica el punto superior izquierdo (el que tiene la coordenada x más pequeña y la coordenada y más pequeña)
        puntos = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        punto_superior_izquierdo = np.argmin(puntos, axis=0)[0]

        # Calcula la matriz de escalado
        escala_matriz = np.array([[self.escala, 0], [0, self.escala]])

        # Escala las coordenadas
        puntos_escalados = puntos - puntos[punto_superior_izquierdo]  # Resta el punto superior izquierdo
        puntos_escalados = np.dot(puntos_escalados, escala_matriz)    # Multiplica por la matriz de escalado
        puntos_escalados = puntos_escalados + puntos[punto_superior_izquierdo]  # Suma el punto superior izquierdo

        # Redondea las coordenadas escaladas
        puntos_escalados = np.round(puntos_escalados / 10) * 10

        # Devuelve las 8 coordenadas escaladas
        x1_escalado, y1_escalado = puntos_escalados[0]
        x2_escalado, y2_escalado = puntos_escalados[1]
        x3_escalado, y3_escalado = puntos_escalados[2]
        x4_escalado, y4_escalado = puntos_escalados[3]
        return x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado
    
    def puntos_rotados(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # """
        # Calcula y devuelve las coordenadas de los puntos de la figura después de aplicar la rotación.
        # La función rota la figura alrededor de su centro. El centro se calcula como el punto medio
        # entre las coordenadas (x1, y1) y (x3, y3).

        # :return: Las 8 coordenadas de los puntos rotados.
        # """
        puntos = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

        # Calcula el centro de la figura
        centro_x = (x1 + x3) / 2
        centro_y = (y1 + y3) / 2

        # Calcula el ángulo de rotación en radianes
        rad = math.radians(self.rotacion)
        cos_rad = math.cos(rad)
        sin_rad = math.sin(rad)

        # Crea la matriz de rotación
        rotacion_matriz = np.array([[cos_rad, sin_rad], [-sin_rad, cos_rad]])

        # Aplica la rotación a los puntos
        puntos_rotados = puntos - np.array([centro_x, centro_y])  # Resta el centro de la figura
        puntos_rotados = np.dot(puntos_rotados, rotacion_matriz)  # Multiplica por la matriz de rotación
        puntos_rotados = puntos_rotados + np.array([centro_x, centro_y])  # Suma el centro de la figura

        # Redondea las coordenadas de los puntos rotados
        puntos_rotados = np.round(puntos_rotados / 10) * 10

        x1_rotado, y1_rotado = puntos_rotados[0]
        x2_rotado, y2_rotado = puntos_rotados[1]
        x3_rotado, y3_rotado = puntos_rotados[2]
        x4_rotado, y4_rotado = puntos_rotados[3]

        return x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado
   
    def colorear(self, canvas):
        # """
        # Colorea el cuadrado en el objeto canvas proporcionado. Este método escala y rota el cuadrado
        # antes de colorearlo utilizando el algoritmo flood fill, que rellena el área delimitada por los
        # bordes del cuadrado con el color especificado.

        # :param canvas: Objeto canvas donde se dibujará el cuadrado.
        # """
        # Calcula las coordenadas escaladas y rotadas del cuadrado
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = self.coordenadas_escaladas()
        x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = self.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

        # Calcula el centro del cuadrado rotado y escalado
        centro_x = (x1_rotado + x3_rotado) / 2
        centro_y = (y1_rotado + y3_rotado) / 2

        # Redondea las coordenadas del centro a múltiplos de 5
        semilla_x = round(centro_x / 10) * 10
        semilla_y = round(centro_y / 10) * 10

        # Realiza el relleno utilizando las coordenadas de la semilla
        flood_fill_puntos(canvas, semilla_x, semilla_y, self.color)

    def trasladar(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy
        self.x4 += dx
        self.y4 += dy



class Triangulo(Figura):
    # """
    # Clase Triangulo que hereda de Figura. Representa un triángulo en un plano 2D con
    # puntos (x1, y1), (x2, y2) y (x3, y3). Permite cambiar el color, el grosor y
    # el tipo de línea, así como realizar transformaciones de escala y traslación.

    # :param color: Color del triángulo (por defecto 'black').
    # :param grosor: Grosor de la línea del triángulo (por defecto 1).
    # :param tipo_linea: Tipo de línea del triángulo (por defecto 'solid').
    # """
    def __init__(self, x1, y1, x2, y2, x3, y3, color='black', grosor=1, tipo_linea='solid'):
        super().__init__(x1, y1, color, grosor, tipo_linea)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.escala = 1
    
    def coordenadas_escaladas(self):
        # """
        # Calcula las coordenadas escaladas del triángulo, manteniendo la proporción
        # original y escalándolo desde el punto superior (el vértice con la coordenada y más pequeña).

        # :return: Seis coordenadas escaladas (x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado).
        # """
        x1, y1, x2, y2, x3, y3 = self.x1, self.y1, self.x2, self.y2, self.x3, self.y3

        # Identifica el punto superior (el que tiene la coordenada y más pequeña)
        puntos = np.array([[x1, y1], [x2, y2], [x3, y3]])
        punto_superior = np.argmin(puntos, axis=0)[1]

        # Calcula la matriz de escalado
        escala_matriz = np.array([[self.escala, 0], [0, self.escala]])

        # Escala las coordenadas
        puntos_escalados = puntos - puntos[punto_superior]
        puntos_escalados = np.dot(puntos_escalados, escala_matriz)
        puntos_escalados = puntos_escalados + puntos[punto_superior]

        # Redondea las coordenadas escaladas
        puntos_escalados = np.round(puntos_escalados / 10) * 10

        # Devuelve las 6 coordenadas escaladas
        x1_escalado, y1_escalado = puntos_escalados[0]
        x2_escalado, y2_escalado = puntos_escalados[1]
        x3_escalado, y3_escalado = puntos_escalados[2]
        return x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado

    def puntos_rotados(self, x1, y1, x2, y2, x3, y3):
        # """
        # Rota los puntos del triángulo alrededor de su centroide según el ángulo de rotación.

        # :param x1: Coordenada x del primer vértice del triángulo.
        # :param y1: Coordenada y del primer vértice del triángulo.
        # :param x2: Coordenada x del segundo vértice del triángulo.
        # :param y2: Coordenada y del segundo vértice del triángulo.
        # :param x3: Coordenada x del tercer vértice del triángulo.
        # :param y3: Coordenada y del tercer vértice del triángulo.
        # :return: Coordenadas rotadas de los vértices del triángulo.
        # """
        puntos = [[x1, y1], [x2, y2], [x3, y3]]

        # Calcular el centroide del triángulo
        centro_x, centro_y = Triangulo.punto_medio_triangulo(x1, y1, x2, y2, x3, y3)

        # Convertir el ángulo de rotación en radianes y calcular sus valores de seno y coseno
        rad = math.radians(self.rotacion)
        cos_rad = math.cos(rad)
        sin_rad = math.sin(rad)

        puntos_rotados = []
        for punto in puntos:
            x, y = punto
            # Aplicar la matriz de rotación a las coordenadas
            x_rotado = cos_rad * (x - centro_x) - sin_rad * (y - centro_y) + centro_x
            y_rotado = sin_rad * (x - centro_x) + cos_rad * (y - centro_y) + centro_y
            # Redondear las coordenadas a múltiplos de 10
            x_rounded = round(x_rotado / 10) * 10
            y_rounded = round(y_rotado / 10) * 10
            puntos_rotados.append([x_rounded, y_rounded])

        x1_rotado, y1_rotado = puntos_rotados[0]
        x2_rotado, y2_rotado = puntos_rotados[1]
        x3_rotado, y3_rotado = puntos_rotados[2]

        return x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado


    def punto_medio_triangulo(x1, y1, x2, y2, x3, y3):
        x_medio = (x1 + x2 + x3) / 3
        y_medio = (y1 + y2 + y3) / 3
        return x_medio, y_medio   
    def colisiona_con_punto(self, x, y):
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = self.coordenadas_escaladas()
        x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado = self.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)

        area_total = area(x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado)
        area1 = area(x, y, x2_rotado, y2_rotado, x3_rotado, y3_rotado)
        area2 = area(x1_rotado, y1_rotado, x, y, x3_rotado, y3_rotado)
        area3 = area(x1_rotado, y1_rotado, x2_rotado, y2_rotado, x, y)
        return abs(area_total - (area1 + area2 + area3)) < 0.1
    def trasladar(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy
    def imprimir_atributos(self):
        super().imprimir_atributos()
    def colorear(self, canvas):
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = self.coordenadas_escaladas()
        semilla_x, semilla_y = Triangulo.punto_medio_triangulo(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)
        flood_fill_puntos(canvas, round(semilla_x/10)*10, round(semilla_y/10)*10, self.color)#cambio
class Circunferencia(Figura):
    def __init__(self, x, y, radio, color='yellow', grosor=1, tipo_linea='solid'):
        super().__init__(x, y, color, grosor, tipo_linea)
        self.radio = radio
    def colisiona_con_punto(self, x, y):
        distancia_centro = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distancia_centro <= self.radio * self.escala
    def imprimir_atributos(self):
        super().imprimir_atributos()
        print(f"Radio: {self.radio}")
    def colorear(self, canvas):
        flood_fill_puntos(canvas, self.x, self.y, self.color)
class FigurasCanvas(tk.Canvas):
    # def borrar_figura(self, figura):
    #     if figura is not None:
    #         items = self.find_all()
    #         for item in items:
    #             if self.gettags(item) == (str(id(figura)),):
    #                 self.delete(item)
    def borrar_figura(self, figura):
        if figura is not None:
            self.delete(figura.id)
    def obtener_color_pixel(self, x, y):
    # Encuentra los elementos en la coordenada (x, y)
        elementos = self.find_overlapping(x, y, x+1, y+1)

        # Si hay elementos en la coordenada
        if elementos:
            # Obtén el color del fondo del Canvas
            color_fondo = self["bg"]
            
            # Itera sobre los elementos superpuestos
            for elemento in elementos:
                color = self.itemcget(elemento, "fill")
                
                # Si el color del elemento es diferente al fondo, devuélvelo
                if color != color_fondo:
                    return color

        # Si no se encontró un elemento con color diferente al fondo, devuelve None
        return None
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.figuras = []
        self.figura_seleccionada = None
        self.bind("<Button-1>", self.on_click_izquierdo)
        self.bind("<B1-Motion>", self.on_arrastre_izquierdo)
        self.bind("<ButtonRelease-1>", self.on_suelta_izquierdo)
        self.estado = "dibujar"
        self.figura_actual = "cuadrado"
          
    def dibujar_figura(self, figura):
        escala = figura.escala
        if isinstance(figura, Cuadrado):
            # x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = figura.coordenadas_escaladas()
            # x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = figura.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

            # # Dibuja las líneas del cuadrado con las coordenadas rotadas
            # puntos_linea1 = bresenham(x1_rotado, y1_rotado, x2_rotado, y2_rotado)
            # puntos_linea2 = bresenham(x2_rotado, y2_rotado, x3_rotado, y3_rotado)
            # puntos_linea3 = bresenham(x3_rotado, y3_rotado, x4_rotado, y4_rotado)
            # puntos_linea4 = bresenham(x4_rotado, y4_rotado, x1_rotado, y1_rotado)
            # for punto in puntos_linea1 + puntos_linea2 + puntos_linea3 + puntos_linea4:
            #     x, y = punto
            #     self.create_rectangle(x, y, x+10, y+10, width=1, outline="Black", fill="Ghostwhite")
            # figura.colorear(self)
            #...................
            x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado = figura.coordenadas_escaladas()
            x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado, x4_rotado, y4_rotado = figura.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado, x4_escalado, y4_escalado)

            # Dibuja las líneas del cuadrado con las coordenadas rotadas
            puntos_linea1 = bresenham(x1_rotado, y1_rotado, x2_rotado, y2_rotado, line_style=figura.tipo_linea)
            puntos_linea2 = bresenham(x2_rotado, y2_rotado, x3_rotado, y3_rotado, line_style=figura.tipo_linea)
            puntos_linea3 = bresenham(x3_rotado, y3_rotado, x4_rotado, y4_rotado, line_style=figura.tipo_linea)
            puntos_linea4 = bresenham(x4_rotado, y4_rotado, x1_rotado, y1_rotado, line_style=figura.tipo_linea)
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3 + puntos_linea4:
                x, y, color = punto
                self.create_rectangle(x, y, x+10, y+10, width=1, outline=color, fill=color)
            figura.colorear(self)
        elif isinstance(figura, Circunferencia):
            radio  = (round(figura.radio * escala/10)*10)
            puntos_circunferencia = punto_medio(figura.x, figura.y, radio)
            for punto in puntos_circunferencia:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width=1,outline="Black",fill="black")
            figura.colorear(self)
        elif isinstance(figura, Triangulo):
            x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = figura.coordenadas_escaladas()
            x1_rotado, y1_rotado, x2_rotado, y2_rotado, x3_rotado, y3_rotado = figura.puntos_rotados(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)

            # Dibuja las líneas del triángulo con las coordenadas rotadas
            puntos_linea1 = bresenham(x1_rotado, y1_rotado, x2_rotado, y2_rotado, line_style=figura.tipo_linea)
            puntos_linea2 = bresenham(x2_rotado, y2_rotado, x3_rotado, y3_rotado, line_style=figura.tipo_linea)
            puntos_linea3 = bresenham(x3_rotado, y3_rotado, x1_rotado, y1_rotado, line_style=figura.tipo_linea)
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3:
                x, y, color = punto
                self.create_rectangle(x, y, x+10, y+10, width=1, outline=color, fill=color)
            figura.colorear(self)
            
            
        # self.dibujar_segundo_borde(figura, "Black", 0)

    
    # def dibujar_segundo_borde(self, figura, color, grosor):
    #     escala = figura.escala

    #     if isinstance(figura, Cuadrado):
    #         lado = (round(figura.lado * escala/10)*10)
    #         puntos_linea1 = bresenham(figura.x, figura.y, figura.x + lado, figura.y)
    #         puntos_linea2 = bresenham(figura.x, figura.y, figura.x, figura.y + lado)
    #         puntos_linea3 = bresenham(figura.x + lado, figura.y, figura.x + lado, figura.y + lado)
    #         puntos_linea4 = bresenham(figura.x, figura.y + lado, figura.x + lado, figura.y + lado)
    #         for punto in puntos_linea1 + puntos_linea2 + puntos_linea3 + puntos_linea4:
    #             x, y = punto
    #             self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
            
    #     elif isinstance(figura, Circunferencia):
    #         radio  = (round(figura.radio * escala/10)*10)
    #         puntos_circunferencia = punto_medio(figura.x, figura.y, radio)
    #         for punto in puntos_circunferencia:
    #             x, y = punto
    #             self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
            
        # elif isinstance(figura, Triangulo):
        #     x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = figura.coordenadas_escaladas()
            
        #     puntos_linea1 = bresenham(x1_escalado, y1_escalado, x2_escalado, y2_escalado)
        #     puntos_linea2 = bresenham(x2_escalado, y2_escalado, x3_escalado, y3_escalado)
        #     puntos_linea3 = bresenham(x3_escalado, y3_escalado, x1_escalado, y1_escalado)
        #     for punto in puntos_linea1 + puntos_linea2 + puntos_linea3:
        #         x, y = punto
        #         self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
    def get_pixel_color(self, x, y):
        items = self.find_overlapping(x, y, x, y)
        if items:
            return self.itemcget(items[0], "fill")
        else:
            return None

    def set_pixel_color(self, x, y, color):
        self.itemconfig(self.find_closest(x, y), fill=color)

    def in_bounds(self, x, y):
        return 0 <= x < self.winfo_width() and 0 <= y < self.winfo_height()
    
    # Las funciones agregar_cuadrado, agregar_circulo y agregar_triangulo deben estar al mismo nivel que dibujar_figura, no dentro de la función __init__
    def agregar_cuadrado(self, x, y):
        lado = 90
        x1, y1 = x, y
        x2, y2 = x + lado, y
        x3, y3 = x + lado, y + lado
        x4, y4 = x, y + lado
        figura = Cuadrado(x1, y1, x2, y2, x3, y3, x4, y4, color="Blue", grosor=2, tipo_linea="solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
        
    def agregar_circulo(self, x, y):
        figura = Circunferencia(x, y, 45, "Yellow", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)

    def agregar_triangulo(self, x, y):
        figura = Triangulo(x - 50, y + 80, x, y-10, x + 50, y + 80, "Green", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
        
    def on_click_izquierdo(self, event):
        x, y = (round(event.x/10)*10), (round(event.y/10)*10)
        # x, y = event.x, event.y
         
        
        if self.estado == "dibujar":
            if self.figura_actual == "cuadrado":
                self.agregar_cuadrado(x, y)
            elif self.figura_actual == "circulo":
                self.agregar_circulo(x, y)
            elif self.figura_actual == "triangulo":
                self.agregar_triangulo(x, y)
        elif self.estado == "mover":
            self.seleccionar_figura(x, y)
        print("Color del píxel en ({}, {}): {}".format(x, y, self.obtener_color_pixel(x, y)))
        # print("Color del píxel en ({}, {}): {}".format(x, y, self.get_pixel_color(self, x, y)))
        

    def on_arrastre_izquierdo(self, event):
        if self.estado == "mover" and self.figura_seleccionada is not None:
            if not hasattr(self, 'prev_x'):
                self.prev_x = event.x
                self.prev_y = event.y
            # dx = event.x - self.prev_x
            # dy = event.y - self.prev_y
            dx = round((event.x - self.prev_x) / 10) * 10
            dy = round((event.y - self.prev_y) / 10) * 10   
            self.prev_x = event.x
            self.prev_y = event.y
            if isinstance(self.figura_seleccionada, Triangulo):
                self.figura_seleccionada.x1 += dx
                self.figura_seleccionada.y1 += dy
                self.figura_seleccionada.x2 += dx
                self.figura_seleccionada.y2 += dy
                self.figura_seleccionada.x3 += dx
                self.figura_seleccionada.y3 += dy
            else:
                self.figura_seleccionada.trasladar(dx, dy)
            # self.borrar_figura(self.figura_seleccionada)
            # self.dibujar_figura(self.figura_seleccionada)
            
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
    def on_suelta_izquierdo(self, event):
        if hasattr(self, 'prev_x'):
            del self.prev_x
            del self.prev_y
    
    def seleccionar_figura(self, x, y):
        self.figura_seleccionada = None
        for figura in self.figuras:
            if figura.colisiona_con_punto(x, y):
                figura.borde_seleccionado = not figura.borde_seleccionado
                self.figura_seleccionada = figura
                break
    def borrar_figura_seleccionada(self):
        if self.figura_seleccionada is not None:
            self.figuras.remove(self.figura_seleccionada)
            self.figura_seleccionada = None
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
    def cambiar_color_figura_seleccionada(self, event):
        if self.canvas.figura_seleccionada is not None:
            color_seleccionado = self.color_var.get()
            colores = {'Negro': 'black', 'Rojo': 'red', 'Verde': 'green', 'Azul': 'blue', 'Amarillo': 'yellow', 'Naranja': 'orange', 'Morado': 'purple'}
            self.canvas.figura_seleccionada.cambiar_color(colores[color_seleccionado])
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)
                
    def cambiar_color_seleccionado(self, color):
        if self.figura_seleccionada is not None:
            # Cambie el atributo color de la figura seleccionada
            self.figura_seleccionada.cambiar_color(color)
            self.figura_seleccionada.imprimir_atributos()
            # self.borrar_figura(self.figura_seleccionada)
            # self.dibujar_figura(self.figura_seleccionada)
            
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
    def mover_figura(self, dx, dy):
        figura = self.figura_seleccionada
        if isinstance(figura, Triangulo):
            figura.x1 += dx
            figura.y1 += dy
            figura.x2 += dx
            figura.y2 += dy
            figura.x3 += dx
            figura.y3 += dy
        else:
            figura.trasladar(dx, dy)

        self.delete("all")
        for fig in self.figuras:
            self.dibujar_figura(fig) 
    def escalar_figura(self, factor):
        if self.figura_seleccionada is not None:
            self.figura_seleccionada.escalar(factor)
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)   
    def rotar_figura(self, rotacion):
        if self.figura_seleccionada is not None:
            self.figura_seleccionada.rotar(rotacion)
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)         
                       
class Aplicacion(tk.Tk):
    def __init__(self):
        # bg1 = "#67747f"
        bg1 = "#171c3b"
        col2 = "#787c9f"
        fgc = "#e9eeee"
        # d9dee2
        super().__init__()
        self.title("Dibujo de figuras geométricas")
        self.configure(bg="#d9dee2")
        self.canvas = FigurasCanvas(self, width=800, height=600)
        self.canvas.configure(bg="#dde0ef", highlightthickness=0)
        self.canvas.pack()

        self.frame_controles = tk.Frame(self)
        self.frame_controles.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_controles.configure(bg=bg1)
        
        self.frame_figura = tk.Frame(self.frame_controles)
        self.frame_figura.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_figura.configure(bg=bg1)

        self.figura_var = tk.StringVar()
        self.seleccion_figura = ttk.Combobox(self.frame_figura, textvariable=self.figura_var, state='readonly',width=20)
        self.seleccion_figura['values'] = ('Cuadrado', 'Círculo', 'Triángulo')
        self.seleccion_figura.current(0)
        self.seleccion_figura.grid(row=1, column=0, columnspan=2, padx=0, pady=5, sticky="W")
        self.seleccion_figura.bind("<<ComboboxSelected>>", self.actualizar_figura_actual)

        
        self.boton_dibujar = tk.Button(self.frame_figura, text="Dibujar", font=("Arial", 8, "bold"), command=self.dibujar, width=8)
        self.boton_dibujar.grid(row=2, column=0, padx=0, pady=5, sticky="W")
        self.boton_dibujar.configure(bg=col2)
        self.boton_dibujar.configure(fg="white")
        
        self.boton_mover = tk.Button(self.frame_figura, text="Seleccionar", font=("Arial", 8, "bold"), command=self.mover, width=10)
        self.boton_mover.grid(row=2, column=1, padx=0, pady=5, sticky="W")
        self.boton_mover.configure(bg=col2)
        self.boton_mover.configure(fg="white")
        
        self.frame_color = tk.Frame(self.frame_controles)
        self.frame_color.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_color.configure(bg=bg1)

        self.label_color = tk.Label(self.frame_color, text="Color de Figura", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        self.label_color.grid(row=2, column=0, sticky="W", padx=5, pady=7)
        self.label_color.configure(bg=bg1)
        
        
        
        
        self.color_var = tk.StringVar()
        self.seleccion_color = ttk.Combobox(self.frame_color, textvariable=self.color_var, state='readonly', width=14)
        self.seleccion_color['values'] = ('Black', 'Red', 'Green', 'Blue', 'Yellow', 'Orange')
        self.seleccion_color.current(0)
        self.seleccion_color.grid(row=1, column=0, sticky="W", padx=5, pady=0)
        self.seleccion_color.bind("<<ComboboxSelected>>", self.cambiar_color_figura_seleccionada)
        #_______________________
        #_______________________
        
        
        
        self.frame_escala = tk.Frame(self.frame_controles)
        self.frame_escala.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_escala.configure(bg=bg1)
        
        self.label_escala = tk.Label(self.frame_escala, text="Tamaño", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2 )
        self.label_escala.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.label_escala.configure(bg=bg1)
        
        self.boton_aumentar = tk.Button(self.frame_escala, text="+", command=self.aumentar_escala, width=4, height=1)
        self.boton_aumentar.grid(row=1, column=1, padx=0, pady=2)
        self.boton_aumentar.configure(bg="#d14c69")
        self.boton_aumentar.configure(fg="White")
        
        self.boton_disminuir = tk.Button(self.frame_escala, text="-",command=self.disminuir_escala, width=4, height=1)
        self.boton_disminuir.grid(row=1, column=0, padx=0, pady=0)
        self.boton_disminuir.configure(bg="#d14c69")
        self.boton_disminuir.configure(fg="White")

        self.frame_movimiento = tk.Frame(self.frame_controles)
        self.frame_movimiento.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_movimiento.configure(bg=bg1)
        
        self.frame_rotacion = tk.Frame(self.frame_controles)
        self.frame_rotacion.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_rotacion.configure(bg=bg1)

        self.label_rotacion = tk.Label(self.frame_rotacion, text="Rotación", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        self.label_rotacion.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.label_rotacion.configure(bg=bg1)

        self.boton_rotar_horario = tk.Button(self.frame_rotacion, text="⇨", command=self.rotar_horario, width=4, height=1)
        self.boton_rotar_horario.grid(row=1, column=1, padx=0, pady=2)
        self.boton_rotar_horario.configure(bg="#5979f7")
        self.boton_rotar_horario.configure(fg="White")
        self.boton_rotar_antihorario = tk.Button(self.frame_rotacion, text="⇦", command=self.rotar_antihorario, width=4, height=1)
        self.boton_rotar_antihorario.grid(row=1, column=0, padx=0, pady=0)
        self.boton_rotar_antihorario.configure(bg="#5979f7")
        self.boton_rotar_antihorario.configure(fg="White")
        
        self.boton_arriba = tk.Button(self.frame_movimiento, text="↑", command=self.mover_arriba, width=4, height=1)
        self.boton_arriba.grid(row=0, column=1)
        self.boton_arriba.configure(bg="#6637ef")
        self.boton_arriba.configure(fg="White")
        self.boton_abajo = tk.Button(self.frame_movimiento, text="↓", command=self.mover_abajo, width=4, height=1)
        self.boton_abajo.grid(row=1, column=1)
        self.boton_abajo.configure(bg="#6637ef")
        self.boton_abajo.configure(fg="White")        
        self.boton_izquierda = tk.Button(self.frame_movimiento, text="←", command=self.mover_izquierda, width=4, height=1)
        self.boton_izquierda.grid(row=1, column=0)
        self.boton_izquierda.configure(bg="#6637ef")
        self.boton_izquierda.configure(fg="White")
        self.boton_derecha = tk.Button(self.frame_movimiento, text="→", command=self.mover_derecha, width=4, height=1)
        self.boton_derecha.grid(row=1, column=2)
        self.boton_derecha.configure(bg="#6637ef")
        self.boton_derecha.configure(fg="White")
        
        self.frame_linea = tk.Frame(self.frame_controles)
        self.frame_linea.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_linea.configure(bg=bg1)

        # self.label_linea = tk.Label(self.frame_linea, text="Tipo de línea", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        # self.label_linea.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        # self.label_linea.configure(bg=bg1)

        self.boton_solido = tk.Button(self.frame_linea, text="Sólido",font=("Arial", 8, "bold"), command=self.cambiar_a_solido, width=11, height=1)
        self.boton_solido.grid(row=0, column=0, padx=0, pady=2)
        self.boton_solido.configure(bg=col2)
        self.boton_solido.configure(fg="White")
        self.boton_segmentado = tk.Button(self.frame_linea, text="Segmentado",font=("Arial", 8, "bold"), command=self.cambiar_a_segmentado, width=11, height=1)
        self.boton_segmentado.grid(row=1, column=0, padx=0, pady=2)
        self.boton_segmentado.configure(bg=col2)
        self.boton_segmentado.configure(fg="White")
        
        
        self.boton_borrar = tk.Button(self.frame_controles, text="Borrar",font=("Arial", 8, "bold"), command=self.borrar, width=6, height=2)
        self.boton_borrar.pack(side=tk.LEFT, padx=5)
        self.boton_borrar.configure(bg=col2)
        self.boton_borrar.configure(fg="White")
        #########
        

        
        
                                
             
    def dibujar(self):
        self.canvas.estado = "dibujar"
        self.actualizar_botones()
        
    def aumentar_escala(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.escalar_figura(fig.get_escala()+0.4)

    def disminuir_escala(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.escalar_figura(fig.get_escala()-0.4)
    
    def rotar_horario(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.rotar_figura(fig.get_rotacion() + 15)

    def rotar_antihorario(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.rotar_figura(fig.get_rotacion() - 15)            
                
    def escalar(self):
        if self.canvas.figura_seleccionada is not None:
            try:
                factor = float(self.escala_var.get())
                self.canvas.figura_seleccionada.escalar(factor)
                self.canvas.delete("all")
                for figura in self.canvas.figuras:
                    self.canvas.dibujar_figura(figura)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor numérico válido.")
    
    
    def cambiar_a_solido(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            fig.tipo_linea = 'solid'
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)

    def cambiar_a_segmentado(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            fig.tipo_linea = 'dashed'
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)
        
    
    
    
    def mover_arriba(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(0, -80)

    def mover_abajo(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(0, 80)

    def mover_izquierda(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(-80, 0)

    def mover_derecha(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(80, 0)

    
    
    
    
    def mover(self):
        self.canvas.estado = "mover"
        self.actualizar_botones()
    def actualizar_botones(self):
        if self.canvas.estado == "dibujar":
            self.boton_dibujar.config(bg="#3d3f51", relief=tk.SUNKEN)  # Botón presionado
            self.boton_mover.config(bg="#787c9f", relief=tk.RAISED)  # Botón no presionado
        elif self.canvas.estado == "mover":
            self.boton_dibujar.config(bg="#787c9f", relief=tk.RAISED)  # Botón no presionado
            self.boton_mover.config(bg="#3d3f51", relief=tk.SUNKEN)  # Botón presionado
    def borrar(self):
        self.canvas.borrar_figura_seleccionada()
    
    # Agregar la función actualizar_figura_actual para manejar la selección de figura
    def actualizar_figura_actual(self, event):
        figura_seleccionada = self.figura_var.get()
        if figura_seleccionada == "Cuadrado":
            self.canvas.figura_actual = "cuadrado"
        elif figura_seleccionada == "Círculo":
            self.canvas.figura_actual = "circulo"
        elif figura_seleccionada == "Triángulo":
            self.canvas.figura_actual = "triangulo"
    def cambiar_color_figura_seleccionada(self, event):
        color_seleccionado = self.color_var.get()#.lower()
        print(color_seleccionado)
        self.canvas.cambiar_color_seleccionado(color_seleccionado)
                       
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
    
    
















