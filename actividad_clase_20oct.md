# Comparación de modelos de reconocimiento facial: LBPH vs Eigenfaces vs Fisherfaces

## 1. Dataset

- **Personas (6 clases):** cesare, jose, kike, pau, tony y vegetta.
- **Obtención:** los rostros se extrajeron de videos con el detector Haar (1 de cada 5 fotogramas) y se guardaron en escala de grises, de 100×100 px.

### 1.1 Evaluación controlada

Además de la prueba en cámara, se reentrenaron los tres modelos con las mismas imágenes para medir su precisión:

| Aspecto | Configuración |
|---|---|
| Personas del modelo | cesare, kike, pau y tony (4 clases) |
| Personas desconocidas | jose y vegetta, excluidas del entrenamiento (600 imágenes) |
| Entrenamiento | 300 imágenes por persona (1,200 en total), las mismas para los tres modelos |
| Prueba | 1,089 imágenes de las 4 personas, distintas a las de entrenamiento |
| Umbrales | Los mismos que en la cámara |

## 2. Configuración de los modelos originales

| Aspecto | LBPH | Eigenfaces | Fisherfaces |
|---|---|---|---|
| Imágenes por persona en el entrenamiento | Todas | Hasta 500 | Hasta 300 |
| Umbral para "Desconocido" | 200 | 5000 | 500 |

- Los tres usan el mismo detector de rostros (Haar) e imágenes de 100×100 en escala de grises.
- Los umbrales se subieron respecto a los valores por defecto porque con estos la cámara no reconocía a nadie.
- Los umbrales **no son comparables entre sí**, porque cada algoritmo mide la distancia de forma distinta.

## 3. Comparación teórica

| Criterio | LBPH | Eigenfaces | Fisherfaces |
|---|---|---|---|
| Qué representa | Histogramas de textura local | Componentes de máxima varianza (PCA) | Componentes que separan clases (PCA + LDA) |
| Robustez a la iluminación | Alta | Baja | Media |
| Robustez a expresión y pose | Media | Baja | Media |
| Uso de las etiquetas al aprender | Solo al clasificar | No (PCA no supervisado) | Sí (LDA supervisado) |
| Tamaño del modelo | Crece con cada imagen | Hasta N − 1 componentes | Máximo C − 1 componentes |
| Entrenamiento incremental | Sí | No | No |
| Costo de predicción | Mayor (compara con todos los histogramas) | Bajo | Bajo |
| Tipo de distancia | Chi-cuadrada entre histogramas | Euclidiana en el subespacio | Euclidiana en el subespacio |

### 3.1 Ejemplo: la convolución en una CNN
 
Los tres modelos comparados usan características definidas a mano (texturas locales, varianza o separación entre clases). Una red neuronal convolucional (CNN) usa en cambio **filtros que aprende durante el entrenamiento**. Su operación básica es la convolución: se desliza un filtro pequeño sobre la imagen y, en cada posición, se multiplican sus valores por los píxeles que cubre y se suman los resultados.
 
Ejemplo con una imagen de 4×4 píxeles (valores de ejemplo) y un filtro de 3×3 que promedia la vecindad (todos sus valores son 1/9):
 
| Imagen | | | |
|---|---|---|---|
| 10 | 20 | 30 | 40 |
| 50 | 60 | 70 | 80 |
| 90 | 100 | 110 | 120 |
| 130 | 140 | 150 | 160 |
 
Primera posición (esquina superior izquierda):
 
(10 + 20 + 30 + 50 + 60 + 70 + 90 + 100 + 110) × 1/9 = 540 / 9 = **60**
 
Al repetirlo en las cuatro posiciones posibles se obtiene un mapa de características de 2×2:
 
| | |
|---|---|
| 60 | 70 |
| 100 | 110 |
 
Con un filtro de promedio el resultado es solo una versión suavizada de la imagen. En una CNN real los nueve valores del filtro **no son fijos, se aprenden**, de modo que cada filtro termina detectando algo útil (bordes, texturas, partes del rostro). Se usan muchos filtros en varias capas y al final una capa clasifica a la persona. Por lo general esto la hace más robusta a cambios de luz y pose, a cambio de requerir más datos y más cómputo.

## 4. Resultados

### 4.1 Observación en cámara (modelos originales)

Pruebas en tiempo real con la cámara del equipo, sin métricas numéricas.

| Aspecto | LBPH | Eigenfaces | Fisherfaces |
|---|---|---|---|
| Tiempo de entrenamiento (percepción) | Rápido, poco notorio incluso con todas las imágenes | Lento | Lento |
| Tamaño del archivo del modelo | 907,874 KB (≈ 887 MB) | 925,092 KB (≈ 903 MB) | 1,826 KB (≈ 1.8 MB) |
| ¿Reconoció correctamente a las personas? | Sí | Sí, pero le costó mucho más | Sí |
| Solidez general | **1.º (más sólido)** | 3.º | 2.º |
| Luz tenue a normal | Buen desempeño | Buen desempeño | Buen desempeño |
| Contraluz | Dificultad | Dificultad | Dificultad |

El tamaño refleja lo que guarda cada algoritmo: LBPH, el histograma de cada imagen; Eigenfaces, todos los componentes principales; y Fisherfaces, solo C − 1 = 5.

### 4.2 Evaluación controlada

Se probaron 1,089 imágenes de personas del modelo y 600 de personas desconocidas.

#### Resumen

| Métrica | LBPH | Eigenfaces | Fisherfaces |
|---|---|---|---|
| Umbral usado | 200 | 5000 | 500 |
| Precisión con umbral (%) | 92.65 | 88.98 | **94.31** |
| Precisión sin umbral (%) | 92.65 | 89.35 | **94.31** |
| Conocidos rechazados como "Desconocido" (%) | 0.00 | 0.37 | 0.00 |
| Falsos positivos con desconocidos (%) | 100.00 | 99.17 | 100.00 |
| Distancia media en aciertos | 71.2 | 2355.9 | 74.9 |
| Distancia media en errores/rechazos | 97.5 | 3471.9 | 152.9 |
| Distancia media en desconocidos | 101.6 | 3705.8 | 146.4 |
| Tiempo de predicción (ms/imagen) | 19.40 | 6.33 | **0.20** |
| Tiempo de entrenamiento (s) | **1.5** | 76.9 | 79.4 |
| Tamaño del modelo (MB) | 104.9 | 315.5 | **1.1** |

*Precisión con umbral*: la persona debe ser correcta y la distancia menor al umbral. *Precisión sin umbral*: solo cuenta que la etiqueta predicha sea la correcta.

#### Precisión por persona (aciertos con umbral / total)

| Persona | LBPH | Eigenfaces | Fisherfaces |
|---|---|---|---|
| cesare | 263/263 (100.0%) | 259/263 (98.5%) | 258/263 (98.1%) |
| kike | 276/277 (99.6%) | 275/277 (99.3%) | 277/277 (100.0%) |
| pau | 294/296 (99.3%) | 294/296 (99.3%) | 284/296 (95.9%) |
| tony | 176/253 (69.6%) | 141/253 (55.7%) | 208/253 (82.2%) |

#### Matrices de confusión

**LBPH**

| Real \ Predicho | cesare | kike | pau | tony | Desconocido |
|---|---|---|---|---|---|
| **cesare** | 263 | 0 | 0 | 0 | 0 |
| **kike** | 0 | 276 | 1 | 0 | 0 |
| **pau** | 0 | 0 | 294 | 2 | 0 |
| **tony** | 0 | 24 | 53 | 176 | 0 |

**Eigenfaces**

| Real \ Predicho | cesare | kike | pau | tony | Desconocido |
|---|---|---|---|---|---|
| **cesare** | 259 | 4 | 0 | 0 | 0 |
| **kike** | 0 | 275 | 2 | 0 | 0 |
| **pau** | 0 | 0 | 294 | 2 | 0 |
| **tony** | 0 | 5 | 103 | 141 | 4 |

**Fisherfaces**

| Real \ Predicho | cesare | kike | pau | tony | Desconocido |
|---|---|---|---|---|---|
| **cesare** | 258 | 5 | 0 | 0 | 0 |
| **kike** | 0 | 277 | 0 | 0 | 0 |
| **pau** | 6 | 4 | 284 | 2 | 0 |
| **tony** | 4 | 4 | 37 | 208 | 0 |

## 5. Análisis

- **Precisión.** Fisherfaces (94.31 %) y LBPH (92.65 %) quedaron muy cerca: la diferencia es de 18 imágenes de 1,089 y no hay un ganador claro por persona. Eigenfaces (88.98 %) quedó claramente detrás, igual que en la cámara.
- **Cámara contra evaluación controlada.** En cámara LBPH se percibió como el más sólido, y en la evaluación controlada Fisherfaces quedó apenas arriba. Dos explicaciones posibles, que son hipótesis: el LBPH original se entrenó con todas las imágenes y aquí se igualó a 300 por persona; y la evaluación no incluye la variación de luz de la cámara en vivo, donde LBPH, por basarse en textura local, debería defenderse mejor. Como la prueba usa imágenes del mismo dataset, sirve sobre todo para comparar los modelos entre sí.
- **Costo computacional.**
  - *LBPH:* entrena casi al instante (1.5 s), pero su modelo es grande y es el más lento al predecir (19.4 ms); ambos crecen con el número de imágenes.
  - *Eigenfaces:* entrena lento (76.9 s), con un modelo grande (315.5 MB) y la menor precisión.
  - *Fisherfaces:* entrena lento (79.4 s), pero su modelo pesa solo 1.1 MB y predice unas 100 veces más rápido que LBPH.
- **Contraluz.** Los tres tuvieron problemas, y lo más probable es que falle la **detección** (el detector Haar es el mismo en los tres) y no el reconocimiento. Se puede comprobar: si no aparece el recuadro sobre el rostro, falló el detector; si aparece como "Desconocido" o con el nombre equivocado, falló el reconocedor.
- **Comparabilidad.** En la evaluación controlada los tres modelos usaron exactamente las mismas imágenes, lo que corrige la diferencia de datos de los modelos originales.

## 6. Conclusión

- **Eigenfaces fue el más débil en ambas pruebas**: peor precisión (88.98 %), el que más le costó reconocer en cámara, entrenamiento lento y modelo grande.
- **Fisherfaces y LBPH tuvieron un desempeño parecido**: Fisherfaces quedó ligeramente arriba en la evaluación controlada (94.31 % contra 92.65 %) y LBPH se percibió como el más sólido en cámara.
- **Fisherfaces es el más eficiente** (modelo de 1.1 MB y predicción unas 100 veces más rápida que LBPH), aunque entrena lento. **LBPH es el más cómodo de entrenar** (1.5 s) y, por su base en textura local, se espera que tolere mejor los cambios de luz, a cambio de un modelo grande y una predicción más lenta.
- **Recomendación según el criterio:** LBPH si se priorizan condiciones reales variables y la facilidad de reentrenar; Fisherfaces si se prioriza el tamaño y la velocidad con condiciones parecidas a las del entrenamiento.
