import matplotlib.pyplot as plt
import networkx as nx
import heapq


class PrimVisual:
    """Clase para ejecutar y visualizar paso a paso el algoritmo de Prim."""

    def __init__(self, graph, start):
        # Guardar referencias básicas
        self.graph = graph
        self.start = start

        # Lista donde acumularemos estados (snapshots) del algoritmo
        # Cada snapshot guarda el estado actual de visitados, aristas MST, cola, etc.
        self.steps = []
        # Índice del paso mostrado actualmente
        self.current_step = 0
        
    # === Implementación del algoritmo de Prim con captura de pasos ===
    def prim_with_steps(self):
        """Ejecuta Prim y guarda pasos intermedios para visualización."""
        
        # ------------------ PASO 1: Inicialización ------------------
        # Conjunto de nodos ya incluidos en el Árbol de Expansión Mínima (MST)
        visited = set()
        
        # Lista de aristas confirmadas que forman parte del MST final
        mst_edges = []
        
        # Variable para acumular el peso total del árbol
        total_weight = 0
        
        # Cola de prioridad (min-heap) con tuplas (peso, nodo_origen, nodo_destino)
        # heapq permite extraer siempre la arista con el menor peso disponible.
        pq = []
        
        # Marcar el nodo inicial como visitado (punto de partida del árbol)
        visited.add(self.start)
        
        # Agregar todas las aristas adyacentes al nodo inicial a la cola de prioridad
        for neighbor in self.graph.neighbors(self.start):
            weight = self.graph[self.start][neighbor]['weight']
            heapq.heappush(pq, (weight, self.start, neighbor))
        
        # Guardar snapshot inicial para la visualización
        self.steps.append({
            'current': self.start,     # nodo foco inicial
            'visited': visited.copy(), # nodos ya en el MST
            'mst_edges': [],           # aristas en el MST (vacío al inicio)
            'total_weight': 0,         # peso acumulado
            'queue': pq.copy(),        # contenido actual de la cola
            'message': f'Inicio: Nodo origen = {self.start}'
        })
        
        # ------------------ PASO 2: Bucle principal ------------------
        # Mientras haya aristas posibles y no hayamos conectado todos los nodos
        while pq and len(visited) < len(self.graph.nodes()):
            # Obtener la arista con el menor peso de la cola
            weight, from_node, to_node = heapq.heappop(pq)
            
            # Si el nodo destino ya está en el MST, esta arista formaría un ciclo. La ignoramos.
            if to_node in visited:
                # Guardar snapshot de arista rechazada (para efecto visual)
                self.steps.append({
                    'current': from_node,
                    'visited': visited.copy(),
                    'mst_edges': mst_edges.copy(),
                    'total_weight': total_weight,
                    'queue': pq.copy(),
                    'rejected_edge': (from_node, to_node),
                    'message': f'Arista ({from_node}, {to_node}) rechazada: {to_node} ya está en el MST'
                })
                continue
            
            # ------------------ PASO 3: Agregar arista al MST ------------------
            # Marcar el nodo destino como parte del árbol
            visited.add(to_node)
            
            # Agregar la arista y sumar su peso
            mst_edges.append((from_node, to_node, weight))
            total_weight += weight
            
            # Guardar snapshot tras confirmar la arista
            self.steps.append({
                'current': to_node,
                'visited': visited.copy(),
                'mst_edges': mst_edges.copy(),
                'total_weight': total_weight,
                'queue': pq.copy(),
                'new_edge': (from_node, to_node),
                'message': f'Agregando arista ({from_node}, {to_node}) con peso {weight} al MST'
            })
            
            # ------------------ PASO 4: Explorar nuevos vecinos ------------------
            # Explorar aristas del nodo recién agregado
            for neighbor in self.graph.neighbors(to_node):
                # Solo agregamos aristas hacia nodos que AÚN NO están en el MST
                if neighbor not in visited:
                    edge_weight = self.graph[to_node][neighbor]['weight']
                    heapq.heappush(pq, (edge_weight, to_node, neighbor))
                    
                    # Guardar snapshot de exploración (opcional, para detalle visual)
                    self.steps.append({
                        'current': to_node,
                        'visited': visited.copy(),
                        'mst_edges': mst_edges.copy(),
                        'total_weight': total_weight,
                        'queue': pq.copy(),
                        'exploring_edge': (to_node, neighbor),
                        'message': f'Explorando arista ({to_node}, {neighbor}) con peso {edge_weight}'
                    })
        
        # Guardar snapshot final con el MST completo
        self.steps.append({
            'current': None,
            'visited': visited.copy(),
            'mst_edges': mst_edges.copy(),
            'total_weight': total_weight,
            'queue': [],
            'final_mst': True,
            'message': f'MST completo con peso total: {total_weight}'
        })
        
        return mst_edges, total_weight
    
    def visualize(self):
        """Prepara la visualización y muestra la interfaz interactiva."""
        
        # Ejecutar algoritmo y capturar pasos
        self.prim_with_steps()
        
        # Crear figura con tema oscuro
        self.fig, self.ax = plt.subplots(figsize=(14, 10), facecolor='#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        
        # Registrar manejador de eventos (teclado)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        # Calcular posiciones de los nodos (layout) para mantener consistencia visual
        self.pos = nx.spring_layout(self.graph, seed=42, k=2)
        
        # Dibujar el primer paso
        self.draw_step()
        plt.tight_layout()
        plt.show()
    
    def draw_step(self):
        """Dibuja el paso actual tomando la información desde `self.steps`."""
        
        # Limpiar lienzo
        self.ax.clear()
        
        # Asegurar índice válido
        if self.current_step >= len(self.steps):
            self.current_step = len(self.steps) - 1
        
        step = self.steps[self.current_step]
        
        # Título y textos informativos
        self.ax.set_title(f"\n\n\nAlgoritmo de Prim - Árbol de Expansión Mínima\n\n",
                          fontsize=16, fontweight='bold', color="#837B7B")

        self.ax.text(0.5, 0.95, f"\n\n\nPaso {self.current_step + 1}/{len(self.steps)}\n{step['message']}\n\n",
                     transform=self.ax.transAxes, ha='center', fontsize=12, color="#837B7B", fontweight='bold')

        self.ax.text(0.1, 0.05, "[Presiona → para avanzar, 'q' para salir]", 
                     transform=self.ax.transAxes, ha='center', fontsize=10, color="#837B7B")
        
        # Determinar colores de los nodos según su estado en el snapshot
        node_colors = []
        for node in self.graph.nodes():
            if node == self.start:
                node_colors.append("#00FF80A8")  # verde (origen)
            elif node == step['current']:
                node_colors.append('#FF8C00')    # naranja (nodo actual)
            elif node in step['visited']:
                node_colors.append('#4169E1')    # azul (ya en MST)
            else:
                node_colors.append('#696969')    # gris (no visitado)
        
        # Determinar colores y grosores de las aristas
        edges = self.graph.edges()
        edge_colors = []
        edge_widths = []
        
        for edge in edges:
            # Lógica para verificar si la arista ya es parte del MST acumulado
            in_mst = False
            for mst_edge in step['mst_edges']:
                if (edge == (mst_edge[0], mst_edge[1]) or edge == (mst_edge[1], mst_edge[0])):
                    in_mst = True
                    break
            
            if in_mst:
                edge_colors.append('#00FF7F')    # verde brillante (MST confirmado)
                edge_widths.append(4)
            elif 'new_edge' in step and (edge == step['new_edge'] or 
                                       edge == (step['new_edge'][1], step['new_edge'][0])):
                edge_colors.append('#FFD700')    # dorado (recién agregada)
                edge_widths.append(5)
            elif 'exploring_edge' in step and (edge == step['exploring_edge'] or 
                                             edge == (step['exploring_edge'][1], step['exploring_edge'][0])):
                edge_colors.append('#FF4500')    # rojo-naranja (siendo explorada)
                edge_widths.append(3)
            elif 'rejected_edge' in step and (edge == step['rejected_edge'] or 
                                            edge == (step['rejected_edge'][1], step['rejected_edge'][0])):
                edge_colors.append('#FF0000')    # rojo (rechazada por ciclo)
                edge_widths.append(3)
            else:
                edge_colors.append('#555555')    # gris (inactiva)
                edge_widths.append(1)
        
        # Dibujar aristas
        nx.draw_networkx_edges(self.graph, self.pos, ax=self.ax, 
                               edge_color=edge_colors, width=edge_widths, alpha=0.6)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(self.graph, self.pos, ax=self.ax,
                               node_color=node_colors, node_size=800,
                               edgecolors='white', linewidths=2)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(self.graph, self.pos, ax=self.ax,
                                font_size=12, font_weight='bold', font_color='white')
        
        # Etiquetas de pesos
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels, ax=self.ax,
                                     font_size=10, font_color='white',
                                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#2b2b2b', 
                                     edgecolor='none', alpha=0.8))
        
        # Texto con el peso acumulado
        if 'final_mst' in step:
            weight_text = f"Peso total del MST: {step['total_weight']}"
        else:
            weight_text = f"Peso acumulado del MST: {step['total_weight']}"
        
        self.ax.text(0.02, 0.98, weight_text, transform=self.ax.transAxes,
                     fontsize=10, verticalalignment='center', color="#BEB1B1", fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='#404040', alpha=0.9, edgecolor="#8B8686"))
        
        # Limpiar ejes
        self.ax.axis('off')
        self.fig.canvas.draw()
    
    def on_key(self, event):
        """Manejador de eventos de teclado."""
        if event.key == 'right':
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
                self.draw_step()
        elif event.key == 'q':
            plt.close()


# ------------------ Ejemplo de uso ------------------

if __name__ == "__main__":
    # Crear grafo de ejemplo
    G = nx.Graph()
    
    # Lista de aristas (u, v, peso)
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3)
    ]
    
    # Agregar aristas con atributos de peso
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    # Mensajes de consola
    print("Iniciando visualización del algoritmo de Prim...")
    print("Controles:")
    print("  → (flecha derecha): Avanzar al siguiente paso")
    print("  q: Cerrar visualización")
    
    # Instanciar y ejecutar
    prim_viz = PrimVisual(G, start='A')
    prim_viz.visualize()