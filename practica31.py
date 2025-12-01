import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Definimos los 8 vértices (x, y, z)
cubo_vertices = (
    (1, -1, -1),  (1, 1, -1),
    (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1),   (1, 1, 1),
    (-1, -1, 1),  (-1, 1, 1)
)

# Definimos las Aristas (conexiones entre índices de vértices)
cubo_aristas = (
    (0,1), (0,3), (0,4), (2,1),
    (2,3), (2,7), (6,3), (6,4),
    (6,7), (5,1), (5,4), (5,7)
)

# Definimos las Caras (grupos de 4 vértices para formar planos)
cubo_caras = (
    (0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6)
)

esfera_vertices = []
esfera_caras = []

def generar_datos_esfera(radio, stacks, sectors):
    global esfera_vertices, esfera_caras
    esfera_vertices = []
    esfera_caras = []

    for i in range(stacks + 1):
        lat = math.pi * (-0.5 + float(i) / stacks) # Latitud
        z = math.sin(lat) * radio
        r_xy = math.cos(lat) * radio # Radio en el plano XY

        for j in range(sectors + 1):
            lng = 2 * math.pi * float(j) / sectors # Longitud
            x = math.cos(lng) * r_xy
            y = math.sin(lng) * r_xy
            esfera_vertices.append((x, y, z))

    for i in range(stacks):
        for j in range(sectors):
            primero = (i * (sectors + 1)) + j
            segundo = primero + sectors + 1
            
            esfera_caras.append((primero, segundo, segundo + 1, primero + 1))

# Generamos la esfera una sola vez al inicio (Radio 1.5, 20 cortes)
generar_datos_esfera(1.5, 20, 20)

def dibujar_cubo():
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.7, 1.0) # Azul Cian
    for cara in cubo_caras:
        for vertice_idx in cara:
            glVertex3fv(cubo_vertices[vertice_idx])
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0) # Negro
    for arista in cubo_aristas:
        for vertice_idx in arista:
            glVertex3fv(cubo_vertices[vertice_idx])
    glEnd()

def dibujar_esfera():
    
    for cara in esfera_caras:
        glBegin(GL_LINE_LOOP) 
        glColor3f(1.0, 0.5, 0.0) # Naranja
        for vertice_idx in cara:
            glVertex3fv(esfera_vertices[vertice_idx])
        glEnd()

def main():
    pygame.init()
    display = (1000, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Practica 1: Cubo y Esfera Paramétrica")

    # Configuración de la Cámara
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10) # Alejar la cámara 10 unidades

    angulo = 0

    while True:
        # Manejo de eventos (Cerrar ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Limpieza de pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # --- DIBUJAR CUBO (Izquierda) ---
        glPushMatrix()           # Guardar estado actual
        glTranslatef(-2.5, 0, 0) # Mover a la izquierda
        glRotatef(angulo, 1, 1, 0) # Rotar sobre eje diagonal
        dibujar_cubo()
        glPopMatrix()            # Restaurar estado

        # --- DIBUJAR ESFERA (Derecha) ---
        glPushMatrix()           # Guardar estado actual
        glTranslatef(2.5, 0, 0)  # Mover a la derecha
        glRotatef(angulo, 0, 1, 0) # Rotar sobre su eje Y
        # Rotamos un poco en X para ver los polos
        glRotatef(45, 1, 0, 0)   
        dibujar_esfera()
        glPopMatrix()            

        
        angulo += 1
        pygame.display.flip()
        pygame.time.wait(10) 

if __name__ == "__main__":
    main()