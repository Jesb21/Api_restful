import pymysql

try:
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="eilaeila2106",
        database="api_restful"
    )
    print("✅ Conexión exitosa a la base de datos")
except pymysql.MySQLError as e:
    print(f"❌ Error al conectar a MySQL: {e}")