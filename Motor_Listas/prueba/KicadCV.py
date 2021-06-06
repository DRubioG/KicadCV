from KicadList import *
import cv2
import numpy as np 
class KicadCV():
    def __init__(self, file):
        a=KicadList(file)
        self.linea, self.ruta, self.via=a.generar_lista()

    def pintar_linea(self, img):
        for num_lin in self.linea:
            p1x=round(float(num_lin[0][0]))*5
            p1y=round(float(num_lin[0][1]))*5
            p1=(p1x, p1y)
            p2x=round(float(num_lin[1][0]))*5
            p2y=round(float(num_lin[1][1]))*5
            p2=(p2x, p2y)
            print("p1: ", p1)
            print("p2: ", p2)
            cv2.line(img, p1, p2, (0,255,255), 1)
    
    def pintar_ruta(self, img):
        for num_rut in self.ruta:
            p1x=round(float(num_rut[0][0]))*5
            p1y=round(float(num_rut[0][1]))*5
            p1=(p1x, p1y)
            p2x=round(float(num_rut[1][0]))*5
            p2y=round(float(num_rut[1][1]))*5
            p2=(p2x, p2y)
            print("p1: ", p1)
            print("p2: ", p2)
            if num_rut[2]=="F.Cu":
                color=(0,0,255)
            elif num_rut[2]=="B.Cu":
                color=(255,0,0)
            cv2.line(img, p1, p2, color, 2)


if __name__=="__main__":
    a=KicadCV('prueba.kicad_pcb')
    blanco=np.ones((700,1000,3),dtype=np.uint8)
    a.pintar_linea(blanco)
    a.pintar_ruta(blanco)
    cv2.imshow("prueba", blanco)
    cv2.waitKey()