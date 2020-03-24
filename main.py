# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets,uic
import pymysql

#Licencias Base de Datos
_host='localhost'
_user='root'
_password='gafo951101'
_db='PuntoVenta'
print("Prueba")

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        uic.loadUi('login.ui',self)
        self.show()
        self.button_iniciar.clicked.connect(self.clicIniciar)

    def clicIniciar(self):
        a = self.line_usuario.text()
        b = self.line_contrasena.text()
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT v_Id,v_Usuario,v_Contrasena FROM PuntoVenta.Vendedores WHERE v_Usuario=%s and v_Contrasena=%s"
                    datos = (a,b)
                    cursor.execute(sentencia,datos)
                    vendedores = cursor.fetchall()
                    if len(vendedores)==1:
                        print("Funciona")
                        self.close()
                        otraventana=VentanaPrincipal(self)
                        otraventana.show()
                    else:
                        self.line_usuario.clear()
                        self.line_contrasena.clear()  
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(VentanaPrincipal,self).__init__(parent)
        uic.loadUi('mainWindow.ui',self)

        def cerrar(self):
            self.parent().show()
            self.close()

app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec()