from KicadList import *
import cv2
import numpy as np 

class KicadCV():
    def __init__(self, file):
        a=KicadList(file)
        self.linea, self.ruta, self.via=a.generar_lista()
        self.escala=1
        self.offsetx=0
        self.offsety=0

    def escala(self, escala=1):
        self.escala=escala
    
    def offset(self, offset=0, offx=0, offy=0):
        self.offsetx=offx
        self.offsety=offy
        if offset is not 0:
            self.offsetx=offset
            self.offsety=offset


    def pintar_linea(self, img):
        for num_lin in self.linea:
            p1x=round(float(num_lin[0][0]))*self.escala+self.offsetx
            p1y=round(float(num_lin[0][1]))*self.escala+self.offsety
            p1=(p1x, p1y)
            p2x=round(float(num_lin[1][0]))*self.escala+self.offsetx
            p2y=round(float(num_lin[1][1]))*self.escala+self.offsety
            p2=(p2x, p2y)
            cv2.line(img, p1, p2, (0,255,255), 1)
    
    def pintar_ruta(self, img, esc=1, offx=0, offy=0):
        for num_rut in self.ruta:
            p1x=round(float(num_rut[0][0]))*self.escala+self.offsetx
            p1y=round(float(num_rut[0][1]))*self.escala+self.offsety
            p1=(p1x, p1y)
            p2x=round(float(num_rut[1][0]))*self.escala+self.offsetx
            p2y=round(float(num_rut[1][1]))*self.escala+self.offsety
            p2=(p2x, p2y)
            if num_rut[2]=="F.Cu":
                color=(0,0,255)
            elif num_rut[2]=="B.Cu":
                color=(255,0,0)
            cv2.line(img, p1, p2, color, 2)


if __name__=="__main__":
    cap=cv2.VideoCapture(0)
    a=KicadCV('prueba.kicad_pcb')
    #a.escala(3)
    #a.offset(50)
    _, tam=cap.read()
    #print(tam.shape[0])
    a.offset(offx=round(float(tam.shape[0]/2)), offy=round(float(tam.shape[1]/2)))
    #blanco=np.ones((700,1000,3),dtype=np.uint8)
    while True:
        ret, image=cap.read()
        a.pintar_linea(image)
        a.pintar_ruta(image)
        cv2.imshow("prueba", image)
        tec=cv2.waitKey(1)
        if tec==27:
            break

    cap.release()
    cv2.destroyAllWindows()