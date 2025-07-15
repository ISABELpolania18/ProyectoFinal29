from Modelo import *
from Vista import *

class Controlador:
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def verificar_login(self, usuario, contrasena):
        datos = self.modelo.validar_usuario(usuario, contrasena) 
        if datos:
            msg = QMessageBox(self.vista)
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Bienvenid@ {datos[0]} con rol: {datos[2]}")
            msg.setWindowTitle("Ingreso exitoso")
            msg.exec_() #para bloquear la ejecución hasta que el usuario haga clic en "Aceptar"
            if datos[2]=='Señales':
                self.ventana_Senales = ventana_Senales(self.vista)
                self.ventana_Senales.asignarCoordinador(self)
                self.vista.hide()  # Oculta la ventana de login
                self.ventana_Senales.show()  # Muestra la ventana de señales
            elif datos[2]=='Imágenes':
                self.ventana_Imagenes = ventana_Imagenes(self.vista)
                self.ventana_Imagenes.asignarCoordinador(self)
                self.vista.hide()  # Oculta la ventana de login
                self.ventana_Imagenes.show()  # Muestra
        
        else:
            QMessageBox.warning(self.vista, "Error", "Usuario o contraseña incorrectos.")
    
    def agregar_usuario(self, nombre_usuario, contrasena, rol, ventana):
        self.modelo.anadir_usuario(nombre_usuario, contrasena, rol)
        QMessageBox.information(ventana, "Éxito", "Usuario agregado correctamente.")
        ventana.close()
        self.vista.show() 
        
    def cargar_dicom(self, carpeta):
        usuario = self.vista.Usuario.text()
        contrasena = self.vista.Contrasena.text()
        self.dicom = DICOM(carpeta, usuario,contrasena)
        self.dicom.guardar_bd(self.modelo.cursor, self.modelo.conexion)
        return self.dicom.get_volumen() # Muestra la ventana principal nuevamente
    
    def guardar_en_bd(self, imagenes, usuario, archivo_nombre, vista): #es la de png
        try:
            imagenes.guardar_en_bd(self.modelo.cursor, self.modelo.conexion, usuario, archivo_nombre)
            QMessageBox.information(vista, "Guardado", "Registro guardado en archivos_otros")
        except Exception as e:
            QMessageBox.critical(vista, "Error", str(e))
    
    def guardar_en_bd_csv(self, csv, usuario, archivo_nombre, vista): 
        try:
            csv.guardar_csv(self.modelo.cursor, self.modelo.conexion, usuario, archivo_nombre)
            QMessageBox.information(vista, "Guardado", "Registro guardado en archivos_otros")
        except Exception as e:
            QMessageBox.critical(vista, "Error", str(e))
    
    def guardar_en_bd_mat(self, mat, vista):
        try:
            usuario = self.modelo.usuario_actual if hasattr(self.modelo, 'usuario_actual') else self.vista.Usuario.text()
            mat.guardar_en_bd(self.modelo.cursor, self.modelo.conexion, usuario)
            QMessageBox.information(vista, "Éxito", "Archivo .mat guardado en la base de datos.")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            QMessageBox.critical(vista, "Error", f"Error al guardar en la BD: {str(e)}")
    
def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    modelo = Login()
    controlador = Controlador(ventana, modelo)
    ventana.asignarCoordinador(controlador)
    ventana.show()
    sys.exit(app.exec_())  
    
if __name__ == "__main__":
    main()  
