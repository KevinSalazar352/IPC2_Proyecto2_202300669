import time
from estructuras import ListaEnlazada, Cola


class Transaccion:
    def __init__(self, id_transaccion, nombre, tiempo_atencion):
        self.id = id_transaccion
        self.nombre = nombre
        self.tiempo_atencion = tiempo_atencion
    
    def __str__(self):
        return f"Transacción {self.id}: {self.nombre} ({self.tiempo_atencion} min)"

class Escritorio:
    def __init__(self, id_escritorio, identificacion, encargado):
        self.id = id_escritorio
        self.identificacion = identificacion
        self.encargado = encargado
        self.activo = False
        self.tiempos_atencion = ListaEnlazada()
        self.cliente_actual = None
        self.clientes_atendidos = ListaEnlazada()
    
    def __str__(self):
        estado = "ACTIVO" if self.activo else "INACTIVO"
        cliente_actual = f" - Cliente: {self.cliente_actual.nombre}" if self.cliente_actual else ""
        return f"Escritorio {self.id} ({self.identificacion}) - Encargado: {self.encargado} [{estado}]{cliente_actual}"
    
    def agregar_tiempo_atencion(self, tiempo):
        self.tiempos_atencion.agregar(tiempo)
    
    def estadisticas(self):
        if len(self.tiempos_atencion) == 0:
            return (0, 0, 0)
        
        tiempos = [t for t in self.tiempos_atencion]
        return (
            sum(tiempos)/len(tiempos),  # Promedio
            max(tiempos),               # Máximo
            min(tiempos)               # Mínimo
        )

class PuntoAtencion:
    def __init__(self, id_punto, nombre, direccion):
        self.id = id_punto
        self.nombre = nombre
        self.direccion = direccion
        self.escritorios = ListaEnlazada()
        self.cola_clientes = Cola()
        self.tiempos_espera = ListaEnlazada()
        self.clientes_atendidos = ListaEnlazada()
    
    def __str__(self):
        return (f"Punto {self.id}: {self.nombre} ({self.direccion})\n"
               f"  Escritorios: {len(self.escritorios)}\n"
               f"  Clientes en espera: {len(self.cola_clientes)}\n"
               f"  Clientes atendidos: {len(self.clientes_atendidos)}")
    
    def estadisticas_espera(self):
        if len(self.tiempos_espera) == 0:
            return (0, 0, 0)
        
        tiempos = [t for t in self.tiempos_espera]
        return (
            sum(tiempos)/len(tiempos),  # Promedio
            max(tiempos),               # Máximo
            min(tiempos)               # Mínimo
        )
    
    def estadisticas_atencion(self):
        tiempos = ListaEnlazada()
        for escritorio in self.escritorios:
            for tiempo in escritorio.tiempos_atencion:
                tiempos.agregar(tiempo)
        
        if len(tiempos) == 0:
            return (0, 0, 0)
        
        tiempos_lista = [t for t in tiempos]
        return (
            sum(tiempos_lista)/len(tiempos_lista),  # Promedio
            max(tiempos_lista),                     # Máximo
            min(tiempos_lista)                      # Mínimo
        )

class Empresa:
    def __init__(self, id_empresa, nombre, abreviatura):
        self.id = id_empresa
        self.nombre = nombre
        self.abreviatura = abreviatura
        self.puntos_atencion = ListaEnlazada()
        self.transacciones = ListaEnlazada()
    
    def __str__(self):
        return (f"Empresa {self.id}: {self.nombre} ({self.abreviatura})\n"
               f"  Puntos de atención: {len(self.puntos_atencion)}\n"
               f"  Transacciones disponibles: {len(self.transacciones)}")

class Cliente:
    def __init__(self, dpi, nombre):
        self.dpi = dpi
        self.nombre = nombre
        self.transacciones = ListaEnlazada()
        self.tiempo_llegada = time.time()
        self.tiempo_atencion = 0
        self.tiempo_finalizacion = None
    
    def calcular_tiempo_total(self):
        if not self.tiempo_llegada or not self.tiempo_finalizacion:
            return 0
        return round(self.tiempo_finalizacion - self.tiempo_llegada, 2)
    
    def __str__(self):
        transacciones = ", ".join([f"{t['id']} x{t['cantidad']}" for t in self.transacciones])
        tiempo_espera = f" - Espera: {self.calcular_tiempo_total()} min" if self.tiempo_finalizacion else ""
        return f"Cliente {self.dpi}: {self.nombre} [Transacciones: {transacciones}]{tiempo_espera}"

class ConfigInicial:
    def __init__(self, id_config, id_empresa, id_punto):
        self.id = id_config
        self.id_empresa = id_empresa
        self.id_punto = id_punto
        self.escritorios_activos = ListaEnlazada()
        self.clientes = ListaEnlazada()
    
    def __str__(self):
        return (f"Configuración {self.id} - Empresa: {self.id_empresa}, Punto: {self.id_punto}\n"
               f"  Escritorios activos: {len(self.escritorios_activos)}\n"
               f"  Clientes: {len(self.clientes)}")