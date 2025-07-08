from Modelo import CSV, ImagenesNormales, Login
import sys
#QFileDialog que es una ventana para abrir/guardar archivos
#QVBoxLayout es un organizador de widget en la ventana, este en particular los apila en vertical
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QMessageBox, QDialog
#ell layout es el organizador haciendo desde el codigo
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from matplotlib.figure import Figure
# Contenedor (canvas = lienzo) para graficos de Matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas #es la que mensajea los graficos
import scipy.io as sio
import numpy as np
import mysql.connector as sql
import pydicom
import os
import cv2
import dicom2nifti
import pandas as pd 



class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('Login.ui', self)
        self.setup()

    def setup(self):
        self.Boton_Ingresar.clicked.connect(self.ingresar)
        self.Boton_Agregar.clicked.connect(self.abrir_ventana_agregar_usuario)

    def ingresar(self):
        usuario = self.Usuario.text()
        contrasena = self.Contrasena.text()
        self.__mensajero.verificar_login(usuario, contrasena)

    def abrir_ventana_agregar_usuario(self):
        self.ventanaAgregarUsuario = ventanaAgregarUsuario(self) #el self indica que su ventana padre es esta ventanaPrincipal
        self.ventanaAgregarUsuario.asignarCoordinador(self.__mensajero)
        self.hide()
        self.ventanaAgregarUsuario.show()  # Muestra la ventana de agregar usuario
        
    def asignarCoordinador(self,c):
        self.__mensajero = c
class ventanaAgregarUsuario(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        loadUi('nuevo.ui', self)
        self.__mi_ventana_principal = parent
        self.setup()

    def setup(self):
        self.Aceptar.clicked.connect(self.Agregar_Usuario)
    

    def Agregar_Usuario(self):
        nuevo_usuario = self.Nuevo_Usuario.text()
        nueva_contrasena = self.Nueva_Contrasena.text()
        rol = self.Rol.currentText() #porque es un combo box
        self.__mensajero.agregar_usuario(nuevo_usuario, nueva_contrasena, rol,self) #self es para que sepa que es la ventana de agregar usuario

    def asignarCoordinador(self, c):
        self.__mensajero = c
        

class ventana_Senales(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        loadUi('Ventana_Senales.ui', self)
        self.__mi_ventana_principal = parent
        self.setup()

    def setup(self):
        self.botonCSV.clicked.connect(self.abrir_ventana_csv)
        self.botonMAT.clicked.connect(self.abrir_ventana_mat)
        
    
    def abrir_ventana_csv(self):
        self.ventanaCSV = VentanaCSV(self) #ese self indica que su ventana padre es la ventanaCSV
        #Se va a usar la estrategia de decirle al amigo (nueva ventana) que el mesero es ese mensajero(coordinador)
        self.ventanaCSV.asignarCoordinador(self.__mensajero) 
        self.hide()  # Oculta la ventana de señales
        self.ventanaCSV.show()  # Muestra la ventana de CSV
    
    def abrir_ventana_mat(self):
        self.ventanaMAT = Ventana_MAT(self)
        self.ventanaMAT.asignarCoordinador(self.__mensajero)
        self.hide()  # Oculta la ventana de señales
        self.ventanaMAT.show()  # Muestra la ventana de MAT
    def asignarCoordinador(self, c):
        self.__mensajero = c
        

class ventana_Imagenes(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        loadUi('Ventana_Imagenes.ui', self)
        self.__mi_ventana_principal = parent
        self.setup()

    def setup(self):
        self.botonDicom.clicked.connect(self.abrir_ventana_dicom)
        self.botonPNG.clicked.connect(self.abrir_ventana_png)
        
    
    def abrir_ventana_dicom(self):
        self.ventanaDICOM = Ventana_DICOM(self)
        self.ventanaDICOM.asignarCoordinador(self.__mensajero)
        self.hide()  # Oculta la ventana de señales
        self.ventanaDICOM.show()  # Muestra la ventana de CSV
    
    def abrir_ventana_png(self):
        self.ventanaPNG = Ventana_PNG(self)
        self.ventanaPNG.asignarCoordinador(self.__mensajero)
        self.hide()  # Oculta la ventana de señales
        self.ventanaPNG.show()  # Muestra la ventana de MAT
    def asignarCoordinador(self, c):
        self.__mensajero = c
        



class VentanaCSV(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("VentanaCSV.ui", self)
        self.__ventana_principal = parent
        self.setWindowTitle("Graficador CSV")
        self.csv = CSV()
        self.setup()


    def setup(self):
        self.comboTipoGrafico.addItems(["plot", "scatter", "boxplot"])
        self.botonCargar.clicked.connect(self.cargar_csv)
        self.botonGraficar.clicked.connect(self.graficar)
        self.botonEstadisticas.clicked.connect(self.mostrar_estadisticas)
        self.botonGuardar.clicked.connect(self.guardar_en_bd)
        self.botonVolver.clicked.connect(self.volver_a_senales)
        self.botonGuardar.setEnabled(False)

    def cargar_csv(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "CSV Files (*.csv)")
        if ruta:
            try:
                df = self.csv.cargar_csv(ruta)
                columnas = df.columns.tolist()
                self.comboColumnaX.clear()
                self.comboColumnaY.clear()
                self.comboColumnaX.addItems(columnas)
                self.comboColumnaY.addItems(columnas)

                self.nombre_usuario = self.__mensajero.vista.Usuario.text()
                self.cod_archivo = np.random.randint(1000, 99999)
                self.nombre_archivo = os.path.basename(ruta)
                self.ruta_archivo = ruta

                self.botonGuardar.setEnabled(True)
                self.llenar_tabla(df)

                QMessageBox.information(self, "Éxito", "Archivo CSV cargado. Presione 'Guardar' si desea almacenarlo en la base de datos.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {e}")

    def guardar_en_bd(self):
        try:
            consulta = """
                INSERT INTO archivos_otros 
                (nombre_usuario, cod_archivo, tipo_archivo, nombre_archivo, fecha_archivo, ruta_archivo)
                VALUES (%s, %s, %s, %s, CURDATE(), %s)
            """
            cursor = self.__mensajero.modelo.cursor
            datos = (
                self.nombre_usuario,
                self.cod_archivo,
                'csv',
                self.nombre_archivo,
                self.ruta_archivo
            )
            cursor.execute(consulta, datos)
            self.__mensajero.modelo.conexion.commit()
            QMessageBox.information(self, "Éxito", "Archivo CSV guardado en la base de datos.")
            self.botonGuardar.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar en la base de datos: {e}")

    def llenar_tabla(self, df):
        self.tablaDatos.setRowCount(len(df))
        self.tablaDatos.setColumnCount(len(df.columns))
        self.tablaDatos.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.tablaDatos.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iat[i, j])))

    def mostrar_grafica_en_widget(self, figura):
        for i in reversed(range(self.widgetGrafica.layout().count())):
            widget = self.widgetGrafica.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)

        canvas = FigureCanvas(figura)
        self.widgetGrafica.layout().addWidget(canvas)
        canvas.draw()

    def graficar(self):
        tipo = self.comboTipoGrafico.currentText()
        columna_x = self.comboColumnaX.currentText()
        columna_y = self.comboColumnaY.currentText() if tipo != "boxplot" else None

        df = self.csv.mostrar_dataframe()
        if df is None:
            QMessageBox.warning(self, "Error", "No hay archivo cargado.")
            return

        figura = Figure()
        ax = figura.add_subplot(111)

        try:
            if tipo == 'plot':
                ax.plot(df[columna_x], df[columna_y])
                ax.set_title(f'{columna_y} vs {columna_x}')
            elif tipo == 'scatter':
                ax.scatter(df[columna_x], df[columna_y])
                ax.set_title(f'{columna_y} vs {columna_x}')
            elif tipo == 'boxplot':
                ax.boxplot(df[columna_x].dropna())
                ax.set_title(f'Boxplot de {columna_x}')
            ax.grid(True)
            self.mostrar_grafica_en_widget(figura)
        except Exception as e:
            QMessageBox.critical(self, "Error al graficar", str(e))

    def mostrar_estadisticas(self):
        df = self.csv.mostrar_dataframe()
        if df is None:
            QMessageBox.warning(self, "Error", "No hay archivo cargado.")
            return

        columna = self.comboColumnaY.currentText()
        if columna not in df.columns:
            QMessageBox.warning(self, "Error", "Seleccione una columna válida.")
            return

        serie = df[columna].dropna()
        if not np.issubdtype(serie.dtype, np.number):
            QMessageBox.warning(self, "Error", "La columna seleccionada no es numérica.")
            return

        estadisticas = (
            f"Estadísticas para la columna '{columna}':\n\n"
            f"Máximo: {serie.max():.2f}\n"
            f"Mínimo: {serie.min():.2f}\n"
            f"Media: {serie.mean():.2f}\n"
            f"Mediana: {serie.median():.2f}\n"
            f"Desviación estándar: {serie.std():.2f}\n"
            f"Suma: {serie.sum():.2f}"
        )

        QMessageBox.information(self, "Estadísticas", estadisticas)

    def asignarCoordinador(self, c):
        self.__mensajero = c

    def volver_a_senales(self):
        self.close()
        self.__ventana_principal.show()


class Ventana_MAT(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaMAT.ui', self)
        self.__ventana_principal = parent
        self.setup()
    def setup(self):
        pass
    def asignarCoordinador(self, c):
        self.__mensajero = c

class MyDicomCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def mostrar_dicom(self, imagen, titulo=""):
        self.ax.clear()
        self.ax.imshow(imagen, cmap='gray',aspect='auto')
        self.ax.set_title(titulo)
        self.draw()


class Ventana_DICOM(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaDICOM.ui', self)
        self.__ventana_principal = parent
        self.setup()

    def actualizar_axial(self, dx):
        imagen = self.volumen3D[dx, :, :]
        self.canvas_axial.mostrar_dicom(imagen, "Corte Axial")

    def actualizar_coronal(self, dx):
        imagen = self.volumen3D[:, dx, :]
        self.canvas_coronal.mostrar_dicom(imagen, "Corte Coronal")

    def actualizar_sagital(self, dx):
        imagen = self.volumen3D[:, :, dx]
        self.canvas_sagital.mostrar_dicom(imagen, "Corte Sagital")

    def setup(self):
        #layouts para cada corte
        self.layout_axial = QVBoxLayout()
        self.layout_coronal = QVBoxLayout()
        self.layout_sagital = QVBoxLayout()
        #sets
        self.campo_grafico_axial.setLayout(self.layout_axial)
        self.campo_grafico_coronal.setLayout(self.layout_coronal)
        self.campo_grafico_sagital.setLayout(self.layout_sagital)
        #canvas para cada corte
        self.canvas_axial = MyDicomCanvas(self)
        self.canvas_coronal = MyDicomCanvas(self)
        self.canvas_sagital = MyDicomCanvas(self)
        #adds
        self.layout_axial.addWidget(self.canvas_axial)
        self.layout_coronal.addWidget(self.canvas_coronal)
        self.layout_sagital.addWidget(self.canvas_sagital)

        self.boton_cargar.clicked.connect(self.cargar_dicom)

        # Conectar sliders( actualizar cortes)
        self.slider_axial.valueChanged.connect(self.actualizar_axial)
        self.slider_coronal.valueChanged.connect(self.actualizar_coronal)
        self.slider_sagital.valueChanged.connect(self.actualizar_sagital)

    def asignarCoordinador(self, c):
        self.__mensajero = c

    def cargar_dicom(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if carpeta:
            archivos = [f for f in os.listdir(carpeta) if f.endswith('.dcm')]

            #ordenar slices
            slices = []
            for archivo in archivos:
                path = os.path.join(carpeta, archivo)
                ds = pydicom.dcmread(path)
                slices.append(ds)

            slices.sort(key=lambda x: int(x.InstanceNumber))  

            #volumen
            volumen = np.stack([d.pixel_array for d in slices])
            self.volumen3D = volumen  

            #metadatos
            cod=123
            nombre = str(slices[0].get('PatientName', 'Anónimo'))
            id_= str(slices[0].get('PatientID', '0'))
            edad = str(slices[0].get('PatientAge', 'NA'))
            ruta = carpeta 

            self.nombre_usuario = self.__mensajero.vista.Usuario.text()
            self.cod = cod
            self.nombre_paciente = nombre
            self.id_paciente = id_
            self.edad_paciente = edad
            self.ruta_dicom = ruta
             


            #Navegar en indices de cortes
            self.slider_axial.setMaximum(volumen.shape[0] - 1)
            self.slider_coronal.setMaximum(volumen.shape[1] - 1)
            self.slider_sagital.setMaximum(volumen.shape[2] - 1)

            #corte para mostrar
            self.slider_axial.setValue(volumen.shape[0] // 2)
            self.slider_coronal.setValue(volumen.shape[1] // 2)
            self.slider_sagital.setValue(volumen.shape[2] // 2)

            ruta_nifti = self.convertir_nifti(ruta) #convierte carpeta a NIFTI
            self.guardar_bd(ruta_nifti)

    def convertir_nifti(self, carpeta):
        from pathlib import Path
        nifti_ = str(Path(carpeta).parent / "convertido_nifti")
        os.makedirs(nifti_, exist_ok=True)

        dicom2nifti.convert_directory(carpeta, nifti_)
        return nifti_ 
        
    def guardar_bd(self,ruta_nifti):
        consulta = """
            INSERT INTO archivos_medicos 
            (nombre_usuario, cod_archivo, Nombre_Paciente, ID_Paciente, Edad_Paciente, Ruta_Dicom,Ruta_Nifti)
            VALUES (%s, %s, %s, %s, %s, %s,%s)
            """
     
        cursor = self.__mensajero.modelo.cursor

        datos = (
            self.nombre_usuario,
            self.cod,
            self.nombre_paciente,
            self.id_paciente,
            self.edad_paciente,
            self.ruta_dicom,
            ruta_nifti
        )

        cursor.execute(consulta, datos)
        self.__mensajero.modelo.conexion.commit()
        QMessageBox.information(self,"Exito","Datos guardados en la base de datos")
        

class MyGraphCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def graficar_imagen(self, img, cmap='gray'):
        self.axes.clear()
        self.axes.imshow(img, cmap=cmap)
        self.axes.axis('off')
        self.draw()


class Ventana_PNG(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('VentanaPNG.ui', self)
        self.__ventana_principal = parent
        self.imagenes = ImagenesNormales()
        self.setup()

    def setup(self):
        #self.imagenes = self.__mensajero.ImagenesNormales()
        self.img_gray = None
        self.img_resultado = None
        self.canvas = MyGraphCanvas()
        self.campo_grafico.layout().addWidget(self.canvas)

        # Añadir filtros al combo
        filtros = [
            "Binario", "Binario Inv", "Truncado", "ToZero", "ToZero Inv", "Otsu",
            "Dilate", "Erode", "Detectar Bordes", "Contar Células"
        ]
        self.combo_filtros.addItems(filtros)

        # Conectar botones
        self.boton_aplicar.clicked.connect(self.aplicar_filtro_unificado)
        self.boton_cargar.clicked.connect(self.cargar_imagen)
        self.boton_guardar.clicked.connect(self.guardar_resultado)
        self.boton_volver.clicked.connect(self.volver)

    def cargar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar Imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        if ruta:
            self.img_gray = self.imagenes.cargarImagenes(ruta)
            self.imagenes.setPath(ruta)
            self.nombre_usuario = self.__mensajero.vista.Usuario.text()
            self.nombre_archivo = os.path.basename(ruta)
            self.canvas.graficar_imagen(self.img_gray)
            self.img_resultado = None

    def aplicar_filtro_unificado(self):
        if self.img_gray is None:
            QMessageBox.warning(self, "Error", "Cargue una imagen primero.")
            return

        filtro = self.combo_filtros.currentText()
        usar_kernel = filtro in ["Dilate", "Erode"]

        if usar_kernel:
            try:
                k = int(self.entrada_kernel.text())
                if k % 2 == 0:
                    k += 1
            except:
                QMessageBox.warning(self, "Error", "Ingrese un tamaño de kernel válido")
                return
        else:
            k = None

        if filtro == "Binario":
            self.img_resultado = self.imagenes.Binario(self.img_gray)
        elif filtro == "Binario Inv":
            self.img_resultado = self.imagenes.BinarioInv(self.img_gray)
        elif filtro == "Truncado":
            self.img_resultado = self.imagenes.truncado(self.img_gray)
        elif filtro == "ToZero":
            self.img_resultado = self.imagenes.tozero(self.img_gray)
        elif filtro == "ToZero Inv":
            self.img_resultado = self.imagenes.tozeroInv(self.img_gray)
        elif filtro == "Otsu":
            self.img_resultado = self.imagenes.otsu(self.img_gray)
        elif filtro == "Dilate":
            binaria = self.imagenes.Binario(self.img_gray)
            self.img_resultado = self.imagenes.dilate(binaria, k)
        elif filtro == "Erode":
            binaria = self.imagenes.Binario(self.img_gray)
            self.img_resultado = self.imagenes.erode(binaria, k)
        elif filtro == "Detectar Bordes":
            self.img_resultado = self.imagenes.bordes(self.img_gray)
        elif filtro == "Contar Células":
            _, imR = cv2.threshold(self.img_gray, 50, 255, cv2.THRESH_BINARY)
            kernel = np.ones((3, 3), np.uint8)
            dilatada = cv2.dilate(imR, kernel, iterations=3)
            erosionada = cv2.erode(dilatada, kernel, iterations=25)
            elem, mask = cv2.connectedComponents(erosionada)
            self.img_resultado = mask
            QMessageBox.information(self, "Conteo", f"Número de células: {elem}")

        cmap = 'nipy_spectral' if filtro == "Contar Células" else 'gray'
        self.canvas.graficar_imagen(self.img_resultado, cmap=cmap)

    def guardar_resultado(self):
        if self.img_resultado is None:
            QMessageBox.warning(self, "Error", "No hay imagen procesada para guardar.")
            return

        try:
            consulta = """
                INSERT INTO archivos_otros 
                (nombre_usuario, cod_archivo, tipo_archivo, nombre_archivo, fecha_archivo, ruta_archivo)
                VALUES (%s, %s, %s, %s, CURDATE(), %s)
            """
            cursor = self.__mensajero.modelo.cursor
            datos = (
                self.nombre_usuario,
                np.random.randint(1000, 99999),
                'png',
                self.nombre_archivo,
                self.imagenes.getPath()
            )
            cursor.execute(consulta, datos)
            self.__mensajero.modelo.conexion.commit()
            QMessageBox.information(self, "Guardado", "Registro guardado en archivos_otros")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def volver(self):
        self.close()
        self.__ventana_principal.show()

    def asignarCoordinador(self, c):
        self.__mensajero = c
