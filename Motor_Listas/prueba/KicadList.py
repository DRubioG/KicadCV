import math

class KicadList():
    def __init__(self, file):
        self.f=open(file, 'r')
        self.mensaje=self.f.readlines()
        self.linea=[]
        self.ruta=[]
        self.via=[]
        self.module=[]
        self.pad=[]
        self.d=0
        self.cont=0
        self.mod=-1
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
            size=palabras[11]
            drill=palabras[15]
            capa1=palabras[19]
            capa2=palabras[20]
            red=palabras[24]
            self.via.append([(p1x, p1y), (capa1, capa2), size, drill, red])
        
    def buscar_pads(self):
        lis=[]
        reg=[]
        flag=0
        for module in self.module:
            for module2 in module:
                
                if "module" in module2:
                    flag=1
                elif flag==1:
                    flag=0
                    ref_x=float(module2[5])
                    ref_y=float(module2[6])
                    n_origenx=ref_x-self.origen[0]
                    n_origeny=ref_y-self.origen[1]

                
                
                if "pad" in module2:

                    nombre=module2[5]
                    tipo=module2[6]
                    forma=module2[7]
                    
                    pos_x=n_origenx-float(module2[9])
                    pos_y=n_origeny-float(module2[10])
                    
                    pos=(pos_x,pos_y)
                    if module2[11].isnumeric():
                        angulo=module2[11]
                        size_num=13
                    else:
                        angulo=0
                        size_num=12
                    size=(module2[size_num],module2[size_num+1])
                    if "thru_hole" in module2:
                        drill=module2[size_num+3]
                        capa=module2[size_num+5:]
                    else:
                        drill=None
                        capa=module2[size_num+3:]
                    
                    reg.append([nombre, tipo, forma, pos, angulo, size, drill, capa])
                    
                    #print(module2)
            self.pad.append(reg)
            #print(reg)
            reg=[]
           # lis.append(reg)
            #print(reg)
            #reg=[]
            
       # print(self.pad)
        return self.pad

    def generar_lista(self):
        lista=[]
        #palabras2=[]
        palabras=[]
        num=0
        num2=0
        num3=0
        #mod=-1
        c=0
        m=0
        for module in self.mensaje:
            self.cont+=module.count("(")
            self.cont-=module.count(")")
            if self.cont==1: 
                if c!=0:
                    c=0
            elif self.cont==2:
                c=2
            elif self.cont==3:
                c=3
            elif self.cont==4:
                c=4

            if c>1:
                if module.find("module ")!=-1:
                    lista.append([])
                    m=1
                    self.mod+=1
            elif c==0:
                m=0

            if m==1:
                lista[self.mod].append(module)

        for cadena in lista:
            for cadena2 in cadena:
                cadena2=cadena2.replace("(", "")
                cadena2=cadena2.replace("\n", "")
                cadena2=cadena2.replace(")", "")
                cadena2=cadena2.split(" ", -1)
                palabras.append(cadena2)
            self.module.append(palabras)
            palabras=[]

        


        for cadena in self.mensaje:
            cadena=cadena.replace("(", " ")
            cadena=cadena.replace(")", " ")
            cadena=cadena.replace("\n", " ")
            palabras=cadena.split(" ", -1)
            self.buscar_origen(cadena, palabras)
            self.buscar_linea(cadena, palabras)
            self.buscar_segment(cadena, palabras)
            self.buscar_via(cadena, palabras)
        self.buscar_pads()
        self.f.close()
        return self.linea, self.ruta, self.via
    
if __name__=="__main__":
    a=KicadList('prueba.kicad_pcb')
    a.generar_lista()
   # print(a.module_a)