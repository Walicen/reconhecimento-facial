import cv2
import sys
import os

from time import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, 'assets')
CASC = "{0}/haarcascade-frontalface-default.xml".format(ASSETS)


def detectar_faces(nome_imagem):
    classificador = cv2.CascadeClassifier(CASC)

    imagem = cv2.imread(f"{ASSETS}/{nome_imagem}")
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    faces = classificador.detectMultiScale(
        cinza,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) > 0:
        try:
            for (x, y, w, h) in faces:
                cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)

            filename = salvar_image(imagem)
        except Exception as e:
            return e
        print("OK")
        return filename
    else:
        print("Nenhuma Face Detectada")
        return False


# Salvar a imagem com as faces detectadas
def salvar_image(imagem):
    timestamp = str(time()).replace(".", "")
    filename = "faces_detectadas_{0}.jpg".format(timestamp)
    pathfile = "{0}/{1}".format(ASSETS, filename)
    cv2.imwrite(pathfile, imagem)
    return filename


if __name__ == "__main__":
    detectar_faces(sys.argv[1])

