import tkinter as tk
from tkinter import ttk
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Variables globales para los parámetros del bloque cerámico
largura = 1.0
altura = 1.0
comprimento = 1.0

# Función para dibujar el modelo 3D del bloque cerámico
def draw_block():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

    # Lado frontal
    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)
    glVertex3f(-largura/2, -altura/2, comprimento/2)
    glVertex3f(largura/2, -altura/2, comprimento/2)
    glVertex3f(largura/2, altura/2, comprimento/2)
    glVertex3f(-largura/2, altura/2, comprimento/2)
    glEnd()

    # Otros lados del cubo se dibujan de manera similar...
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0)  # Verde para los otros lados
    # Lado trasero
    glVertex3f(-largura/2, -altura/2, -comprimento/2)
    glVertex3f(largura/2, -altura/2, -comprimento/2)
    glVertex3f(largura/2, altura/2, -comprimento/2)
    glVertex3f(-largura/2, altura/2, -comprimento/2)
    
    # Lado izquierdo
    glVertex3f(-largura/2, -altura/2, -comprimento/2)
    glVertex3f(-largura/2, -altura/2, comprimento/2)
    glVertex3f(-largura/2, altura/2, comprimento/2)
    glVertex3f(-largura/2, altura/2, -comprimento/2)
    
    # Lado derecho
    glVertex3f(largura/2, -altura/2, -comprimento/2)
    glVertex3f(largura/2, -altura/2, comprimento/2)
    glVertex3f(largura/2, altura/2, comprimento/2)
    glVertex3f(largura/2, altura/2, -comprimento/2)
    
    # Lado superior
    glVertex3f(-largura/2, altura/2, -comprimento/2)
    glVertex3f(largura/2, altura/2, -comprimento/2)
    glVertex3f(largura/2, altura/2, comprimento/2)
    glVertex3f(-largura/2, altura/2, comprimento/2)
    
    # Lado inferior
    glVertex3f(-largura/2, -altura/2, -comprimento/2)
    glVertex3f(largura/2, -altura/2, -comprimento/2)
    glVertex3f(largura/2, -altura/2, comprimento/2)
    glVertex3f(-largura/2, -altura/2, comprimento/2)
    glEnd()

    pygame.display.flip()

# Función para actualizar los valores y redibujar el modelo
def update_values():
    global largura, altura, comprimento
    largura = float(entry_largura.get())
    altura = float(entry_altura.get())
    comprimento = float(entry_comprimento.get())

    # Redibujar el bloque con los nuevos valores
    draw_block()

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Modelo Cerámico")

# Frame para los campos de entrada
frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Campos de entrada
ttk.Label(frame, text="Largura do bloco cerâmico (m):").grid(column=1, row=1, sticky=tk.W)
entry_largura = ttk.Entry(frame)
entry_largura.grid(column=2, row=1)
entry_largura.insert(0, "1.0")

ttk.Label(frame, text="Altura do bloco cerâmico (m):").grid(column=1, row=2, sticky=tk.W)
entry_altura = ttk.Entry(frame)
entry_altura.grid(column=2, row=2)
entry_altura.insert(0, "1.0")

ttk.Label(frame, text="Comprimento do bloco cerâmico (m):").grid(column=1, row=3, sticky=tk.W)
entry_comprimento = ttk.Entry(frame)
entry_comprimento.grid(column=2, row=3)
entry_comprimento.insert(0, "1.0")

# Botón para actualizar el modelo
ttk.Button(frame, text="Calcular", command=update_values).grid(column=2, row=4, sticky=tk.W)

# Iniciar Pygame y configurar la ventana OpenGL
pygame.init()
display = (640, 480)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Renderizar el bloque inicial
draw_block()

# Función para mantener actualizadas ambas interfaces
def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                root.destroy()
                return

        # Mantener el loop de Pygame activo
        draw_block()
        pygame.time.wait(10)

        # Mantener el loop de Tkinter activo
        root.update_idletasks()
        root.update()

# Iniciar el loop principal
main_loop()
