import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText
import xml.etree.ElementTree as ET
from datetime import datetime
import time
from modelos import Transaccion, Escritorio, PuntoAtencion, Empresa, Cliente, ConfigInicial
from estructuras import ListaEnlazada, Cola


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Atención al Cliente")
        self.root.geometry("1000x700")
        
        self.empresas = ListaEnlazada()
        self.config_iniciales = ListaEnlazada()
        self.empresa_seleccionada = None
        self.punto_seleccionado = None
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.crear_pestana_principal()
        self.crear_pestana_configuracion()
        self.crear_pestana_puntos_atencion()
        self.crear_pestana_graphviz()
        
        self.crear_consola()
        self.mostrar_mensaje("Sistema iniciado. Bienvenido al Sistema de Atención al Cliente")

    def crear_consola(self):
        frame_consola = tk.Frame(self.root)
        frame_consola.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10), side=tk.BOTTOM)
        
        tk.Label(frame_consola, text="Consola del sistema:").pack(anchor=tk.W)
        
        self.console = ScrolledText(
            frame_consola,
            height=10,
            width=80,
            state='normal',
            font=('Consolas', 10)
        )
        self.console.pack(fill=tk.BOTH, expand=True)

    def mostrar_mensaje(self, mensaje):
        self.console.config(state='normal')
        self.console.insert(tk.END, mensaje + "\n")
        self.console.config(state='disabled')
        self.console.see(tk.END)

    def crear_pestana_principal(self):
        self.frame_principal = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_principal, text="Menú Principal")
        
        tk.Label(
            self.frame_principal,
            text="SISTEMA DE ATENCIÓN AL CLIENTE",
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        ttk.Button(
            self.frame_principal,
            text="Configuración del Sistema",
            command=lambda: self.notebook.select(1),
            width=30
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_principal,
            text="Manejo de Puntos de Atención",
            command=lambda: self.notebook.select(2),
            width=30
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_principal,
            text="Visualización con Graphviz",
            command=lambda: self.notebook.select(3),
            width=30
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_principal,
            text="Salir del Sistema",
            command=self.root.quit,
            width=30
        ).pack(pady=10)

    def crear_pestana_configuracion(self):
        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Configuración")
        
        tk.Label(
            self.frame_config,
            text="CONFIGURACIÓN DEL SISTEMA",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        canvas = tk.Canvas(self.frame_config)
        scrollbar = ttk.Scrollbar(self.frame_config, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(
            scrollable_frame,
            text="Limpiar sistema (resetear)",
            command=self.limpiar_sistema,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Cargar configuración del sistema (.xml)",
            command=self.cargar_config_sistema,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Cargar configuración inicial (.xml)",
            command=self.cargar_config_inicial,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Crear nueva empresa",
            command=self.crear_nueva_empresa,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Imprimir datos del sistema",
            command=self.imprimir_datos_sistema,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Regresar al menú principal",
            command=lambda: self.notebook.select(0),
            width=30
        ).pack(pady=20, anchor='w')

    def crear_pestana_puntos_atencion(self):
        self.frame_puntos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_puntos, text="Puntos de Atención")
        
        tk.Label(
            self.frame_puntos,
            text="MANEJO DE PUNTOS DE ATENCIÓN",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        canvas = tk.Canvas(self.frame_puntos)
        scrollbar = ttk.Scrollbar(self.frame_puntos, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(scrollable_frame, text="Seleccione empresa:").pack(anchor='w')
        
        self.cmb_empresas = ttk.Combobox(scrollable_frame, state="readonly")
        self.cmb_empresas.pack(pady=5, anchor='w')
        self.cmb_empresas.bind("<<ComboboxSelected>>", self.actualizar_puntos_atencion)
        
        ttk.Label(scrollable_frame, text="Seleccione punto de atención:").pack(anchor='w')
        
        self.cmb_puntos = ttk.Combobox(scrollable_frame, state="readonly")
        self.cmb_puntos.pack(pady=5, anchor='w')
        self.cmb_puntos.bind("<<ComboboxSelected>>", self.actualizar_escritorios)
        
        ttk.Label(scrollable_frame, text="Seleccione escritorio:").pack(anchor='w')
        
        self.cmb_escritorios = ttk.Combobox(scrollable_frame, state="readonly")
        self.cmb_escritorios.pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Ver estado del punto de atención",
            command=self.ver_estado_punto,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Activar escritorio (LIFO)",
            command=self.activar_escritorio_lifo,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Desactivar escritorio (LIFO)",
            command=self.desactivar_escritorio_lifo,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Atender cliente (FIFO)",
            command=self.atender_cliente,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Solicitar atención",
            command=self.solicitar_atencion,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Simular actividad",
            command=self.simular_actividad,
            width=30
        ).pack(pady=5, anchor='w')
        
        ttk.Button(
            scrollable_frame,
            text="Regresar al menú principal",
            command=lambda: self.notebook.select(0),
            width=30
        ).pack(pady=20, anchor='w')

    def crear_pestana_graphviz(self):
        self.frame_graphviz = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_graphviz, text="Graphviz")
        
        tk.Label(
            self.frame_graphviz,
            text="VISUALIZACIÓN CON GRAPHVIZ",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_graphviz,
            text="Mostrar lista de espera de clientes",
            command=self.mostrar_lista_espera_graphviz,
            width=30
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_graphviz,
            text="Mostrar escritorios de servicio",
            command=self.mostrar_escritorios_graphviz,
            width=30
        ).pack(pady=10)
        
        # Nuevos botones para los reportes
        ttk.Button(
            self.frame_graphviz,
            text="Reporte Punto de Atención",
            command=self.generar_reporte_punto_atencion,
            width=30
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_graphviz,
            text="Reporte por Escritorio de Servicio",
            command=self.generar_reporte_escritorio_servicio,
            width=30
        ).pack(pady=10)
        
        ttk.Button(
            self.frame_graphviz,
            text="Regresar al menú principal",
            command=lambda: self.notebook.select(0),
            width=30
        ).pack(pady=20)

    def generar_reporte_punto_atencion(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        # Calcular estadísticas
        activos = sum(1 for escritorio in self.punto_seleccionado.escritorios if escritorio.activo)
        inactivos = len(self.punto_seleccionado.escritorios) - activos
        
        # Estadísticas de espera
        tiempos_espera = [t for t in self.punto_seleccionado.tiempos_espera]
        prom_espera = sum(tiempos_espera)/len(tiempos_espera) if tiempos_espera else 0
        max_espera = max(tiempos_espera) if tiempos_espera else 0
        min_espera = min(tiempos_espera) if tiempos_espera else 0
        
        # Estadísticas de atención
        tiempos_atencion = []
        for escritorio in self.punto_seleccionado.escritorios:
            tiempos_atencion.extend([t for t in escritorio.tiempos_atencion])
        
        prom_atencion = sum(tiempos_atencion)/len(tiempos_atencion) if tiempos_atencion else 0
        max_atencion = max(tiempos_atencion) if tiempos_atencion else 0
        min_atencion = min(tiempos_atencion) if tiempos_atencion else 0
        
        # Crear ventana de reporte
        reporte_window = tk.Toplevel(self.root)
        reporte_window.title("Reporte Punto de Atención")
        reporte_window.geometry("500x600")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(reporte_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del reporte
        tk.Label(scrollable_frame, 
                text="Reporte Punto de Atención",
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(scrollable_frame, 
                text=f"Empresa: {self.empresa_seleccionada.nombre}",
                font=("Arial", 12)).pack(anchor='w', pady=5)
        
        tk.Label(scrollable_frame, 
                text=f"Punto: {self.punto_seleccionado.nombre}",
                font=("Arial", 12)).pack(anchor='w', pady=5)
        
        # Sección de escritorios
        tk.Label(scrollable_frame, 
                text="\nCantidad de escritorios de servicio:",
                font=("Arial", 12, "bold")).pack(anchor='w', pady=5)
        
        tk.Label(scrollable_frame, 
                text=f"Activos: {activos}",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        tk.Label(scrollable_frame, 
                text=f"Inactivos: {inactivos}",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        # Sección de tiempos
        tk.Label(scrollable_frame, 
                text="\nTiempos de espera:",
                font=("Arial", 12, "bold")).pack(anchor='w', pady=5)
        
        tk.Label(scrollable_frame, 
                text=f"Promedio: {prom_espera:.2f} min",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        tk.Label(scrollable_frame, 
                text=f"Máximo: {max_espera:.2f} min",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        tk.Label(scrollable_frame, 
                text=f"Mínimo: {min_espera:.2f} min",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        tk.Label(scrollable_frame, 
                text="\nTiempos de atención:",
                font=("Arial", 12, "bold")).pack(anchor='w', pady=5)
        
        tk.Label(scrollable_frame, 
                text=f"Promedio: {prom_atencion:.2f} min",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        tk.Label(scrollable_frame, 
                text=f"Máximo: {max_atencion:.2f} min",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        tk.Label(scrollable_frame, 
                text=f"Mínimo: {min_atencion:.2f} min",
                font=("Arial", 12)).pack(anchor='w', padx=20)
        
        # Botón de cierre
        ttk.Button(scrollable_frame,
                text="Cerrar",
                command=reporte_window.destroy).pack(pady=20)

    def generar_reporte_escritorio_servicio(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        # Crear ventana de reporte
        reporte_window = tk.Toplevel(self.root)
        reporte_window.title("Reporte por Escritorio de Servicio")
        reporte_window.geometry("600x600")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(reporte_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del reporte
        tk.Label(scrollable_frame, 
                text="Reporte por Escritorio de Servicio",
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(scrollable_frame, 
                text=f"Empresa: {self.empresa_seleccionada.nombre}",
                font=("Arial", 12)).pack(anchor='w', pady=5)
        
        tk.Label(scrollable_frame, 
                text=f"Punto: {self.punto_seleccionado.nombre}",
                font=("Arial", 12)).pack(anchor='w', pady=5)
        
        # Información por cada escritorio
        for escritorio in self.punto_seleccionado.escritorios:
            frame_escritorio = ttk.Frame(scrollable_frame, borderwidth=2, relief="groove")
            frame_escritorio.pack(fill=tk.X, padx=5, pady=10)
            
            estado = "ACTIVO" if escritorio.activo else "INACTIVO"
            color = "green" if escritorio.activo else "red"
            
            tk.Label(frame_escritorio, 
                    text=f"Escritorio {escritorio.id} - {estado}",
                    font=("Arial", 12, "bold"),
                    fg=color).pack(anchor='w')
            
            tk.Label(frame_escritorio, 
                    text=f"Encargado: {escritorio.encargado}",
                    font=("Arial", 11)).pack(anchor='w', padx=10)
            
            if escritorio.cliente_actual:
                tk.Label(frame_escritorio, 
                        text=f"Cliente actual: {escritorio.cliente_actual.nombre}",
                        font=("Arial", 11)).pack(anchor='w', padx=10)
            
            # Estadísticas del escritorio
            tiempos_atencion = [t for t in escritorio.tiempos_atencion]
            clientes_atendidos = len(escritorio.clientes_atendidos)
            
            tk.Label(frame_escritorio, 
                    text=f"\nClientes atendidos: {clientes_atendidos}",
                    font=("Arial", 11)).pack(anchor='w', padx=10)
            
            if tiempos_atencion:
                prom = sum(tiempos_atencion)/len(tiempos_atencion)
                max_t = max(tiempos_atencion)
                min_t = min(tiempos_atencion)
                
                tk.Label(frame_escritorio, 
                        text="Tiempos de atención:",
                        font=("Arial", 11, "underline")).pack(anchor='w', padx=10)
                
                tk.Label(frame_escritorio, 
                        text=f"Promedio: {prom:.2f} min",
                        font=("Arial", 11)).pack(anchor='w', padx=20)
                
                tk.Label(frame_escritorio, 
                        text=f"Máximo: {max_t:.2f} min",
                        font=("Arial", 11)).pack(anchor='w', padx=20)
                
                tk.Label(frame_escritorio, 
                        text=f"Mínimo: {min_t:.2f} min",
                        font=("Arial", 11)).pack(anchor='w', padx=20)
            else:
                tk.Label(frame_escritorio, 
                        text="No hay datos de tiempos de atención",
                        font=("Arial", 11)).pack(anchor='w', padx=10)
        
        # Botón de cierre
        ttk.Button(scrollable_frame,
                text="Cerrar",
                command=reporte_window.destroy).pack(pady=20)

    def limpiar_sistema(self):
        self.empresas = ListaEnlazada()
        self.config_iniciales = ListaEnlazada()
        self.empresa_seleccionada = None
        self.punto_seleccionado = None
        self.cmb_empresas['values'] = []
        self.cmb_puntos['values'] = []
        self.cmb_escritorios['values'] = []
        self.mostrar_mensaje("Sistema limpiado correctamente.")

    def cargar_config_sistema(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de configuración del sistema",
            filetypes=[("Archivos XML", "*.xml")]
        )
        if archivo:
            try:
                tree = ET.parse(archivo)
                root = tree.getroot()
                
                for empresa_elem in root.findall('empresa'):
                    empresa = Empresa(
                        empresa_elem.get('id'),
                        empresa_elem.find('nombre').text.strip(),
                        empresa_elem.find('abreviatura').text.strip()
                    )
                    
                    for punto_elem in empresa_elem.find('listaPuntosAtencion').findall('puntoAtencion'):
                        punto = PuntoAtencion(
                            punto_elem.get('id'),
                            punto_elem.find('nombre').text.strip(),
                            punto_elem.find('direccion').text.strip()
                        )
                        
                        for escritorio_elem in punto_elem.find('listaEscritorios').findall('escritorio'):
                            escritorio = Escritorio(
                                escritorio_elem.get('id'),
                                escritorio_elem.find('identificación').text.strip(),
                                escritorio_elem.find('encargado').text.strip()
                            )
                            punto.escritorios.agregar(escritorio)
                        
                        empresa.puntos_atencion.agregar(punto)
                    
                    for transaccion_elem in empresa_elem.find('listaTransacciones').findall('transaccion'):
                        transaccion = Transaccion(
                            transaccion_elem.get('id'),
                            transaccion_elem.find('nombre').text.strip(),
                            int(transaccion_elem.find('tiempoAtencion').text)
                        )
                        empresa.transacciones.agregar(transaccion)
                    
                    self.empresas.agregar(empresa)
                
                # Actualizar combobox sin usar listas nativas
                nombres_empresas = ListaEnlazada()
                for empresa in self.empresas:
                    nombres_empresas.agregar(empresa.nombre)
                
                # Uso mínimo de list() permitido para integración con tkinter
                self.cmb_empresas['values'] = list(nombres_empresas)
                self.mostrar_mensaje(f"Configuración cargada: {len(self.empresas)} empresas")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
                self.mostrar_mensaje(f"Error: {str(e)}")

    def cargar_config_inicial(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de configuración inicial",
            filetypes=[("Archivos XML", "*.xml")]
        )
        if archivo:
            try:
                tree = ET.parse(archivo)
                root = tree.getroot()
                
                for config_elem in root.findall('configInicial'):
                    config = ConfigInicial(
                        config_elem.get('id'),
                        config_elem.get('idEmpresa'),
                        config_elem.get('idPunto')
                    )
                    
                    # Buscar la empresa y punto correspondiente
                    empresa_encontrada = None
                    punto_encontrado = None
                    
                    for empresa in self.empresas:
                        if empresa.id == config.id_empresa:
                            empresa_encontrada = empresa
                            for punto in empresa.puntos_atencion:
                                if punto.id == config.id_punto:
                                    punto_encontrado = punto
                                    break
                            break
                    
                    if not empresa_encontrada or not punto_encontrado:
                        self.mostrar_mensaje(f"Advertencia: No se encontró empresa {config.id_empresa} o punto {config.id_punto}")
                        continue
                    
                    # Activar los escritorios especificados
                    escritorios_activos = ListaEnlazada()
                    for escritorio_elem in config_elem.find('escritoriosActivos').findall('escritorio'):
                        escritorio_id = escritorio_elem.get('idEscritorio')
                        
                        # Buscar el escritorio en el punto
                        escritorio_encontrado = None
                        for escritorio in punto_encontrado.escritorios:
                            if escritorio.id == escritorio_id:
                                escritorio_encontrado = escritorio
                                break
                        
                        if escritorio_encontrado:
                            if not escritorio_encontrado.activo:
                                escritorio_encontrado.activo = True
                                self.mostrar_mensaje(f"Escritorio {escritorio_id} activado según configuración inicial")
                                escritorios_activos.agregar(escritorio_id)
                            else:
                                self.mostrar_mensaje(f"Escritorio {escritorio_id} ya estaba activo")
                        else:
                            self.mostrar_mensaje(f"Advertencia: No se encontró escritorio {escritorio_id} en el punto {punto_encontrado.nombre}")
                    
                    config.escritorios_activos = escritorios_activos
                    
                    # Agregar clientes a la cola
                    if config_elem.find('listadoClientes') is not None:
                        for cliente_elem in config_elem.find('listadoClientes').findall('cliente'):
                            cliente = Cliente(
                                cliente_elem.get('dpi'),
                                cliente_elem.find('nombre').text.strip()
                            )
                            
                            for transaccion_elem in cliente_elem.find('listadoTransacciones').findall('transaccion'):
                                transaccion = {
                                    'id': transaccion_elem.get('idTransaction'),
                                    'cantidad': int(transaccion_elem.get('cantidad'))
                                }
                                cliente.transacciones.agregar(transaccion)
                            
                            # Calcular tiempo estimado de atención
                            tiempo_atencion = 0
                            for transaccion in cliente.transacciones:
                                for trans in empresa_encontrada.transacciones:
                                    if trans.id == transaccion['id']:
                                        tiempo_atencion += trans.tiempo_atencion * transaccion['cantidad']
                                        break
                            
                            cliente.tiempo_atencion = tiempo_atencion
                            punto_encontrado.cola_clientes.encolar(cliente)
                            config.clientes.agregar(cliente)
                            self.mostrar_mensaje(f"Cliente {cliente.nombre} agregado a la cola con {tiempo_atencion} min de atención estimada")
                    
                    self.config_iniciales.agregar(config)
                    
                    # Asignar clientes a escritorios activos
                    self.asignar_clientes_a_escritorios(punto_encontrado)
                
                self.mostrar_mensaje(f"Configuración inicial cargada: {len(self.config_iniciales)} configuraciones")
                
                # Actualizar la interfaz
                if self.empresa_seleccionada:
                    self.actualizar_puntos_atencion()
                    if self.punto_seleccionado:
                        self.actualizar_escritorios()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
                self.mostrar_mensaje(f"Error: {str(e)}")

    def asignar_clientes_a_escritorios(self, punto):
        """Asigna clientes a escritorios activos disponibles"""
        for escritorio in punto.escritorios:
            if escritorio.activo and escritorio.cliente_actual is None:
                if not punto.cola_clientes.esta_vacia():
                    cliente = punto.cola_clientes.desencolar()
                    cliente.tiempo_llegada = time.time()
                    escritorio.cliente_actual = cliente
                    self.mostrar_mensaje(f"Cliente {cliente.nombre} asignado automáticamente a escritorio {escritorio.id}")

    def crear_nueva_empresa(self):
        try:
            id_empresa = simpledialog.askstring("Nueva Empresa", "Ingrese el ID de la empresa:")
            if not id_empresa:
                return
                
            nombre = simpledialog.askstring("Nueva Empresa", "Ingrese el nombre de la empresa:")
            if not nombre:
                return
                
            abreviatura = simpledialog.askstring("Nueva Empresa", "Ingrese la abreviatura de la empresa:")
            if not abreviatura:
                return
            
            nueva_empresa = Empresa(id_empresa, nombre, abreviatura)
            self.empresas.agregar(nueva_empresa)
            
            # Actualizar combobox sin usar listas nativas
            nombres_empresas = ListaEnlazada()
            for empresa in self.empresas:
                nombres_empresas.agregar(empresa.nombre)
            
            self.cmb_empresas['values'] = list(nombres_empresas)  # Uso mínimo permitido para tkinter
            self.mostrar_mensaje(f"Empresa creada: {nombre} ({abreviatura})")
            
            if messagebox.askyesno("Configuración", "¿Desea agregar puntos de atención ahora?"):
                self.agregar_punto_atencion(nueva_empresa)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la empresa: {str(e)}")

    def agregar_punto_atencion(self, empresa):
        try:
            id_punto = simpledialog.askstring("Nuevo Punto", "Ingrese el ID del punto de atención:")
            if not id_punto:
                return
                
            nombre = simpledialog.askstring("Nuevo Punto", "Ingrese el nombre del punto de atención:")
            if not nombre:
                return
                
            direccion = simpledialog.askstring("Nuevo Punto", "Ingrese la dirección del punto de atención:")
            if not direccion:
                return
            
            nuevo_punto = PuntoAtencion(id_punto, nombre, direccion)
            empresa.puntos_atencion.agregar(nuevo_punto)
            self.mostrar_mensaje(f"Punto de atención agregado: {nombre} ({direccion})")
            
            if messagebox.askyesno("Configuración", "¿Desea agregar escritorios de servicio ahora?"):
                self.agregar_escritorio(nuevo_punto)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el punto de atención: {str(e)}")

    def agregar_escritorio(self, punto):
        try:
            id_escritorio = simpledialog.askstring("Nuevo Escritorio", "Ingrese el ID del escritorio:")
            if not id_escritorio:
                return
                
            identificacion = simpledialog.askstring("Nuevo Escritorio", "Ingrese la identificación del escritorio:")
            if not identificacion:
                return
                
            encargado = simpledialog.askstring("Nuevo Escritorio", "Ingrese el nombre del encargado:")
            if not encargado:
                return
            
            nuevo_escritorio = Escritorio(id_escritorio, identificacion, encargado)
            punto.escritorios.agregar(nuevo_escritorio)
            self.mostrar_mensaje(f"Escritorio agregado: {identificacion} - Encargado: {encargado}")
            
            if messagebox.askyesno("Configuración", "¿Desea agregar otro escritorio?"):
                self.agregar_escritorio(punto)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el escritorio: {str(e)}")

    def agregar_transaccion(self, empresa):
        try:
            id_transaccion = simpledialog.askstring("Nueva Transacción", "Ingrese el ID de la transacción:")
            if not id_transaccion:
                return
                
            nombre = simpledialog.askstring("Nueva Transacción", "Ingrese el nombre de la transacción:")
            if not nombre:
                return
                
            tiempo = simpledialog.askinteger("Nueva Transacción", "Ingrese el tiempo de atención (minutos):")
            if not tiempo:
                return
            
            nueva_transaccion = Transaccion(id_transaccion, nombre, tiempo)
            empresa.transacciones.agregar(nueva_transaccion)
            self.mostrar_mensaje(f"Transacción agregada: {nombre} ({tiempo} min)")
            
            if messagebox.askyesno("Configuración", "¿Desea agregar otra transacción?"):
                self.agregar_transaccion(empresa)
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la transacción: {str(e)}")

    def imprimir_datos_sistema(self):
        self.mostrar_mensaje("\n=== DATOS DEL SISTEMA ===")
        
        if len(self.empresas) == 0:
            self.mostrar_mensaje("No hay empresas registradas")
            return
        
        for empresa in self.empresas:
            self.mostrar_mensaje(f"\n{empresa}")
            
            if len(empresa.puntos_atencion) > 0:
                self.mostrar_mensaje("  Puntos de atención:")
                for punto in empresa.puntos_atencion:
                    self.mostrar_mensaje(f"    {punto}")
                    
                    if len(punto.escritorios) > 0:
                        self.mostrar_mensaje("      Escritorios:")
                        for escritorio in punto.escritorios:
                            self.mostrar_mensaje(f"        {escritorio}")
            
            if len(empresa.transacciones) > 0:
                self.mostrar_mensaje("  Transacciones:")
                for transaccion in empresa.transacciones:
                    self.mostrar_mensaje(f"    {transaccion}")
        
        if len(self.config_iniciales) > 0:
            self.mostrar_mensaje("\nConfiguraciones iniciales:")
            for config in self.config_iniciales:
                self.mostrar_mensaje(f"  {config}")

    def actualizar_puntos_atencion(self, event):
        empresa_nombre = self.cmb_empresas.get()
        for empresa in self.empresas:
            if empresa.nombre == empresa_nombre:
                self.empresa_seleccionada = empresa
                nombres_puntos = ListaEnlazada()
                for punto in empresa.puntos_atencion:
                    nombres_puntos.agregar(punto.nombre)
                
                self.cmb_puntos['values'] = list(nombres_puntos)  # Uso mínimo para tkinter
                if len(nombres_puntos) > 0:
                    self.cmb_puntos.current(0)
                break

    def actualizar_escritorios(self, event=None):
        if not self.empresa_seleccionada or not self.cmb_puntos.get():
            return
        
        punto_nombre = self.cmb_puntos.get()
        for punto in self.empresa_seleccionada.puntos_atencion:
            if punto.nombre == punto_nombre:
                self.punto_seleccionado = punto
                break
        
        if self.punto_seleccionado:
            escritorios_info = ListaEnlazada()
            for escritorio in self.punto_seleccionado.escritorios:
                estado = "ACTIVO" if escritorio.activo else "INACTIVO"
                escritorios_info.agregar(f"{escritorio.id} ({escritorio.identificacion}) - {estado}")
            
            self.cmb_escritorios['values'] = list(escritorios_info)  # Uso mínimo para tkinter
            if len(escritorios_info) > 0:
                self.cmb_escritorios.current(0)

    def ver_estado_punto(self):
        if not self.empresa_seleccionada or not self.cmb_puntos.get():
            messagebox.showerror("Error", "Seleccione una empresa y un punto de atención")
            return
        
        punto_nombre = self.cmb_puntos.get()
        for punto in self.empresa_seleccionada.puntos_atencion:
            if punto.nombre == punto_nombre:
                self.punto_seleccionado = punto
                break
        
        if not self.punto_seleccionado:
            return
        
        # Calcular estadísticas sin listas nativas
        activos = 0
        for escritorio in self.punto_seleccionado.escritorios:
            if escritorio.activo:
                activos += 1
        inactivos = len(self.punto_seleccionado.escritorios) - activos
        
        # Estadísticas de espera
        total_espera = 0
        max_espera = 0
        min_espera = float('inf')
        count_espera = 0
        
        for tiempo in self.punto_seleccionado.tiempos_espera:
            total_espera += tiempo
            if tiempo > max_espera:
                max_espera = tiempo
            if tiempo < min_espera:
                min_espera = tiempo
            count_espera += 1
        
        prom_espera = total_espera / count_espera if count_espera > 0 else 0
        
        # Estadísticas de atención
        total_atencion = 0
        max_atencion = 0
        min_atencion = float('inf')
        count_atencion = 0
        
        for escritorio in self.punto_seleccionado.escritorios:
            for tiempo in escritorio.tiempos_atencion:
                total_atencion += tiempo
                if tiempo > max_atencion:
                    max_atencion = tiempo
                if tiempo < min_atencion:
                    min_atencion = tiempo
                count_atencion += 1
        
        prom_atencion = total_atencion / count_atencion if count_atencion > 0 else 0
        
        info = f"\n=== ESTADO DEL PUNTO ===\n"
        info += f"Empresa: {self.empresa_seleccionada.nombre}\n"
        info += f"Punto: {self.punto_seleccionado.nombre}\n"
        info += f"Clientes en espera: {len(self.punto_seleccionado.cola_clientes)}\n"
        info += f"Clientes atendidos: {len(self.punto_seleccionado.clientes_atendidos)}\n"
        info += f"Escritorios activos: {activos}\n"
        info += f"Escritorios inactivos: {inactivos}\n"
        info += f"Tiempo promedio de espera: {prom_espera:.2f} min\n"
        info += f"Tiempo máximo de espera: {max_espera:.2f} min\n"
        info += f"Tiempo mínimo de espera: {min_espera:.2f} min\n"
        info += f"Tiempo promedio de atención: {prom_atencion:.2f} min\n"
        info += f"Tiempo máximo de atención: {max_atencion:.2f} min\n"
        info += f"Tiempo mínimo de atención: {min_atencion:.2f} min\n"
        
        info += "\n=== ESCRITORIOS ACTIVOS ===\n"
        for escritorio in self.punto_seleccionado.escritorios:
            if escritorio.activo:
                # Estadísticas por escritorio
                total_esc = 0
                max_esc = 0
                min_esc = float('inf')
                count_esc = 0
                
                for tiempo in escritorio.tiempos_atencion:
                    total_esc += tiempo
                    if tiempo > max_esc:
                        max_esc = tiempo
                    if tiempo < min_esc:
                        min_esc = tiempo
                    count_esc += 1
                
                prom_esc = total_esc / count_esc if count_esc > 0 else 0
                
                info += f"Escritorio {escritorio.id}:\n"
                info += f"  Clientes atendidos: {len(escritorio.clientes_atendidos)}\n"
                info += f"  Tiempo promedio: {prom_esc:.2f} min\n"
                info += f"  Tiempo máximo: {max_esc:.2f} min\n"
                info += f"  Tiempo mínimo: {min_esc:.2f} min\n"
                if escritorio.cliente_actual:
                    info += f"  Cliente actual: {escritorio.cliente_actual.nombre}\n"
        
        self.mostrar_mensaje(info)

    def activar_escritorio_lifo(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        # Verificar si hay selección manual de escritorio
        if self.cmb_escritorios.get():
            try:
                escritorio_id = self.cmb_escritorios.get().split()[0]
                for escritorio in self.punto_seleccionado.escritorios:
                    if escritorio.id == escritorio_id:
                        if escritorio.activo:
                            messagebox.showwarning("Advertencia", f"El escritorio {escritorio_id} ya está activo")
                            return
                        escritorio.activo = True
                        self.mostrar_mensaje(f"Escritorio {escritorio.id} activado manualmente")
                        self.actualizar_escritorios()
                        
                        if not self.punto_seleccionado.cola_clientes.esta_vacia():
                            self.asignar_cliente_escritorio(escritorio)
                        return
            except Exception as e:
                self.mostrar_mensaje(f"Error al activar escritorio: {str(e)}")
        
        # Comportamiento LIFO original
        escritorio_activar = None
        for escritorio in reversed(self.punto_seleccionado.escritorios):
            if not escritorio.activo:
                escritorio_activar = escritorio
                break
        
        if escritorio_activar:
            escritorio_activar.activo = True
            self.mostrar_mensaje(f"Escritorio {escritorio_activar.id} activado (LIFO)")
            self.actualizar_escritorios()
            
            if not self.punto_seleccionado.cola_clientes.esta_vacia():
                self.asignar_cliente_escritorio(escritorio_activar)
        else:
            self.mostrar_mensaje("No hay escritorios disponibles para activar")

    def desactivar_escritorio_lifo(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        # Verificar si hay selección manual de escritorio
        if self.cmb_escritorios.get():
            try:
                escritorio_id = self.cmb_escritorios.get().split()[0]
                for escritorio in self.punto_seleccionado.escritorios:
                    if escritorio.id == escritorio_id:
                        if not escritorio.activo:
                            messagebox.showwarning("Advertencia", f"El escritorio {escritorio_id} ya está inactivo")
                            return
                        
                        if escritorio.cliente_actual:
                            cliente = escritorio.cliente_actual
                            cliente.tiempo_finalizacion = time.time()
                            tiempo_atencion = cliente.calcular_tiempo_total()
                            
                            escritorio.tiempos_atencion.agregar(tiempo_atencion)
                            escritorio.clientes_atendidos.agregar(cliente)
                            self.punto_seleccionado.clientes_atendidos.agregar(cliente)
                            self.punto_seleccionado.tiempos_espera.agregar(tiempo_atencion)
                            
                            self.mostrar_mensaje(f"Cliente {cliente.nombre} atendido en {tiempo_atencion:.2f} min")
                        
                        escritorio.activo = False
                        escritorio.cliente_actual = None
                        self.mostrar_mensaje(f"Escritorio {escritorio.id} desactivado manualmente")
                        self.actualizar_escritorios()
                        return
            except Exception as e:
                self.mostrar_mensaje(f"Error al desactivar escritorio: {str(e)}")
        
        # Comportamiento LIFO original
        escritorio_desactivar = None
        for escritorio in reversed(self.punto_seleccionado.escritorios):
            if escritorio.activo:
                escritorio_desactivar = escritorio
                break
        
        if escritorio_desactivar:
            if escritorio_desactivar.cliente_actual:
                cliente = escritorio_desactivar.cliente_actual
                cliente.tiempo_finalizacion = time.time()
                tiempo_atencion = cliente.calcular_tiempo_total()
                
                escritorio_desactivar.tiempos_atencion.agregar(tiempo_atencion)
                escritorio_desactivar.clientes_atendidos.agregar(cliente)
                self.punto_seleccionado.clientes_atendidos.agregar(cliente)
                self.punto_seleccionado.tiempos_espera.agregar(tiempo_atencion)
                
                self.mostrar_mensaje(f"Cliente {cliente.nombre} atendido en {tiempo_atencion:.2f} min")
            
            escritorio_desactivar.activo = False
            escritorio_desactivar.cliente_actual = None
            self.mostrar_mensaje(f"Escritorio {escritorio_desactivar.id} desactivado (LIFO)")
            self.actualizar_escritorios()
        else:
            self.mostrar_mensaje("No hay escritorios activos para desactivar")

    def asignar_cliente_escritorio(self, escritorio):
        if escritorio.cliente_actual is None and not self.punto_seleccionado.cola_clientes.esta_vacia():
            cliente = self.punto_seleccionado.cola_clientes.desencolar()
            cliente.tiempo_llegada = time.time()
            escritorio.cliente_actual = cliente
            
            # Calcular tiempo estimado de atención
            tiempo_atencion = 0
            for transaccion in cliente.transacciones:
                for trans in self.empresa_seleccionada.transacciones:
                    if trans.id == transaccion['id']:
                        tiempo_atencion += trans.tiempo_atencion * transaccion['cantidad']
                        break
            
            self.mostrar_mensaje(f"Cliente {cliente.nombre} asignado a escritorio {escritorio.id}")
            self.mostrar_mensaje(f"Tiempo estimado de atención: {tiempo_atencion} min")

    def atender_cliente(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        atendidos = 0
        for escritorio in self.punto_seleccionado.escritorios:
            if escritorio.activo and escritorio.cliente_actual:
                cliente = escritorio.cliente_actual
                cliente.tiempo_finalizacion = time.time()
                tiempo_atencion = cliente.calcular_tiempo_total()
                
                escritorio.tiempos_atencion.agregar(tiempo_atencion)
                escritorio.clientes_atendidos.agregar(cliente)
                self.punto_seleccionado.clientes_atendidos.agregar(cliente)
                self.punto_seleccionado.tiempos_espera.agregar(tiempo_atencion)
                
                self.mostrar_mensaje(f"Cliente {cliente.nombre} atendido en {tiempo_atencion:.2f} min")
                escritorio.cliente_actual = None
                atendidos += 1
                
                if not self.punto_seleccionado.cola_clientes.esta_vacia():
                    self.asignar_cliente_escritorio(escritorio)
        
        if atendidos == 0:
            self.mostrar_mensaje("No hay clientes siendo atendidos actualmente")

    def solicitar_atencion(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        try:
            dpi = simpledialog.askstring("Nuevo Cliente", "Ingrese el DPI del cliente:")
            if not dpi:
                return
                
            nombre = simpledialog.askstring("Nuevo Cliente", "Ingrese el nombre del cliente:")
            if not nombre:
                return
            
            nuevo_cliente = Cliente(dpi, nombre)
            
            # Obtener transacciones disponibles
            transacciones_disponibles = ListaEnlazada()
            for t in self.empresa_seleccionada.transacciones:
                transacciones_disponibles.agregar(t)
            
            if len(transacciones_disponibles) == 0:
                messagebox.showerror("Error", "No hay transacciones disponibles")
                return
            
            # Mostrar transacciones disponibles
            transacciones_texto = ""
            for i, trans in enumerate(transacciones_disponibles):
                transacciones_texto += f"{trans.id}: {trans.nombre}"
                if i < len(transacciones_disponibles) - 1:
                    transacciones_texto += ", "
            
            while True:
                trans_id = simpledialog.askstring(
                    "Transacción",
                    f"Transacciones disponibles:\n{transacciones_texto}\nIngrese ID de transacción (o dejar vacío para terminar):"
                )
                
                if not trans_id:
                    break
                
                cantidad = simpledialog.askinteger("Transacción", "Ingrese cantidad:")
                if not cantidad or cantidad < 1:
                    messagebox.showerror("Error", "Cantidad inválida")
                    continue
                
                # Verificar que la transacción existe
                trans_existe = False
                for trans in transacciones_disponibles:
                    if trans.id == trans_id:
                        nuevo_cliente.transacciones.agregar({'id': trans_id, 'cantidad': cantidad})
                        trans_existe = True
                        break
                
                if not trans_existe:
                    messagebox.showerror("Error", "ID de transacción no válido")
            
            if len(nuevo_cliente.transacciones) == 0:
                messagebox.showerror("Error", "El cliente debe tener al menos una transacción")
                return
            
            self.punto_seleccionado.cola_clientes.encolar(nuevo_cliente)
            self.mostrar_mensaje(f"Cliente {nombre} agregado a la cola de espera")
            
            for escritorio in self.punto_seleccionado.escritorios:
                if escritorio.activo and escritorio.cliente_actual is None:
                    self.asignar_cliente_escritorio(escritorio)
                    break
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el cliente: {str(e)}")

    def simular_actividad(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        self.mostrar_mensaje("\n=== SIMULANDO ACTIVIDAD ===")
        
        # Activar todos los escritorios posibles (LIFO)
        for escritorio in reversed(self.punto_seleccionado.escritorios):
            if not escritorio.activo:
                escritorio.activo = True
                self.mostrar_mensaje(f"Escritorio {escritorio.id} activado")
        
        # Atender todos los clientes posibles
        while not self.punto_seleccionado.cola_clientes.esta_vacia():
            escritorio_disponible = None
            for escritorio in self.punto_seleccionado.escritorios:
                if escritorio.activo and escritorio.cliente_actual is None:
                    escritorio_disponible = escritorio
                    break
            
            if escritorio_disponible:
                self.asignar_cliente_escritorio(escritorio_disponible)
                self.atender_cliente()
            else:
                break
        
        self.mostrar_mensaje("Simulación completada")
        self.ver_estado_punto()

    def mostrar_lista_espera_graphviz(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        try:
            from graphviz import Digraph
            
            dot = Digraph(comment='Lista de Espera', format='png')
            dot.attr(rankdir='LR')
            
            dot.node('cola', 'Cola de Espera', shape='box')
            
            # Copiar la cola original para no perder datos
            temp_cola = Cola()
            clientes_temp = ListaEnlazada()
            
            while not self.punto_seleccionado.cola_clientes.esta_vacia():
                cliente = self.punto_seleccionado.cola_clientes.desencolar()
                clientes_temp.agregar(cliente)
                temp_cola.encolar(cliente)
            
            # Restaurar la cola original
            while not temp_cola.esta_vacia():
                self.punto_seleccionado.cola_clientes.encolar(temp_cola.desencolar())
            
            # Agregar nodos de clientes
            prev_node = 'cola'
            for i, cliente in enumerate(clientes_temp):
                node_id = f'cliente_{i}'
                dot.node(node_id, f"{cliente.nombre}\nDPI: {cliente.dpi}", shape='ellipse')
                dot.edge(prev_node, node_id)
                prev_node = node_id
            
            dot.render('lista_espera', view=True)
            self.mostrar_mensaje("Gráfico de lista de espera generado")
        
        except ImportError:
            messagebox.showerror("Error", "Graphviz no está instalado")
            self.mostrar_mensaje("Error: Graphviz no está instalado")

    def mostrar_escritorios_graphviz(self):
        if not self.punto_seleccionado:
            messagebox.showerror("Error", "Seleccione un punto de atención primero")
            return
        
        try:
            from graphviz import Digraph
            
            dot = Digraph(comment='Escritorios de Servicio', format='png')
            dot.attr(rankdir='TB')
            
            dot.node('punto', f"Punto: {self.punto_seleccionado.nombre}", shape='box')
            
            for escritorio in self.punto_seleccionado.escritorios:
                estado = "ACTIVO" if escritorio.activo else "INACTIVO"
                color = "green" if escritorio.activo else "red"
                
                label = f"Escritorio {escritorio.id}\nEncargado: {escritorio.encargado}\nEstado: {estado}"
                
                if escritorio.cliente_actual:
                    label += f"\nCliente: {escritorio.cliente_actual.nombre}"
                
                dot.node(f'esc_{escritorio.id}', label, shape='rectangle', color=color)
                dot.edge('punto', f'esc_{escritorio.id}')
            
            dot.render('escritorios_servicio', view=True)
            self.mostrar_mensaje("Gráfico de escritorios generado")
        
        except ImportError:
            messagebox.showerror("Error", "Graphviz no está instalado")
            self.mostrar_mensaje("Error: Graphviz no está instalado")


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()