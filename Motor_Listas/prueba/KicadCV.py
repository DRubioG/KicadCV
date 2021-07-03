from KicadList import *
import cv2
import numpy as np 

class KicadCV():
    def __init__(self, file):
        ab=KicadList(file)
        self.linea, self.ruta, self.via=ab.generar_lista()
        self.alto, self.ancho=ab.get_long()
        self.pad=ab.buscar_pads()
        #self.escalax=1
       # self.escalay=1
        self.offsetx=0
        self.offsety=0

    def escalar(self, escala=1, escalax=1, escalay=1):

        self.escalax=escalax
        self.escalay=escalay

        if escala is not None:
            self.escalax=escala
            self.escalay=escala
       # print("escala x", self.escalax)
       # print("escala y", self.escalay)

    def reescalar(self, h, w):
        self.escalay=w/self.alto
        self.escalax=h/self.ancho
        #print("escalax: ", self.escalax)
       # print("escalay: ", self.escalay)
      #  print("escala x ", self.escalax)
      #  print("escalay ", self.escalay)
    
    def offset(self, offset=0, offx=0, offy=0):
        self.offsetx=offx
        self.offsety=offy
        if offset is not 0:
            self.offsetx=offset
            self.offsety=offset


    def pintar_linea(self, img):
        for num_lin in self.linea:
            p1x=round(float(num_lin[0][0])*self.escalax)+self.offsetx
            p1y=round(float(num_lin[0][1])*self.escalay)+self.offsety
            p1=(p1x, p1y)
            p2x=round(float(num_lin[1][0])*self.escalax)+self.offsetx
            p2y=round(float(num_lin[1][1])*self.escalay)+self.offsety
            p2=(p2x, p2y)
            cv2.circle(img, p1,7, (255,119, 0))
            cv2.line(img, p1, p2, (0,255,255), 1)
    
    def pintar_ruta(self, img, esc=1, offx=0, offy=0):
        for num_rut in self.ruta:
            p1x=round(float(num_rut[0][0])*self.escalax)+self.offsetx
            p1y=round(float(num_rut[0][1])*self.escalay)+self.offsety
            p1=(p1x, p1y)
            p2x=round(float(num_rut[1][0])*self.escalax)+self.offsetx
            p2y=round(float(num_rut[1][1])*self.escalay)+self.offsety
            p2=(p2x, p2y)
            if num_rut[2]=="F.Cu":
                color=(0,0,255)
            elif num_rut[2]=="B.Cu":
                color=(255,0,0)
            cv2.line(img, p1, p2, color, 2)

    def pintar_via(self, img, esc=1, offx=0, offy=0):
        for num_via in self.via:
            px=round(float(num_via[0][0])*self.escalax)+self.offsetx
            py=round(float(num_via[0][1])*self.escalay)+self.offsety
            p=(px, py)
            size=round(float(num_via[3])*self.escalax)
            drill=round(float(num_via[4])*self.escalax)
            radio=round((size+drill)/2)
            radio_int=round((size/2))
            width=size-radio
            cv2.circle(img, p, radio_int, (0,255,255), radio)
            cv2.circle(img, p, radio, (0,0,0), width)

    def pintar_pad(self, img):
        def thru_hole(img, pos, size, drill):
            px=round(pos[0]*self.escalax)+self.offsetx
            py=round(pos[1]*self.escalay)+self.offsety
            p=(px,py)
            size=round(float(size[0])*self.escalax)
            drill=round(float(drill)*self.escalax)
            radio=round((size+drill)/2)
            radio_int=round((size/2))
            width=size-radio
            cv2.circle(img, p, radio, (0,255,255), width)
            cv2.circle(img, p, radio_int, (0,0,0), -1)

        def smd(img, tipo, pos, size, capa):
            color=(0,0,0)
            px=round(pos[0]*self.escalax)+self.offsetx
            py=round(pos[1]*self.escalay)+self.offsety
            p=(px,py)
            if 'F.Cu' in capa:
                color=(0,0,255)
            elif 'B.Cu' in capa:
                color=(255,0,0)
            if tipo == 'circle':
                size=round(float(size[0])*self.escalax)
                cv2.circle(img, p, size, color, -1)
            elif tipo=='rect':
                sizex=round(float(size[0])*self.escalax)
                sizey=round(float(size[1])*self.escalay)
                size=(sizex, sizey)
                p_rect_x=px-round(sizex/2)
                p_rect_y=py-round(sizey/2)
                p_rect=(p_rect_x, p_rect_y)
                tam=(p_rect_x+sizex, p_rect_y+sizey)
                cv2.rectangle(img, p_rect, tam, color, -1)
            elif tipo=='roundrect':
                sizex=round(float(size[0])*self.escalax)
                sizey=round(float(size[1])*self.escalay)
                size=(sizex, sizey)
                p_rect_x=px-round(sizex/2)
                p_rect_y=py-round(sizey/2)
                p_rect=(p_rect_x, p_rect_y)
                tam=(p_rect_x+sizex, p_rect_y+sizey)
                cv2.rectangle(img, p_rect, tam, color, -1)
            
        for module in self.pad:
            for pad in module:
               # print(pad)
                if pad[1] == 'thru_hole':
                    thru_hole(img, pad[3], pad[5], pad[6])
                elif pad[1] == 'smd':
                    smd(img, pad[2], pad[3], pad[5], pad[7])


                    

    def localizar_PCB(self, img, tamx=1200, tamy=800, thres=140, areaMin=9000, areaMax=900000, blur=15):
        contornos_forma=[]
        img=cv2.resize(img, (tamx,tamy))
        imgray=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        im_gauss = cv2.GaussianBlur(imgray, (blur, blur), 0)
        ret, imgthreshold=cv2.threshold(im_gauss, thres, 255, cv2.THRESH_BINARY)
        cv2.imshow("threshold", imgthreshold)
   #     print("ret ", ret)
        if ret==0:
            return "error", 0,0,0,0
   #     imgthreshold = cv2.adaptiveThreshold(im_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 3)
        x, y, h, w=0,0,0,0
        cv2.rectangle(imgthreshold, (1,1), (tamx-1,tamy-1), (0,0,0),3)
        contours, hierarchy = cv2.findContours(imgthreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for con in contours:
            area =cv2.contourArea(con)
            if areaMin < area < areaMax:
                x, y, h, w = cv2.boundingRect(con)
                contornos_forma.append(con)
        return img, x, y, h, w 


if __name__=="__main__":
    cap=cv2.VideoCapture(1)
    a=KicadCV('prueba.kicad_pcb')
    #img=cv2.imread("pruebas/p1.jpg")
    #img, x, y, h, w=a.localizar_PCB(img)
   # a.offset(offx=x, offy=y)
   # a.reescalar(h, w)
   # a.pintar_linea(img)
   # a.pintar_ruta(img)
   # a.pintar_via(img)
   # a.pintar_pad(img)
   # cv2.imshow("prueba", img)
   # cv2.imshow("threshold2", imgthreshold)
    
    #cv2.waitKey(0)
    #a.escala(3)
    #a.offset(50)
    #_, tam=cap.read()
    #print(tam.shape[0])
    #a.offset(offx=round(float(tam.shape[0]/2)), offy=round(float(tam.shape[1]/2)))
    #blanco=np.ones((700,1000,3),dtype=np.uint8)
    while True:
        ret, imagen=cap.read()
        if ret==False:
            print("ERROR")
            break
        img, x, y, h, w=a.localizar_PCB(imagen)
        if img!="Error":
            a.offset(offx=x, offy=y)
            a.reescalar(h, w)
            a.pintar_linea(img)
            a.pintar_ruta(img)
            a.pintar_via(img)
            a.pintar_pad(img)

        cv2.imshow("prueba", img)
        tec=cv2.waitKey(100)
        if tec==27:
            break

    cap.release()
    cv2.destroyAllWindows()