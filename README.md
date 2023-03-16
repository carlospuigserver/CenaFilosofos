

El link de este repositorio es el siguiente: https://github.com/carlospuigserver/CenaFilosofos.git


# Código del campus


```
import time
import random
import threading
import tkinter as tk




N = 5
TIEMPO_TOTAL = 3

class filosofo(threading.Thread):
    semaforo = threading.Lock() #SEMAFORO BINARIO ASEGURA LA EXCLUSION MUTUA
    estado = [] #PARA CONOCER EL ESTADO DE CADA FILOSOFO
    tenedores = [] #ARRAY DE SEMAFOROS PARA SINCRONIZAR ENTRE FILOSOFOS, MUESTRA QUIEN ESTA EN COLA DEL TENEDOR
    count=0

    def __init__(self):
        super().__init__()      #HERENCIA
        self.id=filosofo.count #DESIGNA EL ID AL FILOSOFO
        filosofo.count+=1 #AGREGA UNO A LA CANT DE FILOSOFOS
        filosofo.estado.append('PENSANDO') #EL FILOSOFO ENTRA A LA MESA EN ESTADO PENSANDO
        filosofo.tenedores.append(threading.Semaphore(0)) #AGREGA EL SEMAFORO DE SU TENEDOR( TENEDOR A LA IZQUIERDA)
        print("FILOSOFO {0} - PENSANDO".format(self.id))

    def __del__(self):
        print("FILOSOFO {0} - Se para de la mesa".format(self.id))  #NECESARIO PARA SABER CUANDO TERMINA EL THREAD

    def pensar(self):
        time.sleep(random.randint(0,5)) #CADA FILOSOFO SE TOMA DISTINTO TIEMPO PARA PENSAR, ALEATORIO

    def derecha(self,i):
        return (i-1)%N #BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self,i):
        return(i+1)%N #BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self,i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i]='COMIENDO'
            filosofo.tenedores[i].release()  #SI SUS VECINOS NO ESTAN COMIENDO AUMENTA EL SEMAFORO DEL TENEDOR Y CAMBIA SU ESTADO A COMIENDO

    def tomar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE TOMARA LOS TENEDORES (EXCLUSION MUTUA)
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.verificar(self.id) #VERIFICA SUS VECINOS, SI NO PUEDE COMER NO SE BLOQUEARA EN EL SIGUIENTE ACQUIRE
        filosofo.semaforo.release() #SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        filosofo.tenedores[self.id].acquire() #SOLO SI PODIA TOMARLOS SE BLOQUEARA CON ESTADO COMIENDO

    def soltar(self):
        filosofo.semaforo.acquire() #SEÑALA QUE SOLTARA LOS TENEDORES
        filosofo.estado[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release() #YA TERMINO DE MANIPULAR TENEDORES

    def comer(self):
        print("FILOSOFO {} COMIENDO".format(self.id))
        time.sleep(2) #TIEMPO ARBITRARIO PARA COMER
        print("FILOSOFO {} TERMINO DE COMER".format(self.id))

    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar() #EL FILOSOFO PIENSA
            self.tomar() #AGARRA LOS TENEDORES CORRESPONDIENTES
            self.comer() #COME
            self.soltar() #SUELTA LOS TENEDORES

def main():
    lista=[]
    for i in range(N):
        lista.append(filosofo()) #AGREGA UN FILOSOFO A LA LISTA

    for f in lista:
        f.start() #ES EQUIVALENTE A RUN()

    for f in lista:
        f.join() #BLOQUEA HASTA QUE TERMINA EL THREAD

if __name__=="__main__":
    main()


```








# Código añadiendo tkinter

```
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
        self.estado_label= tk.Label(self.interfaz,text=f"{self.nombre} : {self.estado}")
        self.estado_label.place(x=self.x,y=self.y)
        self.comidas=0
        self.comidas_label= tk.Label(self.interfaz, text=f"Comidas: {self.comidas}")
        self.comidas_label.place(x=self.x+580, y=self.y)

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

class CenaFilosofos:
    def __init__(self):
      self.raiz=tk.Tk()
      self.raiz.geometry("800x600")
      self.raiz.title("Cena de los Filósofos")
      self.palillos= [threading.Lock() for _ in range(5)]
      self.filosofos=[Filosofo("Filósofo"+str(i+1),self.palillos[i],self.palillos[(i+1)%5],self.raiz, 50, 50+50*i) for i in range(5)]
      self.etiquetas_comidas = [tk.Label(self.raiz, text=f"{f.nombre}: 0 comidas") for f in self.filosofos]
      for i, f in enumerate(self.filosofos):
            threading.Thread(target=self.ciclo_vida_filosofo, args=(f, self.etiquetas_comidas[i])).start()
      
      self.raiz.mainloop()

    
    def ciclo_vida_filosofo(self,filosofo,etiqueta_comidas):
      while True:
         filosofo.pensar()
         filosofo.comer()
         comidas=filosofo.comidas
         etiqueta_comidas.config(text=f"{filosofo.nombre}: {comidas} comidas")
         filosofo.estado=f"{comidas} comidas"
         filosofo.estado_label.config(text=f"{filosofo.nombre} : {filosofo.estado}")



if __name__=="__main__":
   CenaFilosofos()
   
   ```



Este código es una implementación del problema clásico de los filósofos, he utilizado hilos y tkinter para poder mostrar el resultado del programa en una ventana gráfica.
Cada filósofo tiene su propia etiqueta que muestra su estado, si están pensando, comieno o intentando obtener un palillo, y también se muestra cuantas veces ha comido cada filósofo. 



Los resultados al ejecutar el código son los siguientes:
<img width="921" alt="filo2" src="https://user-images.githubusercontent.com/91721643/225739484-7ba56ebd-6b9e-41b0-b0a7-245e016351a4.png">


<img width="943" alt="filo3" src="https://user-images.githubusercontent.com/91721643/225739508-7123bb64-f9b9-43e0-8383-2532c9674f14.png">




De esta manera vemos que la etiqueta de estado de cada filósofo se va actualizando constantemente, a su vez que se actualiza y se almacenan las veces que ha comido cada uno.

