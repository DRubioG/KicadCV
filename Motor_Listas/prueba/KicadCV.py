from KicadList import *
import cv2
import numpy as np 

class KicadCV():
    def __init__(self, file):
        ab=KicadList(file)
        self.linea, self.ruta, self.via=ab.generar_lista()
        self.alto, self.ancho=ab.get_long()
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
        print("escala x", self.escalax)
        print("escala y", self.escalay)

    def reescalar(self, h, w):
        self.escalay=w/self.alto
        self.escalax=h/self.ancho
        #print("escalax: ", self.escalax)
       # print("escalay: ", self.escalay)
        print("escala x ", self.escalax)
        print("escalay ", self.escalay)
    
    def offset(self, offset=0, offx=0, offy=0):
        self.offsetx=offx
        self.offsety=offy
        if offset is not 0:
            self.offsetx=offset
            self.offsety=offset


    def pintar_linea(self, img):
        for num_lin in self.linea:
            print(num_lin[0][0] , num_lin[0][1])
            print((float(num_lin[0][0])*self.escalax), (float(num_lin[0][1])*self.escalay))
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


if __name__=="__main__":
    #cap=cv2.VideoCapture(0)
    thres=130
    areaMin = 9000
    areaMax = 900000
    i=0
    blur=15
    contornos_forma=[]
    a=KicadCV('prueba.kicad_pcb')
    img=cv2.imread("pruebas/p1.jpg")
    tamx=1000
    tamy=1000
    img=cv2.resize(img, (tamx,tamy))
    imgray=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    im_gauss = cv2.GaussianBlur(imgray, (blur, blur), 0)
    imgthreshold = cv2.adaptiveThreshold(im_gauss, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 3)
    cv2.rectangle(imgthreshold, (1,1), (tamx-1,tamy-1), (0,0,0),3)
    ret=1
    aream=0
    areas=0
    boundm=0
    if ret !=0:
        contours, hierarchy = cv2.findContours(imgthreshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(img,contornos_forma, -1, (255,0,255), 20)
        #print("pinto y coloreo, contornos: ", len(contours))
        for con in contours:
           
            area =cv2.contourArea(con)
            if area > aream:
                areas=aream
                aream=area
            if areaMin < area < areaMax:
                x, y, h, w = cv2.boundingRect(con)
                if h*w > boundm:
                    boundm=h*w
                cv2.rectangle(img,(x,y),(x+h, y+w), (255,255,0), 1)
                contornos_forma.append(con)
                
                #print("cumplo el minimo, valor ", area)
            #cv2.drawContours(img,con, i, (255,0,255), 3) 
            #cv2.imshow("prueba", img)
            #i+=1
    #print(contornos_forma)
    #cv2.drawContours(img,contornos_forma, -1, (255,0,255), 3)
    print("area maxima: ", aream)
    print("area 2a maxima: ", areas)
    print("bounding maxima: ", boundm)
    print("height: ", h)
    print("width: ", w)
    print("alto: ", a.alto)
    print("ancho: " , a.ancho)
    a.offset(offx=x, offy=y)
    a.reescalar(h, w)
    a.pintar_linea(img)
    a.pintar_ruta(img)
    cv2.imshow("prueba", img)
   # cv2.imshow("threshold2", imgthreshold)
    
    cv2.waitKey(0)
    #a.escala(3)
    #a.offset(50)
    #_, tam=cap.read()
    #print(tam.shape[0])
    #a.offset(offx=round(float(tam.shape[0]/2)), offy=round(float(tam.shape[1]/2)))
    #blanco=np.ones((700,1000,3),dtype=np.uint8)
    #while True:
     #   ret, image=cap.read()
      #  a.pintar_linea(image)
       # a.pintar_ruta(image)
     #   cv2.imshow("prueba", image)
      #  tec=cv2.waitKey(1)
       # if tec==27:
        #    break

    #cap.release()
    #cv2.destroyAllWindows()