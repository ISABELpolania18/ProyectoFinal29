import mysql.connector
import mysql 
import pydicom
import os
import cv2
import dicom2nifti
import pandas as pd 
import numpy as np
import scipy.io as sio

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
    
    def anadir_usuario(self, nombre_usuario, contrasena, rol):
        insertar = "INSERT INTO usuarios (nombre_usuario, Contraseña, Tipo_Usuario) VALUES (%s, %s, %s)"
        self.cursor.execute(insertar, (nombre_usuario, contrasena, rol))
        self.conexion.commit()
    


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
    
    def guardar_csv(self, cursor, conexion, usuario, archivo_nombre): #Agregar aquí
        cod_archivo = np.random.randint(1000, 99999)  
        consulta = """
            INSERT INTO archivos_otros 
            (nombre_usuario, cod_archivo, tipo_archivo, nombre_archivo, fecha_archivo, ruta_archivo)
            VALUES (%s, %s, %s, %s, CURDATE(), %s)
        """
        datos = (
            usuario,
            cod_archivo,
            'csv',
            archivo_nombre,
            self.__ruta
        )
        cursor.execute(consulta, datos)
        conexion.commit()
    
    
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

    '''Método diferente de openCV. '.Canny()'
    El algoritmo de detección de bordes Canny se utiliza en visión artificial para identificar bordes en una imagen.
    Ayuda a resaltar límites importantes para tareas como la detección de objetos y la segmentación de imágene'''
    def bordes(self, Img):
        return cv2.Canny(Img, 100, 200)
    
    def guardar_en_bd(self, cursor, conexion, usuario, archivo_nombre): #Agregar aquí
        cod = np.random.randint(1000, 99999)
        ruta = self.__path
        consulta = """
            INSERT INTO archivos_otros 
            (nombre_usuario, cod_archivo, tipo_archivo, nombre_archivo, fecha_archivo, ruta_archivo)
            VALUES (%s, %s, %s, %s, CURDATE(), %s)
        """
        cursor.execute(consulta, (usuario, cod, 'png', archivo_nombre, ruta))
        conexion.commit() 
        

class DICOM:
    def __init__(self, c, u,contrasena):
        self.__carpeta = c
        self.__usuario = u
        self.__contrasena = contrasena
        self.__volumen = None
        self.__slices = []
        self.__ruta_nifti = None
        self.__datos_paciente = {}

        if self.__carpeta:  
            self.cargar_dicom()

    def cargar_dicom(self):
        archivos = [f for f in os.listdir(self.__carpeta) if f.endswith('.dcm')]
        self.__slices = [pydicom.dcmread(os.path.join(self.__carpeta, f)) for f in archivos]
        self.__slices.sort(key=lambda x: int(x.InstanceNumber))
        self.__volumen = np.stack([d.pixel_array for d in self.__slices])

        #metadatos
        paciente = self.__slices[0]
        self.__datos_paciente = {
            "usuario": self.__usuario ,
            "cod_archivo": self.__contrasena,  # aca no se si poner enseguida lo del usuario o generar otro
            "nombre": str(paciente.get('PatientName', 'Anónimo')),
            "id": str(paciente.get('PatientID', '0')),
            "edad": str(paciente.get('PatientAge', 'NA')),
            "ruta_dicom": self.__carpeta
        }
        
        self.__ruta_nifti = self.convertir_nifti() #convierte carpeta a NIFTI

    def convertir_nifti(self):
        from pathlib import Path
        nifti_ = str(Path(self.__carpeta).parent / "convertido_nifti")
        os.makedirs(nifti_, exist_ok=True)

        dicom2nifti.convert_directory(self.__carpeta, nifti_)
        return nifti_ 
    
    def guardar_bd(self,cursor,conexion):
        consulta = """
            INSERT INTO archivos_medicos 
            (nombre_usuario, cod_archivo, Nombre_Paciente, ID_Paciente, Edad_Paciente, Ruta_Dicom,Ruta_Nifti)
            VALUES (%s, %s, %s, %s, %s, %s,%s)
            """
        datos = (
            self.__datos_paciente["usuario"],
            self.__datos_paciente["cod_archivo"],
            self.__datos_paciente["nombre"],
            self.__datos_paciente["id"],
            self.__datos_paciente["edad"],
            self.__datos_paciente["ruta_dicom"],
            self.__ruta_nifti
        )
        cursor.execute(consulta, datos)
        conexion.commit()

    def get_volumen(self):
        return self.__volumen

    def get_slices(self):
        return self.__slices

    def get_ruta_nifti(self):
        return self.__ruta_nifti

    def get_datos_paciente(self):
        return self.__datos_paciente

class MAT:
    def __init__(self):
        self.datos_senales = {}
        self.senal_actual = None
        self.nombre_usuario = ""
        self.cod_archivo = None
        self.nombre_archivo = ""
        self.ruta_archivo = ""

    def cargar_archivo(self, ruta):
        mat = sio.loadmat(ruta)
        self.datos_senales = {}

        for k, v in mat.items():
            if isinstance(v, np.ndarray):
                if v.ndim == 3:
                    # Extraer cada canal como una señal separada
                    for canal in range(v.shape[0]):
                        self.datos_senales[f"{k}_canal_{canal}"] = v[canal, :, :]
                elif v.ndim == 2:
                    self.datos_senales[k] = v
                elif v.ndim == 1:
                    self.datos_senales[k] = v.flatten()

        self.cod_archivo = np.random.randint(1000, 99999)
        self.nombre_archivo = os.path.basename(ruta)
        self.ruta_archivo = ruta
        return list(self.datos_senales.keys())


    def seleccionar_senal(self, nombre):
        self.senal_actual = self.datos_senales.get(nombre, None)
        return self.senal_actual

    def aplicar_filtro(self, tipo):
        if self.senal_actual is None:
            return None

        if tipo == "Media Móvil":
            ventana = 5
            return np.convolve(self.senal_actual, np.ones(ventana)/ventana, mode='valid')
        elif tipo == "Mediana":
            return pd.Series(self.senal_actual).rolling(window=5).median().dropna().values
        return None

    def guardar_en_bd(self, cursor, conexion, nombre_usuario):
        try:
            consulta = """
                INSERT INTO archivos_otros 
                (nombre_usuario, cod_archivo, tipo_archivo, nombre_archivo, fecha_archivo, ruta_archivo)
                VALUES (%s, %s, %s, %s, CURDATE(), %s)
            """
            datos = (
                nombre_usuario,
                self.cod_archivo,
                'mat',
                self.nombre_archivo,
                self.ruta_archivo
            )
            cursor.execute(consulta, datos)
            conexion.commit()
        except Exception as e:
            print("Error al guardar en la base de datos:", e)
            raise
    
