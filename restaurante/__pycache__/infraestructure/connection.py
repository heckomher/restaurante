from abc import ABC, abstractmethod
import mysql.connector

class Connection(ABC):
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    @abstractmethod
    def execute(self, sql: str, params=None):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def fetchall(self):
        pass

    @abstractmethod
    def fetchone(self):
        pass

class MySQLConnection(Connection):
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        super().__init__(host, user, password, database)
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor(buffered=True)
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def execute(self, sql: str, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la consulta: {e}")

    def commit(self):
        try:
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al hacer commit: {e}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except mysql.connector.Error as e:
            print(f"Error al cerrar la conexión: {e}")

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener todos los registros: {e}")
            return []

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error al obtener un registro: {e}")
            return None

 