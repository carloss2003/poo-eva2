import mysql.connector
from datetime import datetime

# Clase base para la conexión a la base de datos
class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="", database="ejercicio"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return None

# Clase para manejar usuarios, hereda de DatabaseConnection
class User(DatabaseConnection):
    def registrar(self, username, password):
        db = self.conectar()  
        if db is None:
            return  

        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO login_user (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            print("Usuario registrado con éxito.")
        except mysql.connector.IntegrityError:
            print("El nombre de usuario ya existe. Por favor, elige otro.")
        finally:
            cursor.close()
            db.close()

    def iniciar_sesion(self, username, password):
        db = self.conectar()  
        if db is None:
            return None  

        cursor = db.cursor()
        cursor.execute("SELECT * FROM login_user WHERE username = %s AND password = %s", (username, password))
        usuario = cursor.fetchone()
        cursor.close()
        db.close()
        return usuario

# Clase para manejar ejercicios, hereda de DatabaseConnection
class Exercise(DatabaseConnection):
    def obtener_tipos(self):
        db = self.conectar()  
        if db is None:
            print("No se pudo conectar a la base de datos.")
            return []  

        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM tipos_ejercicio")
            tipos = cursor.fetchall()
            print(f"Tipos obtenidos: {tipos}")  # Mensaje de depuración
        except mysql.connector.Error as err:
            print(f"Error al obtener tipos: {err}")
            tipos = []
        finally:
            cursor.close()
            db.close()
        
        return tipos

    def registrar(self, usuario_id, tipo_ejercicio_id, duracion):
        db = self.conectar()  
        if db is None:
            return  

        cursor = db.cursor()

        # Obtener la fecha actual
        fecha_actual = datetime.now().date()

        cursor.execute("INSERT INTO seguimiento (usuario_id, tipo_ejercicio_id, duracion, fecha) VALUES (%s, %s, %s, %s)",
                       (usuario_id, tipo_ejercicio_id, duracion, fecha_actual))
        
        db.commit()
        cursor.close()
        db.close()

    def obtener_seguimiento(self, usuario_id):
        db = self.conectar()  
        if db is None:
            return []  

        cursor = db.cursor()
        
        # Obtener el seguimiento de ejercicios del usuario
        cursor.execute("SELECT s.duracion, s.fecha, te.nombre FROM seguimiento s JOIN tipos_ejercicio te ON s.tipo_ejercicio_id = te.id WHERE s.usuario_id = %s", (usuario_id,))
        
        seguimiento = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return seguimiento

# Interfaz de usuario
def main():
    user_manager = User()  
    exercise_manager = Exercise()  

    while True:
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            user_manager.registrar(username, password)
        
        elif opcion == "2":
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            usuario = user_manager.iniciar_sesion(username, password)
            
            if usuario:
                print(f" +----------sesion de {usuario[1]} iniciada----------+")
                
                while True:
                    print("\n1. Registrar ejercicio")
                    print("2. Ver seguimiento de ejercicios")
                    print("3. Cerrar sesión")
                    sub_opcion = input("Seleccione una opción: ")

                    if sub_opcion == "1":
                        # Mostrar tipos de ejercicio disponibles
                        tipos_ejercicio = exercise_manager.obtener_tipos()
                        if not tipos_ejercicio:
                            print("No hay tipos de ejercicio disponibles.")
                        else:
                            print("\nTipos de ejercicio disponibles:")
                            for tipo in tipos_ejercicio:
                                print(f"{tipo[0]}. {tipo[1]}")  # tipo[0] es el ID y tipo[1] es el nombre
                        
                            tipo_ejercicio_id = int(input("Seleccione el ID del tipo de ejercicio: "))
                            duracion = int(input("Ingrese la duración en minutos: "))
                            exercise_manager.registrar(usuario[0], tipo_ejercicio_id, duracion)
                            print("Ejercicio registrado.")
                    
                    elif sub_opcion == "2":
                        seguimiento = exercise_manager.obtener_seguimiento(usuario[0])
                        print("\nSeguimiento de ejercicios:")
                        for duracion, fecha, nombre in seguimiento:
                            print(f"Fecha: {fecha}, Duración: {duracion} minutos, Tipo: {nombre}")
                    
                    elif sub_opcion == "3":
                        print("Cerrando sesión...")
                        break
                    
                    else:
                        print("Opción no válida.")
                
            else:
                print("Nombre de usuario o contraseña incorrectos.")
        
        elif opcion == "3":
            print("Saliendo...") 
            break
            

if __name__ == "__main__":
    main()