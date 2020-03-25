# -*- coding: utf-8 -*-
import sys
import pymysql
import datetime
from PyQt5 import QtWidgets,uic

#Licencias Base de Datos
_host='localhost'
_user='root'
_password='gafo951101'
_db='PuntoVenta'

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        uic.loadUi('UI/login.ui',self)
        self.show()
        self.button_iniciar.clicked.connect(self.clicIniciar)
        self.bNuevo.clicked.connect(self.abrirNuevo)
        self.bRecordar.clicked.connect(self.abrirRecordar)

    def clicIniciar(self):
        a = self.line_usuario.text()
        b = self.line_contrasena.text()
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT v_Id,v_Usuario,v_Contrasena, v_Nombre FROM Vendedores WHERE v_Usuario='%s' and v_Contrasena='%s'" % (a,b)
                    cursor.execute(sentencia)
                    vendedores = cursor.fetchall()
                    if len(vendedores)==1:
                        self.line_usuario.clear()
                        self.line_contrasena.clear()  
                        self.hide()
                        otraventana=VentanaPrincipal(self)
                        otraventana.show()
                    else: 
                        self.line_usuario.clear()
                        self.line_contrasena.clear()  
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

    def abrirNuevo(self):
        self.line_usuario.clear()
        self.line_contrasena.clear()  
        self.hide()
        nuevo=nuevoUsuario(self)
        nuevo.show()

    def abrirRecordar(self):
        self.line_usuario.clear()
        self.line_contrasena.clear()  
        self.hide()
        nuevo=consultaContrasena(self)
        nuevo.show()   

class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(VentanaPrincipal,self).__init__(parent)
        uic.loadUi('UI/mainWindow.ui',self)
        self.bSalir.clicked.connect(self.cerrar)
        self.bVender.clicked.connect(self.abrirVender)

    def abrirVender(self):
        self.wVender = vender(self)
        self.wVender.move(150,0)
        self.wVender.show()

    def cerrar(self):
        self.parent().show()
        self.close()

class nuevoUsuario(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevoUsuario,self).__init__(parent)
        uic.loadUi('UI/newUsuario.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

    def guardar(self):
        a = self.line_usuario.text()
        b = self.line_contrasena.text()
        c = self.line_nombre.text()
        
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT v_Usuario FROM Vendedores WHERE v_Usuario='%s'" % (a))
                    vendedores = cursor.fetchall()
                    if len(vendedores)==0:
                        insertar = (
                        "INSERT INTO Vendedores (v_Usuario,v_Contrasena,v_Nombre)"
                        "VALUES(%s,%s,%s)"
                        )
                        datos = (a,b,c)
                        cursor.execute(insertar,datos)
                        conexion.commit()
                        self.label_titulo.setText("Agregado con Éxito")
                        self.cerrar()
                    else:
                        self.label_titulo.setText("Error: Ya existe el usuario")
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.parent().show()
        self.close()

class consultaContrasena(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(consultaContrasena,self).__init__(parent)
        uic.loadUi('UI/contrasena.ui',self)
        self.bContra.clicked.connect(self.consultar)
        self.bSalir.clicked.connect(self.cerrar)

    def consultar(self):
        a = self.line_usuario.text()

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT v_Contrasena FROM Vendedores WHERE v_Usuario='%s'" % (a)
                    cursor.execute(sentencia)
                    vendedores = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        if len(vendedores)==0:
            self.label_contrasena.setText("No existe el usuario")
        else:
            contrasena = vendedores[0][0]
            self.label_contrasena.setText(contrasena)

    def cerrar(self):
        self.parent().show()
        self.close()

class vender(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(vender,self).__init__(parent)
        uic.loadUi('UI/vender.ui',self)
        fecha = str(datetime.date.today())
        self.line_fecha.setText(fecha)
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT note_Id FROM Notas")
                    notas = cursor.fetchall()
                    cursor.execute("SELECT * FROM Clientes")
                    clientes = cursor.fetchall()
                    cursor.execute("SELECT * FROM Productos")
                    productos = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        if len(notas)==0:
            self.line_folio.setText("1")
        else:
            num = str(notas[-1][0]+1)
            self.line_folio.setText(num)

        nombres = []
        prods = []
        for i in range(len(clientes)):
            nombres.append(clientes[i][2])
        for i in range(len(productos)):
            prods.append(productos[i][2])
        self.comboBox_cliente.addItems(nombres)
        self.comboBox_producto.addItems(prods)


app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec()