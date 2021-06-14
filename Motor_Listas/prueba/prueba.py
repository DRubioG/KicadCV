from KicadCV import *

a=KicadCV('prueba.kicad_pcb')
blanco=np.ones((700,1000,3),dtype=np.uint8)
a.pintar_linea(blanco)
a.pintar_ruta(blanco)
cv2.imshow("prueba", blanco)
cv2.waitKey()