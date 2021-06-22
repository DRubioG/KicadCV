import math

class KicadList():
    def __init__(self, file):
        self.f=open(file, 'r')
        self.mensaje=self.f.readlines()
        self.linea=[]
        self.ruta=[]
        self.via=[]
        self.d=0
        self.origen=(10000,100000)
       # def veriable(ent):
        #    for sus in range(len(palabras)):
         #       print(sus, ":", palabras[sus])
    def buscar_origen(self, cadena, palabras):
        if cadena.find("gr_line") != -1:
            if cadena.find("Edge.Cuts") != -1:
                #print("linea de corte")
                #print("plabras: ", palabras)
                p1x=self.num_natural(palabras[6])
                p1y=self.num_natural(palabras[7])
                p2x=self.num_natural(palabras[11])
                p2y=self.num_natural(palabras[12])
                #longitudes max y min
                def longitud(p1,p2):
                    return math.sqrt((p1[0]-p2[0])**2+((p1[1]-p2[1])**2))
                lon=longitud((p1x,p1y), (p2x, p2y))
                if p1x == p2x:
                    self.alto=lon
                else:
                    self.ancho=lon
                #distancias al origen
                def distancia(x1, y1):
                    return x1**2+y1**2
                d1=distancia(p1x,p1y)
                d2=distancia(p2x, p2y)
                if d1 < d2:
                    origen=(p1x, p1y)
                    d=d1
                else:
                    origen=(p2x,p2y)
                    d=d2

                self.d=distancia(self.origen[0], self.origen[1])
                if d < self.d:
                    self.origen=origen
                   # print("nuevo origen : ", self.origen)
            

    def num_natural(self, numero):
        return round(float(numero))

    def get_long(self):
        return self.alto, self.ancho

    def buscar_linea(self, cadena, palabras):
        if cadena.find("gr_line ") != -1:
            p1x=self.num_natural(palabras[6])-self.origen[0]
            p1y=self.num_natural(palabras[7])-self.origen[1]
            p2x=self.num_natural(palabras[11])-self.origen[0]
            p2y=self.num_natural(palabras[12])-self.origen[1]
            capa=palabras[16]
            ancho=palabras[20]
            self.linea.append([(p1x, p1y), (p2x, p2y), ancho, capa])
           # if capa==""
            
    def buscar_segment(self, cadena, palabras):
        if cadena.find("segment ")!=-1:
            p1x=self.num_natural(palabras[6])-self.origen[0]
            p1y=self.num_natural(palabras[7])-self.origen[1]
            p2x=self.num_natural(palabras[11])-self.origen[0]
            p2y=self.num_natural(palabras[12])-self.origen[1]
            capa=palabras[16]
            ancho=palabras[20]
            red=palabras[24]
            self.ruta.append([(p1x, p1y), (p2x, p2y), ancho, capa, red])
            
    def buscar_via(self, cadena, palabras):
        if cadena.find("via ")!=-1:
            p1x=self.num_natural(palabras[6])-self.origen[0]
            p1y=self.num_natural(palabras[7])-self.origen[1]
            size=palabras[10]
            drill=palabras[15]
            capa1=palabras[19]
            capa2=palabras[20]
            red=palabras[24]
            self.via.append([(p1x, p1y), (capa1, capa2), size, drill, red])
        
    def generar_lista(self):
        for cadena in self.mensaje:
            cadena=cadena.replace("(", " ")
            cadena=cadena.replace(")", " ")
            cadena=cadena.replace("\n", " ")
            palabras=cadena.split(" ", -1)
            self.buscar_origen(cadena, palabras)
            self.buscar_linea(cadena, palabras)
            self.buscar_segment(cadena, palabras)
            self.buscar_via(cadena, palabras)
        self.f.close()
        return self.linea, self.ruta, self.via
    
if __name__=="__main__":
    a=KicadList('prueba.kicad_pcb')
    print("ejeucion")
    a.generar_lista()
    #print(a.linea)