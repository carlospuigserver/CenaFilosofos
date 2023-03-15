import threading
import time
import random
import tkinter as tk

class Filosofo:
    def __init__(self,nombre,palillo_izquierdo,palillo_derecho,interfaz,x,y):
        self.nombre=nombre
        self.palillo_izquierdo= palillo_izquierdo
        self.palillo_derecho= palillo_derecho
        self.interfaz=interfaz
        self.x= x
        self.y= y
        self.estado= "Pensando"
        self.estado_label= tk.Lable(self.interfaz,text=f"{self.nombre} : {self.estado}")
        self.estado_label.place(x=self.x,y=self.y)
        self.comidas=0
        self.comidas_label= tk.Label(self.interfaz, text=f"Comidas: {self.comidas}")
        self.comidas_label.place(x=self.x+180,y=self.y)