import pymysql

#Licencias Base de Datos
_host='localhost'
_user='root'
_password='gafo951101'
_db='PuntoVenta'

try:
  conexion = pymysql.connect(host=_host,user=_user,password=_password,db=_db)
  try:
    with conexion.cursor() as cursor:
      cursor.execute("SELECT prov_Id,prov_Nombres,prov_Paterno,prov_Materno FROM Proveedores")
      proveedores = cursor.fetchall()
      cursor.execute("SELECT * FROM Almacenes")
      almacenes = cursor.fetchall() 
  finally:
    conexion.close()
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
  print("Ocurrió un error al conectar: ", e)

listaProveedores = []
listaAlmacenes = []
for i in range(0,len(proveedores)):
  nombre = proveedores[i][2]
  listaProveedores.append(nombre)

print (listaProveedores)

