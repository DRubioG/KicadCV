class KicadList():
    def __init__(self, file):
        self.f=open(file, 'r')
        self.mensaje=self.f.readlines()
        self.linea=[]
        self.ruta=[]
        self.via=[]
       # def veriable(ent):
        #    for sus in range(len(palabras)):
         #       print(sus, ":", palabras[sus])

    def buscar_linea(self, cadena, palabras):
        if cadena.find("gr_line ") != -1:
            p1x=palabras[6]
            p1y=palabras[7]
            p2x=palabras[11]
            p2y=palabras[12]
            capa=palabras[16]
            ancho=palabras[20]
            self.linea.append([(p1x, p1y), (p2x, p2y), ancho, capa])
            
    def buscar_segment(self, cadena, palabras):
        if cadena.find("segment ")!=-1:
            p1x=palabras[6]
            p1y=palabras[7]
            p2x=palabras[11]
            p2y=palabras[12]
            capa=palabras[16]
            ancho=palabras[20]
            red=palabras[24]
            self.ruta.append([(p1x, p1y), (p2x, p2y), ancho, capa, red])
            
    def buscar_via(self, cadena, palabras):
        if cadena.find("via ")!=-1:
            p1x=palabras[6]
            p1y=palabras[7]
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
            self.buscar_linea(cadena, palabras)
            self.buscar_segment(cadena, palabras)
            self.buscar_via(cadena, palabras)
        self.f.close()
        return self.linea, self.ruta, self.via
    
#if __name__=="__main__":
 #   a=KicadList('prueba.kicad_pcb')
  #  a.generar_lista()