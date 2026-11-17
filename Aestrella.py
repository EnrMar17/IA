"""
A* "Evaluación Asterisco"
--------------------------------------------------------
Materia: Inteligencia Artificial
Alumno : Enrique Martinez - 22121275

Reglas:
  - La búsqueda parte de la SALIDA y termina en el INICIO
    (por eso la Lista Cerrada empieza con la SALIDA).
  - Movimiento en 8 direcciones: recto = 10, diagonal = 14.
  - h(n) = distancia Manhattan * 10 hacia el objetivo.
  - f(n) = g(n) + h(n).
  - Se expande el nodo de La con menor f. Si hay empate, el que entró primero.
  - Cada celda muestra su número, g, h, f y una flecha roja hacia su PADRE.
  - Azul = ya está en la Lista Cerrada (Lc). Gris = pared.

Controles:
    ESPACIO / FLECHA DERECHA -> siguiente paso
    FLECHA IZQUIERDA         -> paso anterior
    A                        -> avance automático (on/off)
    F                        -> ir al final
    R                        -> reiniciar
    E                        -> modo editar paredes (clic para poner/quitar)
    S + clic (en modo editar)-> mover SALIDA
    I + clic (en modo editar)-> mover INICIO
    D                        -> cargar el tablero de ejemplo (7x9)
    Q / ESC                  -> salir
"""

import pygame

FILAS = 7
COLUMNAS = 9
TAM = 90
BARRA = 50

NO_CORTAR_ESQUINAS = False

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (110, 110, 110)
AZUL = (140, 180, 255)
VERDE = (190, 240, 190)
AMARILLO = (255, 235, 120)
ROJO = (220, 30, 30)

DIRECCIONES = [
    (-1, 0, 10), (1, 0, 10), (0, -1, 10), (0, 1, 10),
    (-1, -1, 14), (-1, 1, 14), (1, -1, 14), (1, 1, 14),
]


def tablero_ejemplo():
    paredes = {(1, 4), (2, 4), (3, 4), (4, 4), (5, 4)}
    salida = (3, 7)
    inicio = (3, 1)
    return paredes, salida, inicio


def heuristica(celda, objetivo):
    return (abs(celda[0] - objetivo[0]) + abs(celda[1] - objetivo[1])) * 10


def agregar_vecinos(actual, paredes, g, padre, abierta, cerrada):
    for df, dc, costo in DIRECCIONES:
        vecino = (actual[0] + df, actual[1] + dc)

        if not (0 <= vecino[0] < FILAS and 0 <= vecino[1] < COLUMNAS):
            continue
        if vecino in paredes or vecino in cerrada:
            continue

        if NO_CORTAR_ESQUINAS and costo == 14:
            if (actual[0] + df, actual[1]) in paredes or (actual[0], actual[1] + dc) in paredes:
                continue

        nuevo_g = g[actual] + costo
        if vecino not in abierta:
            abierta.append(vecino)
            g[vecino] = nuevo_g
            padre[vecino] = actual
        elif nuevo_g < g[vecino]:
            g[vecino] = nuevo_g
            padre[vecino] = actual


def correr_astar(paredes, salida, inicio):
    g = {salida: 0}
    padre = {}
    abierta = []
    cerrada = [salida]
    pasos = []

    def foto():
        pasos.append((list(abierta), list(cerrada), dict(g), dict(padre)))

    agregar_vecinos(salida, paredes, g, padre, abierta, cerrada)
    foto()

    while abierta and inicio not in cerrada:

        mejor = min(abierta, key=lambda n: g[n] + heuristica(n, inicio))
        abierta.remove(mejor)
        cerrada.append(mejor)
        agregar_vecinos(mejor, paredes, g, padre, abierta, cerrada)
        foto()

    return pasos


def obtener_camino(padre, salida, inicio):
    camino = []
    nodo = inicio
    while nodo in padre or nodo == salida:
        camino.append(nodo)
        if nodo == salida:
            break
        nodo = padre[nodo]
    return camino


def numero_celda(celda):
    return celda[0] * COLUMNAS + celda[1] + 1


def centro(celda):
    return (celda[1] * TAM + TAM // 2, celda[0] * TAM + TAM // 2)


def dibujar_flecha(pantalla, celda, padre_celda):
    x1, y1 = centro(celda)
    df = padre_celda[0] - celda[0]
    dc = padre_celda[1] - celda[1]

    ini = (x1 - dc * 12, y1 - df * 12)
    fin = (x1 + dc * 26, y1 + df * 26)
    pygame.draw.line(pantalla, ROJO, ini, fin, 3)

    if dc != 0 and df != 0:
        puntas = [(fin[0] - dc * 9, fin[1]), (fin[0], fin[1] - df * 9)]
    elif dc != 0:
        puntas = [(fin[0] - dc * 9, fin[1] - 7), (fin[0] - dc * 9, fin[1] + 7)]
    else:
        puntas = [(fin[0] - 7, fin[1] - df * 9), (fin[0] + 7, fin[1] - df * 9)]
    for p in puntas:
        pygame.draw.line(pantalla, ROJO, fin, p, 3)


def dibujar(pantalla, fuente, fuente_chica, paredes, salida, inicio,
            estado, indice, total, camino, editando, auto):
    abierta, cerrada, g, padre = estado
    pantalla.fill(BLANCO)

    for f in range(FILAS):
        for c in range(COLUMNAS):
            celda = (f, c)
            rect = pygame.Rect(c * TAM, f * TAM, TAM, TAM)

            if celda in paredes:
                color = GRIS
            elif celda in camino:
                color = AMARILLO
            elif celda in cerrada:
                color = AZUL
            elif celda in abierta:
                color = VERDE
            else:
                color = BLANCO
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)

            txt = fuente_chica.render(str(numero_celda(celda)), True, (90, 90, 90))
            pantalla.blit(txt, (rect.right - txt.get_width() - 4, rect.bottom - 18))

            if celda in paredes:
                continue

            if celda == salida:
                pantalla.blit(fuente.render("SALIDA", True, NEGRO), (rect.x + 18, rect.y + 36))
            if celda == inicio:
                pantalla.blit(fuente.render("INICIO", True, NEGRO), (rect.x + 20, rect.y + 36))

            if celda in g:
                h = heuristica(celda, inicio)
                pantalla.blit(fuente.render(str(g[celda]), True, NEGRO), (rect.x + 5, rect.y + 3))
                pantalla.blit(fuente.render(str(h), True, NEGRO), (rect.right - 30, rect.y + 3))
                pantalla.blit(fuente.render(str(g[celda] + h), True, NEGRO), (rect.x + 5, rect.bottom - 22))

            if celda in padre:
                dibujar_flecha(pantalla, celda, padre[celda])

    y = FILAS * TAM
    pygame.draw.rect(pantalla, (235, 235, 235), (0, y, COLUMNAS * TAM, BARRA))
    if editando:
        msg = "EDITAR: clic=pared, S+clic=salida, I+clic=inicio, E=salir"
    else:
        msg = "Paso %d/%d | Auto: %s | ESPACIO/IZQ, A, F, R, E" % (
            indice, total - 1, "ON" if auto else "OFF")
        if indice == total - 1:
            msg = ("Camino encontrado | " if camino else "No hay camino | ") + msg
    pantalla.blit(fuente_chica.render(msg, True, NEGRO), (8, y + 16))
    pygame.display.flip()


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((COLUMNAS * TAM, FILAS * TAM + BARRA))
    pygame.display.set_caption("A* - Evaluación Asterisco")
    fuente = pygame.font.SysFont("arial", 18, bold=True)
    fuente_chica = pygame.font.SysFont("arial", 14)
    reloj = pygame.time.Clock()

    paredes, salida, inicio = tablero_ejemplo()
    pasos = correr_astar(paredes, salida, inicio)
    indice = 0
    editando = False
    auto = False
    ultimo_auto = 0

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                tecla = evento.key
                if tecla in (pygame.K_q, pygame.K_ESCAPE):
                    corriendo = False
                elif tecla in (pygame.K_SPACE, pygame.K_RIGHT):
                    indice = min(indice + 1, len(pasos) - 1)
                elif tecla == pygame.K_LEFT:
                    indice = max(indice - 1, 0)
                elif tecla == pygame.K_a:
                    auto = not auto
                elif tecla == pygame.K_f:
                    indice = len(pasos) - 1
                elif tecla == pygame.K_r:
                    indice = 0
                    auto = False
                elif tecla == pygame.K_e:
                    editando = not editando
                    auto = False
                elif tecla == pygame.K_d:
                    paredes, salida, inicio = tablero_ejemplo()
                    pasos = correr_astar(paredes, salida, inicio)
                    indice = 0

            elif evento.type == pygame.MOUSEBUTTONDOWN and editando:
                x, y = evento.pos
                celda = (y // TAM, x // TAM)
                if 0 <= celda[0] < FILAS and 0 <= celda[1] < COLUMNAS:
                    teclas = pygame.key.get_pressed()
                    if teclas[pygame.K_s]:
                        if celda not in paredes and celda != inicio:
                            salida = celda
                    elif teclas[pygame.K_i]:
                        if celda not in paredes and celda != salida:
                            inicio = celda
                    elif celda != salida and celda != inicio:
                        if celda in paredes:
                            paredes.remove(celda)
                        else:
                            paredes.add(celda)

                    pasos = correr_astar(paredes, salida, inicio)
                    indice = 0

        if auto and not editando:
            ahora = pygame.time.get_ticks()
            if ahora - ultimo_auto > 500:
                ultimo_auto = ahora
                if indice < len(pasos) - 1:
                    indice += 1
                else:
                    auto = False

        estado = pasos[indice]
        camino = []
        if indice == len(pasos) - 1 and inicio in estado[1]:
            camino = obtener_camino(estado[3], salida, inicio)

        dibujar(pantalla, fuente, fuente_chica, paredes, salida, inicio,
                estado, indice, len(pasos), camino, editando, auto)
        reloj.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
