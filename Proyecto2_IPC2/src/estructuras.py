class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1
    
    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
    
    def __len__(self):
        return self.tamano
    
    def __str__(self):
        if self.esta_vacia():
            return "Lista vacía"
        
        actual = self.cabeza
        resultado = str(actual.dato)
        actual = actual.siguiente
        
        while actual is not None:
            resultado += " -> " + str(actual.dato)
            actual = actual.siguiente
            
        return resultado

class Pila:
    def __init__(self):
        self.items = ListaEnlazada()
    
    def apilar(self, item):
        nuevo_nodo = Nodo(item)
        nuevo_nodo.siguiente = self.items.cabeza
        self.items.cabeza = nuevo_nodo
        self.items.tamano += 1
    
    def desapilar(self):
        if self.items.esta_vacia():
            raise IndexError("La pila está vacía")
        dato = self.items.cabeza.dato
        self.items.cabeza = self.items.cabeza.siguiente
        self.items.tamano -= 1
        return dato
    
    def esta_vacia(self):
        return self.items.esta_vacia()
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        if self.esta_vacia():
            return "Pila vacía"
        
        resultado = ""
        actual = self.items.cabeza
        primera_iteracion = True
        
        while actual is not None:
            if not primera_iteracion:
                resultado = str(actual.dato) + "\n" + resultado
            else:
                resultado = str(actual.dato)
                primera_iteracion = False
            actual = actual.siguiente
            
        return resultado

class Cola:
    def __init__(self):
        self.entrada = Pila()
        self.salida = Pila()
    
    def encolar(self, item):
        self.entrada.apilar(item)
    
    def desencolar(self):
        if self.salida.esta_vacia():
            while not self.entrada.esta_vacia():
                self.salida.apilar(self.entrada.desapilar())
        if self.salida.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.salida.desapilar()
    
    def esta_vacia(self):
        return self.entrada.esta_vacia() and self.salida.esta_vacia()
    
    def __len__(self):
        return len(self.entrada) + len(self.salida)
    
    def __str__(self):
        if self.esta_vacia():
            return "Cola vacía"
        
        # Procesar salida (primera parte)
        temp_salida = Pila()
        resultado_salida = ""
        tiene_salida = False
        
        while not self.salida.esta_vacia():
            item = self.salida.desapilar()
            if resultado_salida:
                resultado_salida = str(item) + "\n" + resultado_salida
            else:
                resultado_salida = str(item)
            temp_salida.apilar(item)
            tiene_salida = True
        
        # Restaurar salida
        while not temp_salida.esta_vacia():
            self.salida.apilar(temp_salida.desapilar())
        
        # Procesar entrada (segunda parte)
        temp_entrada = Pila()
        resultado_entrada = ""
        tiene_entrada = False
        
        while not self.entrada.esta_vacia():
            item = self.entrada.desapilar()
            if resultado_entrada:
                resultado_entrada += "\n" + str(item)
            else:
                resultado_entrada = str(item)
            temp_entrada.apilar(item)
            tiene_entrada = True
        
        # Restaurar entrada
        while not temp_entrada.esta_vacia():
            self.entrada.apilar(temp_entrada.desapilar())
        
        # Combinar resultados
        if tiene_salida and tiene_entrada:
            return resultado_salida + "\n" + resultado_entrada
        elif tiene_salida:
            return resultado_salida
        else:
            return resultado_entrada