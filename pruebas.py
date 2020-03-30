"""import random
def unico(x,L):
  esUnico=True
  for i in range(len(L)):
    if x==L[i]:
      esUnico=False
      break
  return esUnico
L=[]
j=0
suma = 0
while j<100:
  x=random.randint(1,100)
  if unico(x,L):
    suma += x
    if x == 17 or x ==35 or x ==53 or x ==71 or x ==85 or x ==89 or x ==100:
        print(j,".- "," Suma = ",suma, " GANADOR ")
    else:
        print(j,".- "," Suma = ",suma)
    L.append(x)
    j+=1"""

class Person:
  def __init__(self,nombre,edad):
    self.nombre = nombre
    self.edad = edad

  def imprimir(self):
    print("Nombre: ",self.nombre," - Edad: ",self.edad)

class Empleado(Person):
  def __init__(self,trabajo):
    super(Empleado,self).__init__(self)
    

