# -*- coding: utf-8 -*-
import sys
import pymysql
import imagenes.imagenes
import datetime
from PyQt5 import QtWidgets,uic
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

#Licencias Base de Datos
_host='localhost'
_user='root'
_password='gafo951101'
_db='PuntoVenta'

class login(QtWidgets.QMainWindow):
    def __init__(self):
        super(login,self).__init__()
        uic.loadUi('UI/login.ui',self)
        self.show()
        self.button_iniciar.clicked.connect(self.clicIniciar)
        self.bNuevo.clicked.connect(self.abrirNuevo)
        self.bRecordar.clicked.connect(self.abrirRecordar)

        self.llenarComboBox()

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
                        otraventana=ventanaPrincipal(self)
                        otraventana.setNombreHeader(vendedores[0][3].title())
                        otraventana.setAlmacenVentas(self.almacenes[self.comboBox_almacenes.currentIndex()][0])
                        otraventana.show()
                    else: 
                        self.line_usuario.clear()
                        self.line_contrasena.clear()  
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def llenarComboBox(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Almacenes")
                    self.almacenes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        self.listaAlmacenes = []
        for i in range(0,len(self.almacenes)):
            self.listaAlmacenes.append(self.almacenes[i][1])
        self.comboBox_almacenes.addItems(self.listaAlmacenes)

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

class ventanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(ventanaPrincipal,self).__init__(parent)
        uic.loadUi('UI/mainWindow.ui',self)

        self.SS = vender(self.body)
        self.wProductos = productos(self.body)
        self.wClientes = clientes(self.body)
        self.wAlmacenes = almacenes(self.body)
        self.wProveedores = proveedores(self.body)
        self.wSalidas = salidas(self.body)
        self.wEntradas = entradas(self.body)
        self.wReportes = reportes(self.body)

        self.almacenVentas = None
        self.refreshBody()

        self.bVender.clicked.connect(self.abrirVender)
        self.bProductos.clicked.connect(self.abrirProductos)
        self.bClientes.clicked.connect(self.abrirClientes)
        self.bAlmacenes.clicked.connect(self.abrirAlmacenes)
        self.bProveedores.clicked.connect(self.abrirProveedores)
        self.bSalidas.clicked.connect(self.abrirSalidas)
        self.bEntradas.clicked.connect(self.abrirEntradas)
        self.bReportes.clicked.connect(self.abrirReportes)
        self.bSalir.clicked.connect(self.cerrar)

    def setNombreHeader(self,nombre):
        self.label_header.setText("Bienvenido %s" % (nombre))

    def abrirVender(self):
        self.refreshBody()
        self.wVender.setAlmacenVentas(self.almacenVentas)
        self.wVender.actualizar()
        self.wVender.show()

    def abrirProductos(self):
        self.refreshBody()
        self.wProductos.actualizar()
        self.wProductos.show()

    def abrirClientes(self):
        self.refreshBody()
        self.wClientes.actualizar()
        self.wClientes.show()

    def abrirAlmacenes(self):
        self.refreshBody()
        self.wAlmacenes.actualizar()
        self.wAlmacenes.show()

    def abrirProveedores(self):
        self.refreshBody()
        self.wProveedores.actualizar()
        self.wProveedores.show()

    def abrirSalidas(self):
        self.refreshBody()
        self.wSalidas.actualizar()
        self.wSalidas.show()

    def abrirEntradas(self):
        self.refreshBody()
        self.wEntradas.actualizar()
        self.wEntradas.show()

    def abrirReportes(self):
        self.refreshBody()
        self.wReportes.show()

    def refreshBody(self):
        self.wVender.close()
        self.wProductos.close()
        self.wClientes.close()
        self.wAlmacenes.close()
        self.wProveedores.close()
        self.wSalidas.close()
        self.wEntradas.close()
        self.wReportes.close()

    def setAlmacenVentas(self,almacen):
        self.almacenVentas = almacen

    def cerrar(self):
        self.wProductos.close()
        self.wVender.close()
        self.parent().show()
        self.close()

class vender(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(vender,self).__init__(parent)
        uic.loadUi('UI/vender.ui',self)

        self.tableList = []
        self.almacenVentas = None

        self.line_Ccli.editingFinished.connect(self.buscarCliente)
        self.line_Cbarras.editingFinished.connect(self.buscarProducto)
        self.bAgregar.clicked.connect(self.agregar)
        self.bGuardar.clicked.connect(self.guardar)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bNueva.clicked.connect(self.actualizar)

    def setAlmacenVentas(self,almacen):
        self.almacenVentas = almacen
    
    def buscarCliente(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Clientes WHERE cli_Id='%s'" % (self.line_Ccli.text()))
                    self.clientes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        if len(self.clientes)==1:
            self.line_cli.setText(self.clientes[0][2])
            self.num = self.clientes[0][0]
        else:
            self.line_cli.setText("NO EXISTE")

    def buscarProducto(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Productos WHERE prod_CodBarras='%s' and prod_IdAlmacen='%s'" % (self.line_Cbarras.text(),self.almacenVentas))
                    self.productos = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        if len(self.productos)==1:
            self.line_producto.setText(self.productos[0][2])
            self.num = self.productos[0][0]
        else:
            self.line_producto.setText("NO EXISTE")
    

    
    def crearTabla(self):
        self.table_vender.clear()
        filas = len(self.tableList)
        self.table_vender.setRowCount(filas)
        self.table_vender.setColumnCount(5)
        self.table_vender.setHorizontalHeaderLabels(["CB","NOMBRE","P/U","C","$"])
        self.header = self.table_vender.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range (0,filas):
            for j in range (1,6):
                self.table_vender.setItem(i, j-1, QtWidgets.QTableWidgetItem(str(self.tableList[i][j])))
        
        self.total()
    
    def total(self):
        self.line_total.clear()
        suma = 0
        for i in range (0,len(self.tableList)):
            suma += self.tableList[i][5]
        
        self.totalNota = suma
        self.line_total.setText("$"+str(suma))

    def agregar(self):
        if ((not self.line_producto.text()) or
            (self.line_producto.text()=="NO EXISTE") or
            (not self.line_Cbarras.text()) or
            (not self.line_cantidad.text()) or
            (int(self.line_cantidad.text())<=0)):
            pass
        else:
            codigo = self.line_Cbarras.text()
            cantidad = int(self.line_cantidad.text())
            self.line_Cbarras.clear()
            self.line_cantidad.clear()
            self.line_producto.clear()
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:
                        cursor.execute("SELECT prod_Id,prod_CodBarras,prod_Nombre,prod_Precio,prod_IdAlmacen FROM PuntoVenta.Productos WHERE prod_CodBarras=%s" % (codigo))
                        producto = cursor.fetchall() 
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)
            
            productoLista = list(producto[0])
            self.tableList.append(productoLista)
            self.tableList[-1].insert(4,int(cantidad))
            self.tableList[-1].insert(5,(self.tableList[-1][4]*self.tableList[-1][3]))
            self.crearTabla()
    
    def guardar(self):
        if ((not self.line_Ccli.text()) or
            (not self.line_cli.text()) or
            (self.line_cli.text() == "NO EXISTE") or
            (len(self.tableList) == 0)):
            pass
        else:
            nota = []
            nota.append(self.line_folio.text())
            nota.append(self.line_Ccli.text())
            nota.append(self.almacenVentas)
            nota.append(self.totalNota)
            nota.append(self.fechaHora)
            ventanaPagar=pagar(self)
            ventanaPagar.setInfo(self.tableList,nota)
            ventanaPagar.show()

    def eliminar(self):
        if self.table_vender.currentRow() >= 0:
            fila = self.table_vender.currentRow()
            self.tableList.pop(fila)
        
        self.crearTabla() 

    def actualizar(self):
        self.line_Ccli.clear()
        self.line_cli.clear()
        self.line_Cbarras.clear()
        self.line_producto.clear()
        self.line_fecha.clear()
        self.line_folio.clear()
        self.line_cantidad.clear()
        self.table_vender.clear()

        self.definirFecha()
        self.definirFolio()
        self.tableList.clear()
        self.crearTabla()
    
    def definirFecha(self):
        self.fechaHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        self.line_fecha.setText(self.fecha)
    
    def definirFolio(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Notas")
                    notas = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        if len(notas) == 0:
            folio = 1
            self.line_folio.setText("Nota - "+str(folio))
        else:
            folio = notas[-1][0]+1
            self.line_folio.setText("Nota - "+str(folio))

class pagar(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(pagar,self).__init__(parent)
        uic.loadUi('UI/pagar.ui',self)
        self.bGuardar.clicked.connect(self.guardar)

        self.metodosPago = ["Efectivo","Tarjeta","Transferencia"]
        self.nota = []

        self.llenarComboBox()
    
    def llenarComboBox(self):
        self.comboBox_metodosPago.addItems(self.metodosPago)
    
    def setInfo(self,datosSalidas,datosNota):
        self.salidas = datosSalidas
        self.nota = datosNota
        self.line_cantidadPagar.setText(str(self.nota[3]))
    
    def guardarNota(self):
        #Datos para salidas:  [[6, 123, 'BalanXC Supreme', 750.0, 2, 1500.0, 10]]
        #Datos para nota:  ['Nota - 1', '1', 10, 1500.0, '2020-04-10 14:18:32']
        codigo = self.nota[0]
        cliente = self.nota[1]
        almacen = self.nota[2]
        total = self.nota[3]
        formaPago = self.metodosPago[self.comboBox_metodosPago.currentIndex()]
        fechaHora = self.nota[4]

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Notas (note_codigo,note_IdCli,note_IdAlma,note_Total,note_formaPago,note_FechaHora)"
                                    "VALUES ('%s','%s','%s','%s','%s','%s')" % (codigo,cliente,almacen,total,formaPago,fechaHora))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

    def guardarSalida(self):

        for salida in self.salidas:
            almacen = salida[6]
            producto = salida[0]
            cantidad = salida[4]
            motivo = self.nota[0]
            fechaHora = self.nota[4]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:
                        cursor.execute("INSERT INTO Salidas (sal_IdAlma,sal_IdProd,sal_Cantidad,sal_Motivo,sal_FechaHora,sal_estado)"
                                        "VALUES ('%s','%s','%s','%s','%s','%s')" % (almacen,producto,cantidad,motivo,fechaHora,1))
                        cursor.execute("UPDATE Productos SET prod_existencias=(prod_existencias-%s) WHERE prod_Id='%s'" % (cantidad,producto))
                        conexion.commit()
                finally:
                    conexion.close()
                    self.cerrar()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def guardar(self):
        if float(self.line_cantidadPagada.text()) == float(self.line_cantidadPagar.text()):
            self.guardarNota()
            self.guardarSalida()
            pdf = notaPdf(self.nota,self.salidas)
            pdf.go()
            self.cerrar()
        else:
            print("No paso")
    
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
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
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

        self.bNuevo.clicked.connect(self.nuevo)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bActualizar.clicked.connect(self.actualizar)
        
        self.salidas,self.filas= self.consultarTodo()
        self.crearTabla(self.filas,7,self.salidas)
    
    def crearTabla(self,filas,columnas,datos):
        self.table_salidas.setRowCount(filas)
        self.table_salidas.setColumnCount(columnas)
        self.table_salidas.setHorizontalHeaderLabels(["ID","ALMACEN","PRODUCTO", "CANTIDAD","MOTIVO","FECHA & HORA","ESTADO"])
        self.header = self.table_salidas.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range (0,self.filas):
            for j in range (0,7):
                self.table_salidas.setItem(i, j, QtWidgets.QTableWidgetItem(str(datos[i][j])))
    
    def consultarTodo(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT * FROM Salidas WHERE sal_estado = 1"
                    cursor.execute(sentencia)
                    salidas = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        return salidas,len(salidas)
    
    def nuevo(self):
        salida=nuevaSalida(self)
        salida.show()
    
    def eliminar(self):
        if self.table_salidas.currentRow() >= 0:
            fila = self.table_salidas.currentRow()
            num = self.salidas[fila][0]
            producto = self.salidas[fila][2]
            cantidad = self.salidas[fila][3]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:    
                        cursor.execute("UPDATE Salidas SET sal_estado = '%s' WHERE ( sal_Id = '%s')" % (0,num))
                        cursor.execute("UPDATE Productos SET prod_existencias=(prod_existencias+%s) WHERE prod_Id='%s'" % (cantidad,producto))
                    conexion.commit()
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def actualizar(self):
        self.salidas,self.filas= self.consultarTodo()
        self.crearTabla(self.filas,7,self.salidas)

class nuevaSalida(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevaSalida,self).__init__(parent)
        uic.loadUi('UI/nuevaSalida.ui',self)
        
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)
        self.line_Cbarras.editingFinished.connect(self.buscarProducto)

        self.llenarComboBox()
    
    def llenarComboBox(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Almacenes")
                    self.almacenes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        listaAlmacenes = []
        for i in range(0,len(self.almacenes)):
            listaAlmacenes.append(self.almacenes[i][1])
        self.comboBox_almacen.addItems(listaAlmacenes)
    
    def buscarProducto(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Productos WHERE prod_CodBarras='%s'" % (self.line_Cbarras.text()))
                    self.productos = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        if len(self.productos)==1:
            self.line_nombre.setText(self.productos[0][2])
            self.num = self.productos[0][0]
        else:
            self.line_nombre.setText("No Existe !!!!!!!!")

    def guardar(self):
        almacen = self.almacenes[self.comboBox_almacen.currentIndex()][0]
        producto = self.num
        cantidad = self.line_cantidad.text()
        motivo = self.line_motivo.text()
        fechaHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Salidas (sal_IdAlma,sal_IdProd,sal_Cantidad,sal_Motivo,sal_FechaHora,sal_estado)"
                                    "VALUES ('%s','%s','%s','%s','%s','%s')" % (almacen,producto,cantidad,motivo,fechaHora,1))
                    cursor.execute("UPDATE Productos SET prod_existencias=(prod_existencias-%s) WHERE prod_Id='%s'" % (cantidad,producto))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.close()

class entradas(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(entradas,self).__init__(parent)
        uic.loadUi('UI/entradas.ui',self)

        self.bNuevo.clicked.connect(self.nuevo)
        self.bEliminar.clicked.connect(self.eliminar)
        self.bActualizar.clicked.connect(self.actualizar)
        
        self.entradas, self.filas = self.consultarTodo()
        self.crearTabla(self.filas,7,self.entradas)
    
    def crearTabla(self,filas,columnas,datos):
        self.table_entradas.setRowCount(filas)
        self.table_entradas.setColumnCount(columnas)
        self.table_entradas.setHorizontalHeaderLabels(["ID","ALMACEN","PRODUCTO", "CANTIDAD","MOTIVO","FECHA & HORA","ESTADO"])
        self.header = self.table_entradas.horizontalHeader()
        self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range (0,self.filas):
            for j in range (0,7):
                self.table_entradas.setItem(i, j, QtWidgets.QTableWidgetItem(str(datos[i][j])))
    
    def consultarTodo(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    sentencia = "SELECT * FROM Entradas WHERE ent_estado = 1"
                    cursor.execute(sentencia)
                    entradas = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

        return entradas, len(entradas)

    
    def nuevo(self):
        entrada=nuevaEntrada(self)
        entrada.show()
    
    def eliminar(self):
        if self.table_entradas.currentRow() >= 0:
            fila = self.table_entradas.currentRow()
            num = self.entradas[fila][0]
            producto = self.entradas[fila][2]
            cantidad = self.entradas[fila][3]
            try:
                conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
                try:
                    with conexion.cursor() as cursor:    
                        cursor.execute("UPDATE Entradas SET ent_estado = '%s' WHERE ( ent_Id = '%s')" % (0,num))
                        cursor.execute("UPDATE Productos SET prod_existencias=(prod_existencias-%s) WHERE prod_Id='%s'" % (cantidad,producto))
                    conexion.commit()
                finally:
                    conexion.close()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                print("Ocurrió un error al conectar: ", e)

    def actualizar(self):
        self.entradas,self.filas= self.consultarTodo()
        self.crearTabla(self.filas,7,self.entradas)

class nuevaEntrada(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(nuevaEntrada,self).__init__(parent)
        uic.loadUi('UI/nuevaEntrada.ui',self)
        
        self.bGuardar.clicked.connect(self.guardar)
        self.bSalir.clicked.connect(self.cerrar)
        self.line_Cbarras.editingFinished.connect(self.buscarProducto)

        self.llenarComboBox()
    
    def llenarComboBox(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Almacenes")
                    self.almacenes = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        listaAlmacenes = []
        for i in range(0,len(self.almacenes)):
            listaAlmacenes.append(self.almacenes[i][1])
        self.comboBox_almacen.addItems(listaAlmacenes)
    
    def buscarProducto(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Productos WHERE prod_CodBarras='%s'" % (self.line_Cbarras.text()))
                    self.productos = cursor.fetchall() 
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        if len(self.productos)==1:
            self.line_nombre.setText(self.productos[0][2])
            self.num = self.productos[0][0]
        else:
            self.line_nombre.setText("No Existe !!!!!!!!")

    def guardar(self):
        almacen = self.almacenes[self.comboBox_almacen.currentIndex()][0]
        producto = self.num
        cantidad = self.line_cantidad.text()
        motivo = self.line_motivo.text()
        fechaHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Entradas (ent_IdAlma,ent_IdProd,ent_Cantidad,ent_Motivo,ent_FechaHora,ent_estado)"
                                    "VALUES ('%s','%s','%s','%s','%s','%s')" % (almacen,producto,cantidad,motivo,fechaHora,1))
                    cursor.execute("UPDATE Productos SET prod_existencias=(prod_existencias+%s) WHERE prod_Id='%s'" % (cantidad,producto))
                    conexion.commit()
            finally:
                conexion.close()
                self.cerrar()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
    
    def cerrar(self):
        self.close()

class reportes(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(reportes,self).__init__(parent)
        uic.loadUi('UI/reportes.ui',self)

        self.bProductos.clicked.connect(self.reporteProductos)
        self.bClientes.clicked.connect(self.reporteClientes)
        self.bProveedores.clicked.connect(self.reporteProveedores)
        self.bAlmacenes.clicked.connect(self.reporteAlmacenes)

    def reporteProductos(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT prod_Id,prod_CodBarras,prod_Nombre,prod_existencias,prod_Costo,prod_Precio FROM Productos")
                    productos = cursor.fetchall()
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
        
        productos2=list(productos)
        productos2.insert(0,("ID","CODIGO","NOMBRE","EXISTENCIAS","COSTO","PRECIO"))
        reporte1 = reporte("ProductsReport","Listado de Productos",productos2)
        reporte1.go()
        del reporte1

    def reporteClientes(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT cli_Id,cli_Nombres,cli_Paterno,cli_Materno,cli_RFC,cli_Ciudad,cli_Estado,cli_Pais FROM Clientes")
                    clientes = cursor.fetchall()
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
            
        clientes2=list(clientes)
        clientes2.insert(0,("ID","NOMBRES","PATERNO","MATERNO","RFC","CIUDAD","ESTADO","PAIS"))
        reporte1 = reporte("ClientsReport","Listado de Clientes",clientes2)
        reporte1.go()
        del reporte1

    def reporteProveedores(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT prov_Id,prov_Nombres,prov_Paterno,prov_Materno,prov_RFC,prov_Ciudad,prov_Estado,prov_Pais FROM Proveedores")
                    proveedores = cursor.fetchall()
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
            
        proveedores2=list(proveedores)
        proveedores2.insert(0,("ID","NOMBRES","PATERNO","MATERNO","RFC","CIUDAD","ESTADO","PAIS"))
        reporte1 = reporte("ProvidersReport","Listado de Proveedores",proveedores2)
        reporte1.go()
        del reporte1

    def reporteAlmacenes(self):
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Almacenes")
                    almacenes = cursor.fetchall()
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)
            
        almacenes2=list(almacenes)
        almacenes2.insert(0,("ID","NOMBRE"))
        reporte1 = reporte("WarehousesReport","Listado de Almacenes",almacenes2)
        reporte1.go()
        del reporte1
    
class reporte():
    def __init__(self,nombreReporte,titulo,datos):
        self.PAGE_HEIGHT=letter[1]; self.PAGE_WIDTH=letter[0]
        self.pageinfo = " |  StoreSoft"
        self.datos = datos
        self.titutlo = titulo
        self.nombreReporte = nombreReporte

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        #Cabecera ------------------------------------
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,self.PAGE_HEIGHT+30,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #Fin de cabecera ---------------------------------
        #Pie de pagina -----------------------------------
        canvas.setFillColorRGB(.2196,.2196,.2196)
        canvas.setFont('Helvetica-Bold',20)
        canvas.drawCentredString(self.PAGE_WIDTH/2, 700, "%s" % (self.titutlo))
        canvas.setFont('Helvetica',9)
        canvas.drawCentredString(self.PAGE_WIDTH/2, 50, "Página %d %s" % (doc.page, self.pageinfo))
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,0,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #-------------------------------------------------
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        #Cabecera ------------------------------------
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,self.PAGE_HEIGHT+30,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #Fin de cabecera ---------------------------------
        #Pie de pagina -----------------------------------
        canvas.setFillColorRGB(.2196,.2196,.2196)
        canvas.setFont('Helvetica',9)
        canvas.drawCentredString(self.PAGE_WIDTH/2, 50, "Página %d %s" % (doc.page, self.pageinfo))
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,0,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #-------------------------------------------------
        canvas.restoreState()
    
    def hacerTabla(self):
        tabla = Table(self.datos)
        tabla.setStyle(TableStyle([ 
            ('FONT',(0,0),(-1,0),'Helvetica-Bold'),
            ('BACKGROUND',(0,0),(-1,0),(.6588,0,.0627)),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN',(0,0),(-1,0),'CENTER'),
            ('TEXTCOLOR',(0,1),(-1,-1),(.2196,.2196,.2196))]))
        
        for i in range(1, len(self.datos)):
            if i % 2 == 0:
                bc = (.80,.80,.80)
            else:
                bc = colors.white
        
            ts = TableStyle(
                [('BACKGROUND',(0,i),(-1,i),bc)]
                )
            tabla.setStyle(ts)
        return tabla
    
    def go(self):
        doc = SimpleDocTemplate("ReportesPdf/%s" % (self.nombreReporte))
        Story = [Spacer(1,150)]
        tabla = self.hacerTabla()
        Story.append(tabla)
        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)

class notaPdf:
    
    def __init__(self,nota, salidas):
        self.PAGE_HEIGHT=letter[1]; self.PAGE_WIDTH=letter[0]
        self.pageinfo = " |  StoreSoft"
        self.nota = nota
        self.salidas = salidas

    def myFirstPage(self,canvas, doc):
        canvas
        canvas.saveState()
        #Cabecera ------------------------------------
        nombre = "TIENDA DON LUIS"
        rfc = "XXXX010101"
        calle ="Av. Plan de San Luis"
        ext ="1820"
        inte = " "
        col = "Chapultepec Country"
        cp = "44620"
        ciudad = "Guadalajara"
        estado = "Jalisco"
        pais = "México"
        canvas.setStrokeColorRGB(.6588,0,.0627)
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,self.PAGE_HEIGHT-70,self.PAGE_WIDTH, 120,fill=True,stroke=False)

        canvas.drawImage("imagenes/logoNota.png", self.PAGE_WIDTH-170, self.PAGE_HEIGHT-40, width=120, height=60)

        canvas.setFillColorRGB(1,1,1)
        canvas.setFont("Helvetica", 12)
        cabecera = canvas.beginText(50, self.PAGE_HEIGHT+10)
        cabecera.textLines("%s\n%s\nAv. %s No.%s Int.%s\nCol. %s, C.P. %s\n%s, %s, %s." % (nombre, rfc, calle, ext, inte, col, cp, ciudad, estado, pais))
        canvas.drawText(cabecera)
        #Fin de cabecera ---------------------------------
        #Info Cliente ------------------------------------
        try:
            conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM Clientes WHERE cli_Id='%s'" % (self.nota[1]))
                    cliente = cursor.fetchall()
                    if len(cliente)==1:
                        nombre = cliente[0][2]+cliente[0][3]+cliente[0][4]
                        rfc = cliente[0][5]
                        calle = cliente[0][6]
                        ext =cliente[0][7]
                        inte = cliente[0][8]
                        col = cliente[0][10]
                        cp = cliente[0][9]
                        ciudad = cliente[0][12]
                        estado = cliente[0][3]
                        pais = cliente[0][14]
                    else:
                        nombre = "N/A"
                        rfc = "N/A"
                        calle = "N/A"
                        ext = "N/A"
                        inte = "N/A"
                        col = "N/A"
                        cp = "N/A"
                        ciudad = "N/A"
                        estado = "N/A"
                        pais = "N/A"
            finally:
                conexion.close()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error al conectar: ", e)

        codigoNota = self.nota[0]
        fechaHora = self.nota[4]
        canvas.setFillColorRGB(.2196,.2196,.2196)
        canvas.setFont("Helvetica", 12)
        cliente = canvas.beginText(50, 630+70)
        cliente.textLines("%s\n%s\nAv. %s No.%s Int.%s\nCol. %s, C.P. %s\n%s, %s, %s." % (nombre, rfc, calle, ext, inte, col, cp, ciudad, estado, pais))
        canvas.drawText(cliente)

        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.setFont("Helvetica-Bold", 15)
        canvas.drawRightString(self.PAGE_WIDTH-50,630+70,"%s" %(codigoNota))
        canvas.setFillColorRGB(.2196,.2196,.2196)
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawRightString(self.PAGE_WIDTH-50,590+70,"Fecha y Hora:")
        canvas.setFont("Helvetica", 12)
        canvas.drawRightString(self.PAGE_WIDTH-50,575+70,"%s" % (fechaHora))
        #-------------------------------------------------
        #Pie de pagina -----------------------------------
        canvas.setFont('Helvetica',9)
        canvas.drawCentredString(self.PAGE_WIDTH/2, 50, "Página %d %s" % (doc.page, self.pageinfo))
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,0,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #-------------------------------------------------
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        #Cabecera ------------------------------------
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,self.PAGE_HEIGHT+30,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #Fin de cabecera ---------------------------------
        #Pie de pagina -----------------------------------
        canvas.setFillColorRGB(.2196,.2196,.2196)
        canvas.setFont('Helvetica',9)
        canvas.drawCentredString(self.PAGE_WIDTH/2, 50, "Página %d %s" % (doc.page, self.pageinfo))
        canvas.setFillColorRGB(.6588,0,.0627)
        canvas.rect(0,0,self.PAGE_WIDTH, 20,fill=True,stroke=False)
        #-------------------------------------------------
        canvas.restoreState()

    def hacerTabla(self):
            #Datos para salidas:  [[6, 123, 'BalanXC Supreme', 750.0, 2, 1500.0, 10]]
            #Datos para nota:  ['Nota - 1', '1', 10, 1500.0, '2020-04-10 14:18:32']
        salida = []
        datos = [["CANTIDAD","                       NOMBRE                       ","  P/U  ","TOTAL"]]
        for i in range(0,len(self.salidas)):
            salida.append(self.salidas[i][4])
            salida.append(self.salidas[i][2])
            salida.append(self.salidas[i][3])
            salida.append(self.salidas[i][5])
            datos.append(salida)
            salida=[]
        total = [" "," ","TOTAL:",str(self.nota[3])]
        datos.append(total)

        tabla = Table(datos)
        tabla.setStyle(TableStyle([ 
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('FONT',(0,0),(-1,0),'Helvetica-Bold'),
            ('BACKGROUND',(0,0),(-1,0),(.6588,0,.0627)),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('FONT',(2,-1),(-1,-1),'Helvetica-Bold'),
            ('BACKGROUND',(2,-1),(-1,-1),(.6588,0,.0627)),
            ('TEXTCOLOR',(2,-1),(-1,-1),colors.white),
            ('TEXTCOLOR',(0,1),(-2,-2),(.2196,.2196,.2196)),
            ('ALIGN',(0,0),(-1,0),'CENTER'),
            ('ALIGN',(0,1),(1,-2),'CENTER'),
            ('ALIGN',(2,1),(3,-1),'RIGHT'),]))
        
        for i in range(1, len(datos)-1):
            if i % 2 == 0:
                bc = (.80,.80,.80)
            else:
                bc = colors.white
        
            ts = TableStyle(
                [('BACKGROUND',(0,i),(-1,i),bc)]
                )
            tabla.setStyle(ts)
        return tabla

    def go(self):
        doc = SimpleDocTemplate("NotasDeVentaPdf/%s" % (self.nota[0]))
        Story = [Spacer(1,150)]
        tabla = self.hacerTabla()
        Story.append(tabla)
        doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)


app = QtWidgets.QApplication(sys.argv)
window = login()
app.exec()