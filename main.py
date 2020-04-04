# -*- coding: utf-8 -*-
import sys
import pymysql
import imagenes.imagenes
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
                        otraventana.setNombreHeader(vendedores[0][1].title())
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
        self.close()
        nuevo=nuevoUsuario(self)
        nuevo.show()

    def abrirRecordar(self):
        self.line_usuario.clear()
        self.line_contrasena.clear()  
        self.close()
        nuevo=consultaContrasena(self)
        nuevo.show() 

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

class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(VentanaPrincipal,self).__init__(parent)
        uic.loadUi('UI/mainWindow.ui',self)

        self.wVender = vender(self.body)
        self.wProductos = productos(self.body)
        self.wClientes = clientes(self.body)
        self.wAlmacenes = almacenes(self.body)
        self.wSalidas = salidas(self.body)
        self.wEntradas = entradas(self.body)
        self.wReportes = proveedores(self.body)

        self.refreshBody()

        self.bSalir.clicked.connect(self.cerrar)
        self.bVender.clicked.connect(self.abrirVender)
        self.bProductos.clicked.connect(self.abrirProductos)
        self.bClientes.clicked.connect(self.abrirClientes)
        self.bAlmacenes.clicked.connect(self.abrirAlmacenes)
        self.bSalidas.clicked.connect(self.abrirSalidas)
        self.bEntradas.clicked.connect(self.abrirEntradas)
        self.bProveedores.clicked.connect(self.abrirProveedores)

    def setNombreHeader(self,nombre):
        self.label_header.setText("Bienvenido %s" % (nombre))

    
    def abrirVender(self):
        self.refreshBody()
        self.wVender.show()
        
    def abrirProductos(self):
        self.refreshBody()
        self.wProductos.show()
    
    def abrirClientes(self):
        self.refreshBody()
        self.wClientes.show()
    
    def abrirAlmacenes(self):
        self.refreshBody()
        self.wAlmacenes.show()
    
    def abrirSalidas(self):
        self.refreshBody()
        self.wSalidas.show()
    
    def abrirEntradas(self):
        self.refreshBody()
        self.wEntradas.show()

    def abrirProveedores(self):
        self.refreshBody()
        self.wReportes.show()

    def refreshBody(self):
        self.wProductos.close()
        self.wVender.close()
        self.wClientes.close()
        self.wAlmacenes.close()
        self.wSalidas.close()
        self.wEntradas.close()
        self.wReportes.close()

    def cerrar(self):
        self.wProductos.close()
        self.wVender.close()
        self.parent().show()
        self.close()

class vender(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(vender,self).__init__(parent)
        uic.loadUi('UI/vender.ui',self)
        self.bSalir.clicked.connect(self.cerrar)

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

    def cerrar(self):
        self.close() 

class productos(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(productos,self).__init__(parent)
        uic.loadUi('UI/productos.ui',self)

        self.bNuevo.clicked.connect(self.nuevo)
        self.bEditar.clicked.connect(self.editar)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bActualizar.clicked.connect(self.actualizar)
        
        self.productos,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,11,self.productos)
    
    def crearTabla(self,filas,columnas,datos):
        self.table_productos.setRowCount(filas)
        self.table_productos.setColumnCount(columnas)
        self.table_productos.setHorizontalHeaderLabels(["ID","COD","NOMBRE", "DESCRIPCION","MIN","MAX","EXISTENCIA","COSTO","PRECIO","PROV","ALM"])
        self.header = self.table_productos.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        #self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range (0,self.filas):
            for j in range (0,11):
                self.table_productos.setItem(i, j, QtWidgets.QTableWidgetItem(str(datos[i][j])))
    
    def consultarTodo(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT * FROM Productos"
                    cursor.execute(sentencia)
                    productos = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        return productos,len(productos)
    
    def nuevo(self):
        producto=nuevoProducto(self)
        producto.show()
    
    def editar(self):
        if self.table_productos.currentRow() >= 0:
            fila = self.table_productos.currentRow()
            lista = []
            for i in range(0,len(self.productos[fila])):
                lista.append(self.productos[fila][i])
            update = updateProducto(self)
            update.setInfo(lista)
            update.show()
    
    def eliminar(self):
        if self.table_productos.currentRow() >= 0:
            fila = self.table_productos.currentRow()
            num = self.productos[fila][0]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:    
                        cursor.execute("DELETE FROM Productos WHERE prod_Id = '%s' " % (num))
                    conexion.commit()
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def actualizar(self):
        self.productos,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,11,self.productos)

class nuevoProducto(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevoProducto,self).__init__(parent)
        uic.loadUi('UI/nuevoProducto.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

        self.llenarComboBox()
    
    def llenarComboBox(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT prov_Id,prov_Nombres,prov_Paterno,prov_Materno FROM Proveedores")
                    self.proveedores = cursor.fetchall()
                    cursor.execute("SELECT * FROM Almacenes")
                    self.almacenes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        listaProveedores = []
        listaAlmacenes = []
        for i in range(0,len(self.proveedores)):
            nombre = self.proveedores[i][1]+" "+self.proveedores[i][2]+" "+self.proveedores[i][3]
            listaProveedores.append(nombre)
        for i in range(0,len(self.almacenes)):
            listaAlmacenes.append(self.almacenes[i][1])
        self.comboBox_proveedor.addItems(listaProveedores)
        self.comboBox_almacen.addItems(listaAlmacenes)

    def guardar(self):
        codigoBarras = self.line_Cbarras.text()
        nombre = self.line_nombre.text()
        descripcion = self.line_descripcion.text()
        stockmin = self.line_stockmin.text()
        stockmax = self.line_stockmax.text()
        costo = self.line_costo.text()
        precio = self.line_precio.text()
        proveedor = self.proveedores[self.comboBox_proveedor.currentIndex()][0]
        almacen = self.almacenes[self.comboBox_almacen.currentIndex()][0]

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Productos (prod_CodBarras,prod_Nombre,prod_Descrip,prod_StockMin,prod_StockMax,prod_Costo,prod_Precio,prod_IdProv,prod_IdAlmacen)"
                                    "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (codigoBarras,nombre,descripcion,stockmin,stockmax,costo,precio,proveedor,almacen))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.close()

class updateProducto(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(updateProducto,self).__init__(parent)
        uic.loadUi('UI/updateProducto.ui',self)
        self.proveedores = None
        self.almacenes = None
        self.num = None
        self.codigoBarras = None
        self.nombre = None
        self.descripcion = None 
        self.stockmin = None 
        self.stockmax = None 
        self.costo = None 
        self.precio = None 
        self.proveedor = None 
        self.almacen = None 

        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

    def llenarComboBox(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT prov_Id,prov_Nombres,prov_Paterno,prov_Materno FROM Proveedores")
                    self.proveedores = cursor.fetchall()
                    cursor.execute("SELECT * FROM Almacenes")
                    self.almacenes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        listaProveedores = []
        listaAlmacenes = []
        for i in range(0,len(self.proveedores)):
            nombre = self.proveedores[i][1]+" "+self.proveedores[i][2]+" "+self.proveedores[i][3]
            listaProveedores.append(nombre)
        for i in range(0,len(self.almacenes)):
            listaAlmacenes.append(self.almacenes[i][1])
        self.comboBox_proveedor.addItems(listaProveedores)
        self.comboBox_almacen.addItems(listaAlmacenes)

    def setInfo(self,lista):
        self.lista = lista
        self.num = lista[0]
        self.codigoBarras = lista[1]
        self.nombre = lista[2]
        self.descripcion = lista[3] 
        self.stockmin = lista[4] 
        self.stockmax = lista[5]
        self.costo = lista[7] 
        self.precio = lista[8] 
        self.proveedor = lista[9] 
        self.almacen = lista[10] 

        self.line_Cbarras.setText(str(self.codigoBarras))
        self.line_nombre.setText(self.nombre)
        self.line_descripcion.setText(self.descripcion )
        self.line_stockmin.setText(str(self.stockmin))
        self.line_stockmax.setText(str(self.stockmax))
        self.line_costo.setText(str(self.costo))
        self.line_precio.setText(str(self.precio))

        self.llenarComboBox()
    
    def getInfo(self):
        return self.num,self.nombre

    def guardar(self):
        idProducto = self.num
        codigoBarras = self.line_Cbarras.text()
        nombre = self.line_nombre.text()
        descripcion = self.line_descripcion.text()
        stockmin = self.line_stockmin.text()
        stockmax = self.line_stockmax.text()
        costo = self.line_costo.text()
        precio = self.line_precio.text()
        proveedor = self.proveedores[self.comboBox_proveedor.currentIndex()][0]
        almacen = self.almacenes[self.comboBox_almacen.currentIndex()][0]

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE Productos SET prod_CodBarras = '%s',prod_Nombre = '%s', prod_Descrip = '%s', prod_StockMin = '%s', prod_StockMax = '%s', prod_Costo = '%s', prod_Precio = '%s', prod_IdProv = '%s', prod_IdAlmacen = '%s' WHERE (prod_Id = '%s')" % (codigoBarras,nombre,descripcion,stockmin,stockmax,costo,precio,proveedor,almacen,idProducto))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

    def cerrar(self):
        self.close()

class clientes(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(clientes,self).__init__(parent)
        uic.loadUi('UI/clientes.ui',self)

        self.bNuevo.clicked.connect(self.nuevo)
        self.bEditar.clicked.connect(self.editar)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bActualizar.clicked.connect(self.actualizar)
        
        self.clientes,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,18,self.clientes)
    
    def crearTabla(self,filas,columnas,datos):
        self.table_clientes.setRowCount(filas)
        self.table_clientes.setColumnCount(columnas)
        self.table_clientes.setHorizontalHeaderLabels(["ID","TIPO","NOMBRES", "PATERNO","MATERNO","RFC","CALLE","EXT","INT","CP","COLONIA","LOCALIDAD","CIUDAD","ESTADO","PAIS","TELEFONO","CELULAR","CORREO"])
        self.header = self.table_clientes.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range (0,self.filas):
            for j in range (0,18):
                self.table_clientes.setItem(i, j, QtWidgets.QTableWidgetItem(str(datos[i][j])))
    
    def consultarTodo(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT * FROM Clientes"
                    cursor.execute(sentencia)
                    clientes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        return clientes,len(clientes)
    
    def nuevo(self):
        cliente=nuevoCliente(self)
        cliente.show()
    
    def editar(self):
        if self.table_clientes.currentRow() >= 0:
            fila = self.table_clientes.currentRow()
            lista = []
            for i in range(0,len(self.clientes[fila])):
                lista.append(self.clientes[fila][i])
            update = updateCliente(self)
            update.setInfo(lista)
            update.show()
    
    def eliminar(self):
        if self.table_clientes.currentRow() >= 0:
            fila = self.table_clientes.currentRow()
            num = self.clientes[fila][0]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:    
                        cursor.execute("DELETE FROM Clientes WHERE cli_Id = '%s' " % (num))
                    conexion.commit()
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def actualizar(self):
        self.clientes,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,18,self.clientes)
    
class nuevoCliente(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevoCliente,self).__init__(parent)
        uic.loadUi('UI/nuevoCliente.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)
        
    def guardar(self):
        tipo = 0 if self.radioButton_fisica.isChecked() else 1
        nombres = self.line_nombres.text()
        paterno = self.line_paterno.text()
        materno = self.line_materno.text()
        rfc = self.line_rfc.text()
        calle = self.line_calle.text()
        exterior = self.line_ext.text()
        interior = self.line_int.text()
        codigoPostal = self.line_cp.text()
        colonia = self.line_colonia.text()
        localidad = self.line_localidad.text()
        ciudad = self.line_ciudad.text()
        estado = self.line_estado.text()
        pais = self.line_pais.text()
        telefono = self.line_telefono.text()
        celular = self.line_celular.text()
        correo = self.line_correo.text()

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Clientes (cli_Tipo,cli_Nombres,cli_Paterno,cli_Materno,cli_RFC,cli_Calle,cli_NumExt,cli_NumInt,cli_CP,cli_Col,cli_Localidad,cli_Ciudad,cli_Estado,cli_Pais,cli_Tel,cli_Cel,cli_Mail)"
                                    "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (tipo,nombres,paterno,materno,rfc,calle,exterior,interior,codigoPostal,colonia,localidad,ciudad,estado,pais,telefono,celular,correo))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.close()

class updateCliente(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(updateCliente,self).__init__(parent)
        uic.loadUi('UI/updateCliente.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

    def setInfo(self,lista):
        self.lista = lista
        self.num = lista[0]
        self.tipo = lista[1]
        self.nombres = lista[2]
        self.paterno = lista[3]
        self.materno = lista[4]
        self.rfc = lista[5]
        self.calle = lista[6]
        self.exterior = lista[7]
        self.interior = lista[8]
        self.codigoPostal = lista[9]
        self.colonia = lista[10]
        self.localidad = lista[11]
        self.ciudad = lista[12]
        self.estado = lista[13]
        self.pais = lista[14]
        self.telefono = lista[15]
        self.celular = lista[16]
        self.correo = lista[17]

        if self.tipo == 1:
            self.radioButton_fisica.isChecked(False)
            self.radioButton_moral.isChecked(True)
        self.line_nombres.setText(str(self.nombres))
        self.line_paterno.setText(str(self.paterno))
        self.line_materno.setText(str(self.materno))
        self.line_rfc.setText(str(self.rfc))
        self.line_calle.setText(str(self.calle))
        self.line_ext.setText(str(self.exterior))
        self.line_int.setText(str(self.interior))
        self.line_cp.setText(str(self.codigoPostal))
        self.line_colonia.setText(str(self.colonia))
        self.line_localidad.setText(str(self.localidad))
        self.line_ciudad.setText(str(self.ciudad))
        self.line_estado.setText(str(self.estado))
        self.line_pais.setText(str(self.pais))
        self.line_telefono.setText(str(self.telefono))
        self.line_celular.setText(str(self.celular))
        self.line_correo.setText(str(self.correo))


    def guardar(self):
        num = self.num
        tipo = 0 if self.radioButton_fisica.isChecked() else 1
        nombres = self.line_nombres.text()
        paterno = self.line_paterno.text()
        materno = self.line_materno.text()
        rfc = self.line_rfc.text()
        calle = self.line_calle.text()
        exterior = self.line_ext.text()
        interior = self.line_int.text()
        codigoPostal = self.line_cp.text()
        colonia = self.line_colonia.text()
        localidad = self.line_localidad.text()
        ciudad = self.line_ciudad.text()
        estado = self.line_estado.text()
        pais = self.line_pais.text()
        telefono = self.line_telefono.text()
        celular = self.line_celular.text()
        correo = self.line_correo.text()

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE Clientes SET cli_Tipo = '%s', cli_Nombres = '%s', cli_Paterno = '%s', cli_Materno = '%s', cli_RFC = '%s', cli_Calle = '%s', cli_NumExt = '%s', cli_NumInt = '%s', cli_CP = '%s', cli_Col = '%s', cli_Localidad = '%s', cli_Ciudad = '%s', cli_Estado = '%s', cli_Pais = '%s', cli_Tel = '%s', cli_Cel = '%s', cli_Mail = '%s' WHERE (`cli_Id` = %s)" % (tipo,nombres,paterno,materno,rfc,calle,exterior,interior,codigoPostal,colonia,localidad,ciudad,estado,pais,telefono,celular,correo,num))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

    def cerrar(self):
        self.close()

class almacenes(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(almacenes,self).__init__(parent)
        uic.loadUi('UI/almacenes.ui',self)

        self.bNuevo.clicked.connect(self.nuevo)
        self.bEditar.clicked.connect(self.editar)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bActualizar.clicked.connect(self.actualizar)
        
        self.almacenes,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,2,self.almacenes)
    
    def crearTabla(self,filas,columnas,datos):
        self.table_almacenes.setRowCount(filas)
        self.table_almacenes.setColumnCount(columnas)
        self.table_almacenes.setHorizontalHeaderLabels(["ID","NOMBRE"])
        self.header = self.table_almacenes.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        for i in range (0,self.filas):
            for j in range (0,2):
                self.table_almacenes.setItem(i, j, QtWidgets.QTableWidgetItem(str(datos[i][j])))
    
    def consultarTodo(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT * FROM Almacenes"
                    cursor.execute(sentencia)
                    almacenes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        return almacenes,len(almacenes)
    
    def nuevo(self):
        almacen=nuevoAlmacen(self)
        almacen.show()
    
    def editar(self):
        if self.table_almacenes.currentRow() >= 0:
            fila = self.table_almacenes.currentRow()
            num = self.almacenes[fila][0]
            nombre = self.almacenes[fila][1]
            update = updateAlmacen(self)
            update.setInfo(num,nombre)
            update.show()
    
    def eliminar(self):
        if self.table_almacenes.currentRow() >= 0:
            fila = self.table_almacenes.currentRow()
            num = self.almacenes[fila][0]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:    
                        cursor.execute("DELETE FROM Almacenes WHERE alma_Id = '%s' " % (num))
                    conexion.commit()
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def actualizar(self):
        self.almacenes,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,2,self.almacenes)

class nuevoAlmacen(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevoAlmacen,self).__init__(parent)
        uic.loadUi('UI/nuevoAlmacen.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

    def guardar(self):
        a = self.line_nombre.text()
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT alma_Nombre FROM Almacenes WHERE alma_Nombre='%s'" % (a))
                    almacenes = cursor.fetchall()
                    if len(almacenes)==0:
                        cursor.execute("INSERT INTO Almacenes (alma_Nombre) VALUES ('%s')" % (a))
                        conexion.commit()
                    else:
                        pass
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.close()

class updateAlmacen(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(updateAlmacen,self).__init__(parent)
        uic.loadUi('UI/updateAlmacen.ui',self)
        self.num = None
        self.nombre = None

        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

    def setInfo(self,num, nombre):
        self.num = num
        self.nombre = nombre
        self.line_id.setText(str(self.num))
        self.line_nombre.setText(self.nombre)
    
    def getInfo(self):
        return self.num,self.nombre

    def guardar(self):
        num,nombre = self.getInfo()
        if num >= 0:
            nuevoNombre = self.line_nombre.text()
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:
                        cursor.execute("SELECT alma_Nombre FROM Almacenes WHERE alma_Nombre='%s'" % (nuevoNombre))
                        almacenes = cursor.fetchall()
                        if len(almacenes)==0:
                            cursor.execute("UPDATE Almacenes SET alma_Nombre = '%s' WHERE ( alma_Id = '%s')" % (nuevoNombre,num))
                            conexion.commit()
                            self.cerrar()
                        else:
                            self.line_nombre.setText(nombre)
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def cerrar(self):
        self.close()

class proveedores(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(proveedores,self).__init__(parent)
        uic.loadUi('UI/proveedores.ui',self)

        self.bNuevo.clicked.connect(self.nuevo)
        self.bEditar.clicked.connect(self.editar)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bActualizar.clicked.connect(self.actualizar)
        
        self.proveedores,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,18,self.proveedores)
    
    def crearTabla(self,filas,columnas,datos):
        self.table_proveedores.setRowCount(filas)
        self.table_proveedores.setColumnCount(columnas)
        self.table_proveedores.setHorizontalHeaderLabels(["ID","TIPO","NOMBRES", "PATERNO","MATERNO","RFC","CALLE","EXT","INT","CP","COLONIA","LOCALIDAD","CIUDAD","ESTADO","PAIS","TELEFONO","CELULAR","CORREO"])
        self.header = self.table_proveedores.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range (0,self.filas):
            for j in range (0,18):
                self.table_proveedores.setItem(i, j, QtWidgets.QTableWidgetItem(str(datos[i][j])))
    
    def consultarTodo(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT * FROM Proveedores"
                    cursor.execute(sentencia)
                    proveedores = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        return proveedores,len(proveedores)
    
    def nuevo(self):
        proveedor=nuevoProveedor(self)
        proveedor.show()
    
    def editar(self):
        if self.table_proveedores.currentRow() >= 0:
            fila = self.table_proveedores.currentRow()
            lista = []
            for i in range(0,len(self.proveedores[fila])):
                lista.append(self.proveedores[fila][i])
            update = updateProveedor(self)
            update.setInfo(lista)
            update.show()
    
    def eliminar(self):
        if self.table_proveedores.currentRow() >= 0:
            fila = self.table_proveedores.currentRow()
            num = self.proveedores[fila][0]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:    
                        cursor.execute("DELETE FROM Proveedores WHERE prov_Id = '%s' " % (num))
                    conexion.commit()
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def actualizar(self):
        self.proveedores,self.filas = self.consultarTodo()
        self.crearTabla(self.filas,18,self.proveedores)

class nuevoProveedor(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevoProveedor,self).__init__(parent)
        uic.loadUi('UI/nuevoProveedor.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)
    
    def guardar(self):
        tipo = 0 if self.radioButton_fisica.isChecked() else 1
        nombres = self.line_nombres.text()
        paterno = self.line_paterno.text()
        materno = self.line_materno.text()
        rfc = self.line_rfc.text()
        calle = self.line_calle.text()
        exterior = self.line_ext.text()
        interior = self.line_int.text()
        codigoPostal = self.line_cp.text()
        colonia = self.line_colonia.text()
        localidad = self.line_localidad.text()
        ciudad = self.line_ciudad.text()
        estado = self.line_estado.text()
        pais = self.line_pais.text()
        telefono = self.line_telefono.text()
        celular = self.line_celular.text()
        correo = self.line_correo.text()

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Proveedores (prov_Tipo,prov_Nombres,prov_Paterno,prov_Materno,prov_RFC,prov_Calle,prov_NumExt,prov_NumInt,prov_CP,prov_Col,prov_Localidad,prov_Ciudad,prov_Estado,prov_Pais,prov_Tel,prov_Cel,prov_Mail)"
                                    "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (tipo,nombres,paterno,materno,rfc,calle,exterior,interior,codigoPostal,colonia,localidad,ciudad,estado,pais,telefono,celular,correo))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.close()

class updateProveedor(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(updateProveedor,self).__init__(parent)
        uic.loadUi('UI/updateProveedor.ui',self)
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)

    def setInfo(self,lista):
        self.lista = lista
        self.num = lista[0]
        self.tipo = lista[1]
        self.nombres = lista[2]
        self.paterno = lista[3]
        self.materno = lista[4]
        self.rfc = lista[5]
        self.calle = lista[6]
        self.exterior = lista[7]
        self.interior = lista[8]
        self.codigoPostal = lista[9]
        self.colonia = lista[10]
        self.localidad = lista[11]
        self.ciudad = lista[12]
        self.estado = lista[13]
        self.pais = lista[14]
        self.telefono = lista[15]
        self.celular = lista[16]
        self.correo = lista[17]

        if self.tipo == 1:
            self.radioButton_fisica.isChecked(False)
            self.radioButton_moral.isChecked(True)
        self.line_nombres.setText(str(self.nombres))
        self.line_paterno.setText(str(self.paterno))
        self.line_materno.setText(str(self.materno))
        self.line_rfc.setText(str(self.rfc))
        self.line_calle.setText(str(self.calle))
        self.line_ext.setText(str(self.exterior))
        self.line_int.setText(str(self.interior))
        self.line_cp.setText(str(self.codigoPostal))
        self.line_colonia.setText(str(self.colonia))
        self.line_localidad.setText(str(self.localidad))
        self.line_ciudad.setText(str(self.ciudad))
        self.line_estado.setText(str(self.estado))
        self.line_pais.setText(str(self.pais))
        self.line_telefono.setText(str(self.telefono))
        self.line_celular.setText(str(self.celular))
        self.line_correo.setText(str(self.correo))


    def guardar(self):
        num = self.num
        tipo = 0 if self.radioButton_fisica.isChecked() else 1
        nombres = self.line_nombres.text()
        paterno = self.line_paterno.text()
        materno = self.line_materno.text()
        rfc = self.line_rfc.text()
        calle = self.line_calle.text()
        exterior = self.line_ext.text()
        interior = self.line_int.text()
        codigoPostal = self.line_cp.text()
        colonia = self.line_colonia.text()
        localidad = self.line_localidad.text()
        ciudad = self.line_ciudad.text()
        estado = self.line_estado.text()
        pais = self.line_pais.text()
        telefono = self.line_telefono.text()
        celular = self.line_celular.text()
        correo = self.line_correo.text()

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("UPDATE Proveedores SET prov_Tipo = '%s', prov_Nombres = '%s', prov_Paterno = '%s', prov_Materno = '%s', prov_RFC = '%s', prov_Calle = '%s', prov_NumExt = '%s', prov_NumInt = '%s', prov_CP = '%s', prov_Col = '%s', prov_Localidad = '%s', prov_Ciudad = '%s', prov_Estado = '%s', prov_Pais = '%s', prov_Tel = '%s', prov_Cel = '%s', prov_Mail = '%s' WHERE (`prov_Id` = %s)" % (tipo,nombres,paterno,materno,rfc,calle,exterior,interior,codigoPostal,colonia,localidad,ciudad,estado,pais,telefono,celular,correo,num))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

    def cerrar(self):
        self.close()

class salidas(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(salidas,self).__init__(parent)
        uic.loadUi('UI/salidas.ui',self)
        self.bSalir.clicked.connect(self.cerrar)
    
    def cerrar(self):
        self.close()

class entradas(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(entradas,self).__init__(parent)
        uic.loadUi('UI/entradas.ui',self)
        self.bSalir.clicked.connect(self.cerrar)
    
    def cerrar(self):
        self.close()

app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec()