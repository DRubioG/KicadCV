f=open('prueba.kicad_pcb', 'r')
mensaje=f.readlines()
linea=[]
ruta=[]
via=[]
def veriable(ent):
    for sus in range(len(palabras)):
        print(sus, ":", palabras[sus])

for cadena in mensaje:
    cadena=cadena.replace("(", " ")
    cadena=cadena.replace(")", " ")
    cadena=cadena.replace("\n", " ")
    palabras=cadena.split(" ", -1)
    if cadena.find("gr_line ") != -1:
        p1x=palabras[6]
        p1y=palabras[7]
        p2x=palabras[11]
        p2y=palabras[12]
        capa=palabras[16]
        ancho=palabras[20]
        linea.append([(p1x, p1y), (p2x, p2y), ancho, capa])
    
    if cadena.find("segment ")!=-1:
        p1x=palabras[6]
        p1y=palabras[7]
        p2x=palabras[11]
        p2y=palabras[12]
        capa=palabras[16]
        ancho=palabras[20]
        red=palabras[24]
        ruta.append([(p1x, p1y), (p2x, p2y), ancho, capa, red])
    
    if cadena.find("via ")!=-1:
        p1x=palabras[6]
        p1y=palabras[7]
        size=palabras[10]
        drill=palabras[15]
        capa1=palabras[19]
        capa2=palabras[20]
        red=palabras[24]
        via.append([(p1x, p1y), (capa1, capa2), size, drill, red])
print(via)
f.close()
