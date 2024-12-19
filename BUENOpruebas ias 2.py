import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import heapq # Para la heurística de IA
import random #para el nivel facil de la IA


class TresEnRayaGrafo:
    def __init__(self):
        self.grafo = self.crear_grafo_tres_en_raya()
        self.tablero = {nodo: None for nodo in self.grafo.nodes}  # Estado de cada nodo
        self.turnos = deque(["X", "O"])  # Cola para alternar jugadores
        self.movimientos = []  # Pila para registrar movimientos
        self.jugador_actual = self.turnos[0]
        self.aristas_ganadoras = []  # Guardará las aristas de la línea ganadora
        self.nivel_ia = None  # Nivel de dificultad de la IA (definido más tarde)
        self.modo_ia = False  # Si el modo IA está activado

    def configurar_modo_de_juego(self):
        """
        Configura el modo de juego al inicio (contra IA o contra jugador humano).
        """
        print("Elige el modo de juego:")
        print("1. Contra otro jugador humano")
        print("2. Contra la IA")
        while True:
            try:
                opcion = int(input("Selecciona 1 o 2: "))
                if opcion == 1:
                    self.modo_ia = False
                    print("Modo seleccionado: Jugador contra Jugador")
                    break
                elif opcion == 2:
                    self.modo_ia = True
                    print("Modo seleccionado: Jugador contra IA")
                    self.configurar_dificultad()
                    break
                else:
                    print("Por favor, selecciona 1 o 2.")
            except ValueError:
                print("Entrada inválida. Intenta nuevamente.")

    def configurar_dificultad(self):
        """
        Configura el nivel de dificultad de la IA al inicio del juego.
        """
        print("Elige la dificultad de la IA:")
        print("1. Fácil")
        print("2. Difícil")
        while True:
            try:
                opcion = int(input("Selecciona 1 o 2: "))
                if opcion == 1:
                    self.nivel_ia = "fácil"
                    print("Has seleccionado: Fácil")
                    break
                elif opcion == 2:
                    self.nivel_ia = "difícil"
                    print("Has seleccionado: Difícil")
                    break
                else:
                    print("Por favor, selecciona 1 o 2.")
            except ValueError:
                print("Entrada inválida. Intenta nuevamente.")

    def crear_grafo_tres_en_raya(self):
        """
        Crea un grafo que representa las conexiones entre las casillas del tablero 3x3x3.
        """
        G = nx.Graph()
        # Crear nodos para cada casilla en el tablero 3x3x3
        for nivel in range(3):
            for fila in range(3):
                for columna in range(3):
                    G.add_node((nivel, fila, columna), pos=(columna, fila, nivel))
        
        # Conexiones horizontales y verticales dentro de cada nivel
        for nivel in range(3):
            for i in range(3):
                # Horizontal en cada fila
                G.add_edges_from([((nivel, i, 0), (nivel, i, 1)),
                                  ((nivel, i, 1), (nivel, i, 2))])
                # Vertical en cada columna
                G.add_edges_from([((nivel, 0, i), (nivel, 1, i)),
                                  ((nivel, 1, i), (nivel, 2, i))])
            # Diagonales dentro de cada nivel
            G.add_edges_from([((nivel, 0, 0), (nivel, 1, 1)),
                              ((nivel, 1, 1), (nivel, 2, 2))])
            G.add_edges_from([((nivel, 0, 2), (nivel, 1, 1)),
                              ((nivel, 1, 1), (nivel, 2, 0))])
        
        # Conexiones verticales entre niveles
        for fila in range(3):
            for columna in range(3):
                G.add_edges_from([((0, fila, columna), (1, fila, columna)),
                                  ((1, fila, columna), (2, fila, columna))])
        
        # Conexiones diagonales en 3D
        # Diagonales principales que atraviesan los niveles
        G.add_edges_from([((0, 0, 0), (1, 1, 1)), ((1, 1, 1), (2, 2, 2))])
        G.add_edges_from([((0, 0, 2), (1, 1, 1)), ((1, 1, 1), (2, 2, 0))])
        G.add_edges_from([((0, 2, 0), (1, 1, 1)), ((1, 1, 1), (2, 0, 2))])
        G.add_edges_from([((0, 2, 2), (1, 1, 1)), ((1, 1, 1), (2, 0, 0))])
        
        # Nuevas diagonales completas que atraviesan el cubo
        G.add_edges_from([((0, 0, 0), (1, 0, 1)), ((1, 0, 1), (2, 0, 2))])
        G.add_edges_from([((0, 2, 0), (1, 2, 1)), ((1, 2, 1), (2, 2, 2))])
        G.add_edges_from([((0, 0, 2), (1, 0, 1)), ((1, 0, 1), (2, 0, 0))])
        G.add_edges_from([((0, 2, 2), (1, 2, 1)), ((1, 2, 1), (2, 2, 0))])
        
        # Conexiones adicionales que cubren todas las combinaciones diagonales a través del cubo
        for fila in range(3):
            G.add_edges_from([((0, fila, 0), (1, fila, 1)), ((1, fila, 1), (2, fila, 2))])
            G.add_edges_from([((0, fila, 2), (1, fila, 1)), ((1, fila, 1), (2, fila, 0))])
        for columna in range(3):
            G.add_edges_from([((0, 0, columna), (1, 1, columna)), ((1, 1, columna), (2, 2, columna))])
            G.add_edges_from([((0, 2, columna), (1, 1, columna)), ((1, 1, columna), (2, 0, columna))])
        G.add_edges_from([((0, 0, 1), (1, 1, 1)), ((1, 1, 1), (2, 2, 1))])
        G.add_edges_from([((0, 2, 1), (1, 1, 1)), ((1, 1, 1), (2, 0, 1))])
        G.add_edges_from([((0, 1, 0), (1, 1, 1)), ((1, 1, 1), (2, 1, 2))])
        G.add_edges_from([((0, 1, 2), (1, 1, 1)), ((1, 1, 1), (2, 1, 0))])
        G.add_edges_from([((0, 1, 1), (1, 1, 1)), ((1, 1, 1), (2, 1, 1))])

        return G

    def imprimir_tablero(self):
        """
        Muestra el estado actual del tablero.
        """
        for nivel in range(3):
            print(f"Nivel {nivel + 1}:")
            for fila in range(3):
                fila_estado = [self.tablero[(nivel, fila, col)] or " " for col in range(3)]
                print(" | ".join(fila_estado))
            print("-" * 10)

    def verificar_ganador(self):
        """
        Verifica si hay un ganador en el tablero.
        """
        lineas = []
        # Líneas horizontales en cada nivel
        for nivel in range(3):
            for fila in range(3):
                lineas.append([(nivel, fila, 0), (nivel, fila, 1), (nivel, fila, 2)])
        # Líneas verticales en cada nivel
        for nivel in range(3):
            for columna in range(3):
                lineas.append([(nivel, 0, columna), (nivel, 1, columna), (nivel, 2, columna)])
        # Líneas diagonales dentro de cada nivel
        for nivel in range(3):
            lineas.append([(nivel, 0, 0), (nivel, 1, 1), (nivel, 2, 2)])
            lineas.append([(nivel, 0, 2), (nivel, 1, 1), (nivel, 2, 0)])
        # Líneas verticales entre niveles
        for fila in range(3):
            for columna in range(3):
                lineas.append([(0, fila, columna), (1, fila, columna), (2, fila, columna)])
        # Líneas diagonales en 3D
        lineas.append([(0, 0, 0), (1, 1, 1), (2, 2, 2)])  # Diagonal 3D principal
        lineas.append([(0, 0, 2), (1, 1, 1), (2, 2, 0)])  # Diagonal 3D inversa
        lineas.append([(0, 2, 0), (1, 1, 1), (2, 0, 2)])  # Diagonal 3D cruzada
        lineas.append([(0, 2, 2), (1, 1, 1), (2, 0, 0)])  # Diagonal 3D cruzada inversa
        # Nuevas diagonales completas añadidas
        lineas.append([(0, 0, 0), (1, 0, 1), (2, 0, 2)])
        lineas.append([(0, 2, 0), (1, 2, 1), (2, 2, 2)])
        lineas.append([(0, 0, 2), (1, 0, 1), (2, 0, 0)])
        lineas.append([(0, 2, 2), (1, 2, 1), (2, 2, 0)])
        # Líneas adicionales para asegurar todas las diagonales
        for fila in range(3):
            lineas.append([(0, fila, 0), (1, fila, 1), (2, fila, 2)])
            lineas.append([(0, fila, 2), (1, fila, 1), (2, fila, 0)])
        for columna in range(3):
            lineas.append([(0, 0, columna), (1, 1, columna), (2, 2, columna)])
            lineas.append([(0, 2, columna), (1, 1, columna), (2, 0, columna)])
        lineas.append([(0, 0, 1), (1, 1, 1), (2, 2, 1)])
        lineas.append([(0, 2, 1), (1, 1, 1), (2, 0, 1)])
        lineas.append([(0, 1, 0), (1, 1, 1), (2, 1, 2)])
        lineas.append([(0, 1, 2), (1, 1, 1), (2, 1, 0)])
        lineas.append([(0, 1, 1), (1, 1, 1), (2, 1, 1)])

        # Verificar si alguna línea está llena por un mismo jugador
        for linea in lineas:
            valores = [self.tablero[nodo] for nodo in linea]
            if len(set(valores)) == 1 and valores[0] is not None:  # Todos los valores son iguales y no son None
                self.aristas_ganadoras = [(linea[i], linea[i + 1]) for i in range(len(linea) - 1)]
                return valores[0]  # Retornar el jugador ganador

        return None
    
    def mejor_movimiento(self):
        """
        Determina el mejor movimiento para la IA considerando:
        - Bloquear al oponente si está a punto de ganar.
        - Ganar si es posible.
        - En otros casos, usar heurística para tomar la decisión más estratégica.
        """
        lineas = []
        # Generar todas las líneas posibles en el tablero
        for nivel in range(3):
            for fila in range(3):
                lineas.append([(nivel, fila, 0), (nivel, fila, 1), (nivel, fila, 2)])
            for columna in range(3):
                lineas.append([(nivel, 0, columna), (nivel, 1, columna), (nivel, 2, columna)])
        for nivel in range(3):
            lineas.append([(nivel, 0, 0), (nivel, 1, 1), (nivel, 2, 2)])
            lineas.append([(nivel, 0, 2), (nivel, 1, 1), (nivel, 2, 0)])
        for fila in range(3):
            for columna in range(3):
                lineas.append([(0, fila, columna), (1, fila, columna), (2, fila, columna)])
        lineas.append([(0, 0, 0), (1, 1, 1), (2, 2, 2)])  # Diagonal 3D principal
        lineas.append([(0, 0, 2), (1, 1, 1), (2, 2, 0)])  # Diagonal 3D inversa
        lineas.append([(0, 2, 0), (1, 1, 1), (2, 0, 2)])  # Diagonal 3D cruzada
        lineas.append([(0, 2, 2), (1, 1, 1), (2, 0, 0)])  # Diagonal 3D cruzada inversa
        # Añadir las nuevas líneas completas
        lineas.append([(0, 0, 0), (1, 0, 1), (2, 0, 2)])
        lineas.append([(0, 2, 0), (1, 2, 1), (2, 2, 2)])
        lineas.append([(0, 0, 2), (1, 0, 1), (2, 0, 0)])
        lineas.append([(0, 2, 2), (1, 2, 1), (2, 2, 0)])
        for fila in range(3):
            lineas.append([(0, fila, 0), (1, fila, 1), (2, fila, 2)])
            lineas.append([(0, fila, 2), (1, fila, 1), (2, fila, 0)])
        for columna in range(3):
            lineas.append([(0, 0, columna), (1, 1, columna), (2, 2, columna)])
            lineas.append([(0, 2, columna), (1, 1, columna), (2, 0, columna)])
        lineas.append([(0, 0, 1), (1, 1, 1), (2, 2, 1)])
        lineas.append([(0, 2, 1), (1, 1, 1), (2, 0, 1)])
        lineas.append([(0, 1, 0), (1, 1, 1), (2, 1, 2)])
        lineas.append([(0, 1, 2), (1, 1, 1), (2, 1, 0)])
        lineas.append([(0, 1, 1), (1, 1, 1), (2, 1, 1)])

        # Primero: Ver si la IA puede ganar
        for linea in lineas:
            valores = [self.tablero[nodo] for nodo in linea]
            if valores.count("O") == 2 and valores.count(None) == 1:
                return linea[valores.index(None)]  # Movimiento ganador

        # Segundo: Bloquear al oponente si puede ganar
        for linea in lineas:
            valores = [self.tablero[nodo] for nodo in linea]
            if valores.count("X") == 2 and valores.count(None) == 1:
                return linea[valores.index(None)]  # Movimiento para bloquear

        # Tercero: Usar la heurística para determinar el mejor movimiento
        movimientos = []
        for nodo in self.tablero:
            if self.tablero[nodo] is None:
                heuristica = self.heuristica(nodo)
                heapq.heappush(movimientos, (-heuristica, nodo))
        return heapq.heappop(movimientos)[1]  # Nodo con la mejor heurística

    def ia_jugar(self):
        """
        Realiza el turno de la IA usando el mejor movimiento calculado o un movimiento más aleatorio basado en la dificultad.
        """
        if self.nivel_ia == "fácil":
            if random.random() < 0.7:  # 70% de probabilidad de hacer el mejor movimiento
                movimiento = self.mejor_movimiento()
            else:  # 30% de probabilidad de hacer un movimiento aleatorio
                movimientos_disponibles = [nodo for nodo in self.tablero if self.tablero[nodo] is None]
                movimiento = random.choice(movimientos_disponibles)
        else:
            movimiento = self.mejor_movimiento()

        # Realizar el movimiento de la IA y verificar si hay un ganador
        return self.jugar_turno(*movimiento)  # Devuelve True si la IA gana


    def heuristica(self, nodo): ######################################################### como he dearollado la euristica
        """
        Calcula un valor heurístico para un nodo dado.
        Nodo es un lugar donde la IA podría jugar.
        """
        heuristica = 0

        # Evalúa todas las líneas que incluyen este nodo
        lineas = []
        for nivel in range(3):
            for fila in range(3):
                lineas.append([(nivel, fila, 0), (nivel, fila, 1), (nivel, fila, 2)])
            for columna in range(3):
                lineas.append([(nivel, 0, columna), (nivel, 1, columna), (nivel, 2, columna)])
        for nivel in range(3):
            lineas.append([(nivel, 0, 0), (nivel, 1, 1), (nivel, 2, 2)])
            lineas.append([(nivel, 0, 2), (nivel, 1, 1), (nivel, 2, 0)])
        for fila in range(3):
            for columna in range(3):
                lineas.append([(0, fila, columna), (1, fila, columna), (2, fila, columna)])
        lineas.append([(0, 0, 0), (1, 1, 1), (2, 2, 2)])
        lineas.append([(0, 0, 2), (1, 1, 1), (2, 2, 0)])
        lineas.append([(0, 2, 0), (1, 1, 1), (2, 0, 2)])
        lineas.append([(0, 2, 2), (1, 1, 1), (2, 0, 0)])
        for fila in range(3):
            lineas.append([(0, fila, 0), (1, fila, 1), (2, fila, 2)])
            lineas.append([(0, fila, 2), (1, fila, 1), (2, fila, 0)])
        for columna in range(3):
            lineas.append([(0, 0, columna), (1, 1, columna), (2, 2, columna)])
            lineas.append([(0, 2, columna), (1, 1, columna), (2, 0, columna)])
        lineas.append([(0, 0, 1), (1, 1, 1), (2, 2, 1)])
        lineas.append([(0, 2, 1), (1, 1, 1), (2, 0, 1)])
        lineas.append([(0, 1, 0), (1, 1, 1), (2, 1, 2)])
        lineas.append([(0, 1, 2), (1, 1, 1), (2, 1, 0)])
        lineas.append([(0, 1, 1), (1, 1, 1), (2, 1, 1)])

        # Recorre las líneas relevantes
        for linea in lineas:
            if nodo in linea:
                valores = [self.tablero[n] for n in linea]
                if valores.count("O") > 0 and valores.count("X") == 0:
                    heuristica += 10 ** valores.count("O")  # Favorece a la IA
                if valores.count("X") > 0 and valores.count("O") == 0:
                    heuristica -= 10 ** valores.count("X")  # Perjudica al oponente
        return heuristica


    def jugar_turno(self, nivel, fila, columna):
        """
        Realiza el turno de un jugador.
        """
        if self.tablero[(nivel, fila, columna)]:
            print("Esa casilla ya está ocupada.")
            return False  # Movimiento inválido

        # Registrar el movimiento
        self.tablero[(nivel, fila, columna)] = self.jugador_actual
        self.movimientos.append((nivel, fila, columna))

        # Verificar si hay un ganador
        ganador = self.verificar_ganador()
        if ganador:
            self.imprimir_tablero()
            print(f"¡El jugador {ganador} gana!")
            self.dibujar_grafo()  # Mostrar el grafo final con las líneas ganadoras
            return True  # Indicar que el juego ha terminado

        # Cambiar de turno
        self.turnos.rotate(-1)
        self.jugador_actual = self.turnos[0]
        return False  # El juego continúa

    def dibujar_grafo(self):
        """
        Dibuja el grafo tridimensional representando el tablero.
        """
        pos = nx.get_node_attributes(self.grafo, 'pos')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for nodo, (x, y, z) in pos.items():
            jugador = self.tablero[nodo]
            color = 'red' if jugador == 'X' else 'blue' if jugador == 'O' else 'black'
            ax.scatter(x, y, z, color=color, s=100)
            ax.text(x, y, z, jugador or '', color='white', fontsize=12, ha='center', va='center')

        for (n1, n2) in self.grafo.edges:
            x = [pos[n1][0], pos[n2][0]]
            y = [pos[n1][1], pos[n2][1]]
            z = [pos[n1][2], pos[n2][2]]
           #pinta las aristas del jugador ganador
            if (n1, n2) in self.aristas_ganadoras or (n2, n1) in self.aristas_ganadoras:
                color = 'red' if self.jugador_actual == "X" else 'blue'
            else:
                color = 'gray'#ver las aristas o no verlas   
            ax.plot(x, y, z, color=color)

            # Configuración de ejes
            """ax.set_xlabel("Columnas (X-axis)")
            ax.set_ylabel("Filas (Y-axis)")
            ax.set_zlabel("Niveles (Z-axis)")"""

            # Etiquetas personalizadas en los ejes
            ax.set_xticks([0, 1, 2])
            ax.set_xticklabels(['Columna 1', 'Columna 2', 'Columna 3'])
            ax.set_yticks([0, 1, 2])
            ax.set_yticklabels(['Fila 1', 'Fila 2', 'Fila 3'])
            ax.set_zticks([0, 1, 2])
            ax.set_zticklabels(['Nivel 1', 'Nivel 2', 'Nivel 3'])
            
        ax.set_title("Tres en Raya 3D")
        plt.show()

    def jugar(self):
        """
        Inicia el juego.
        """
        self.configurar_modo_de_juego()  # Configura el modo de juego al iniciar (IA o humano)
        while len(self.movimientos) < 27:
            self.imprimir_tablero()
            self.dibujar_grafo()
            print(f"Turno del jugador {self.jugador_actual}.")
            if self.modo_ia and self.jugador_actual == "O":  # IA juega si está activa y es el turno de 'O'
                if self.ia_jugar():  # Si la IA gana, se termina el juego
                    return
            else:
                while True:  # Bucle para repetir en caso de entrada inválida
                    try:
                        nivel = int(input("Selecciona el nivel (1-3): "))
                        if nivel not in [1, 2, 3]:  # Verificar rango
                            print("Número de nivel no válido. Por favor, elige 1, 2 o 3.")
                            continue
                        fila = int(input("Selecciona la fila (1-3): "))
                        if fila not in [1, 2, 3]:  # Verificar rango
                            print("Número de fila no válido. Por favor, elige 1, 2 o 3.")
                            continue
                        columna = int(input("Selecciona la columna (1-3): "))
                        if columna not in [1, 2, 3]:  # Verificar rango
                            print("Número de columna no válido. Por favor, elige 1, 2 o 3.")
                            continue

                        # Intentar jugar el turno
                        if self.jugar_turno(nivel - 1, fila - 1, columna - 1):  # Ajustar índices a 0-2
                            return  # Terminar el juego si hay un ganador
                        break  # Salir del bucle si el turno fue válido
                    except (ValueError, IndexError):
                        print("Entrada inválida. Por favor, introduce un número entre 1 y 3.")
        print("¡Es un empate!")



# Iniciar el juego
if __name__ == "__main__":
    juego = TresEnRayaGrafo()
    juego.jugar()
