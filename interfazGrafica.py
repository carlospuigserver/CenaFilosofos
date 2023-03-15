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

    def pensar(self):
      self.estado="Pensando"
      self.estado_label.config(text=f"{self.nombre} : {self.estado}")
      time.sleep(random.uniform(1,5))


    def intentar_obtener_palillo(self,palillo):
     palillo.acquire()
     self.estado= f"Obtuvo {palillo}"
     self.estado_label.config(text=f"{self.nombre} : {self.estado}")

    def obtener_palillos(self):
       self.estado="Intentando obtener palillo izquierdo"
       self.estado_label.config(text=f"{self.nombre} : {self.estado}")
       self.intentar_obtener_palillo(self.palillo_izquierdo)
       self.estado="Intentando obtener palillo derecho"
       self.estado_label.config(text=f"{self.nombre} : {self.estado}")
       self.intentar_obtener_palillo(self.palillo_derecho)
       self.estado= "Comiendo"
       self.estado_label.config(text=f"{self.nombre} : {self.estado}")

    def comer(self):
       self.obtener_palillos()
       time.sleep(random.uniform(1,5))
       self.palillo_izquierdo.release()
       self.palillo_derecho.release()
       self.estado="Terminó de comer"
       self.estado_label.config(text=f"{self.nombre} : {self.estado}")
       self.comidas+=1
       self.comidas_label.config(text=f"Comidas: {self.comidas}")

    def ciclo_vida(self):
       while True:
          self.pensar()
          self.comer()
          self.estado = f"{self.comidas} Comidas"
          self.estado_label.config(text=f"{self.nombre} : {self.estado}")

    