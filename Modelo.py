import mysql.connector
import mysql 
import pydicom
import os
import cv2
import dicom2nifti
import pandas as pd 
import numpy as np

class Login:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="", 
            database="filesbank"
        )
        self.cursor = self.conexion.cursor()

    def validar_usuario(self, usuario, contrasena):
        buscar = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND Contraseña = %s"
        self.cursor.execute(buscar, (usuario, contrasena))
        return self.cursor.fetchone() # Devuelve una tupla con los datos del usuario si existe, o None si no existe

class CSV:
    def __init__(self, ruta=None):
        self.__ruta = ruta
        self.__dataframe = None
        if ruta:
            self.__dataframe = self.cargar_csv(ruta)

    def cargar_csv(self, ruta):
        self.__ruta = ruta
        self.__dataframe = pd.read_csv(ruta)
        return self.__dataframe

    def mostrar_dataframe(self):
        return self.__dataframe
    
class ImagenesNormales:
    def __init__(self, path=""):
        self.__path = path

    def getPath(self):
        return self.__path

    def setPath(self, path):
        self.__path = path

    def cargarImagenes(self, path=None):
        if path is None:
            path = self.__path
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"No se pudo cargar la imagen: {path}")
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img_gray

    # Filtros simples
    def Binario(self, Img):
        return cv2.threshold(Img, 125, 255, cv2.THRESH_BINARY)[1]

    def BinarioInv(self, Img):
        return cv2.threshold(Img, 125, 255, cv2.THRESH_BINARY_INV)[1]

    def truncado(self, Img):
        return cv2.threshold(Img, 125, 255, cv2.THRESH_TRUNC)[1]

    def tozero(self, Img):
        return cv2.threshold(Img, 125, 255, cv2.THRESH_TOZERO)[1]

    def tozeroInv(self, Img):
        return cv2.threshold(Img, 125, 255, cv2.THRESH_TOZERO_INV)[1]

    def otsu(self, Img):
        return cv2.threshold(Img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Morfología
    def dilate(self, Img, k):
        return cv2.dilate(Img, np.ones((k, k), np.uint8), iterations=1)

    def erode(self, Img, k):
        return cv2.erode(Img, np.ones((k, k), np.uint8), iterations=1)

    # Avanzados
    def bordes(self, Img):
        return cv2.Canny(Img, 100, 200)
    
