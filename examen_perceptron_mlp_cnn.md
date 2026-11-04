           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            EXAMEN TEÓRICO — PERCEPTRÓN, MLP Y CNN (GRUPO B)

                            Eduardo Alcaraz
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


1 Datos del alumno
══════════════════

  ━━━━━━━━━━━
   Nombre  Enrique Martinez
   Grupo   B 
   Fecha   03/11/2026  
  ━━━━━━━━━━━


2 Pregunta 1 — Por qué no basta “una sola neurona”
══════════════════════════════════════════════════

  1. Resume el funcionamiento de un perceptrón como “regla de decisión”.
  2. Explica la noción de *frontera lineal* sin escribir fórmulas.
  3. Da un ejemplo (aunque sea inventado) donde esa frontera *no*
     alcanza.


2.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Recibe varios datos, les da un peso, los ajusta y en base a ellos decide generalmente entre "si" y "no"
  2. Es la línea recta que separa dos clases, un lado cae una respuesta y del otro la contraria.
  3. Cuando la línea no es capaz de separar las clases y que estas esten mezcladas.


3 Pregunta 2 — CNN: de píxeles a mapas
══════════════════════════════════════

  1. ¿Qué problema de *estructura espacial* ignora un MLP si aplana la
     foto?
  2. ¿Qué significa que un mismo filtro se aplique en toda la imagen?
  3. Además de clasificación de objetos, cita *dos* usos donde la CNN
     encaja bien.


3.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Al aplanar la foto la convierte en una fila de números y pierde que pixeles estaban juntos.
  2. Busca el mismo patrón en cualquier parte.
  3. Detección de personas y detección de tumores.


4 Pregunta 3 — Softmax, clases y decisiones
═══════════════════════════════════════════

  1. Diferencia un problema *binario* de uno *multiclase* en términos de
     salida de la red.
  2. ¿Qué lectura le das a las probabilidades que produce un softmax?
  3. Imagina tres carpetas de imágenes (tres riesgos o tres animales):
     ¿qué arquitectura de *salida* usarías y por qué?


4.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. El binario solo tiene 2 salidas, el multiclase puede tener más de 3 y la red tiene una salida por cada clase.
  2. Convierte los resultados en probabilidades que suman 1. Elige la clase con mas probabilidades.
  3. SoftMax, además de una neurona por cada clase porque como cada imagen pertece a una carpeta, se elige la mas probable de esa clase.

5 Pregunta 4 — MLP: profundidad con sentido
═══════════════════════════════════════════

  1. ¿Qué ganas al apilar capas densas con activaciones no lineales?
  2. ¿Qué riesgo aparece si la red es *demasiado* grande para tus datos?
  3. Relaciona “capa oculta” con la idea de aprender representaciones
     intermedias (en palabras simples).


5.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Al apilarlas, la red puede aprender relaciones complicadas y no solo líneas rectas.
  2. El riesgo es el sobreajuste, si la red es enorme y tienes pocos datos, memoriza el entrenamiento, incluido el ruido, y falla con datos nuevos.
  3. Aprende representaciones intermedias. En reconocimiento de caras, por ejemplo, primero aparecen bordes y curvas, luego ojos y narices, y al final la cara completa.


6 Pregunta 5 — Entrenamiento sin magia
══════════════════════════════════════

  1. Explica qué es una *época* a nivel intuitivo.
  2. ¿Hacia qué “objetivo” se mueven los pesos cuando hablamos de
     minimizar el error?
  3. Si el learning rate es absurdo (muy grande o muy chico), ¿qué
     síntomas conceptuales esperarías?


6.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Una época es una pasada completa por todo el dataset usado para el entrenamiento. 
  2. Se busca que el error sea lo más pequeño que se pueda, para eso se ajustan los pesos.
  3. Si el learning rate es muy grande, el error salta de un lado a otro o hasta explota y si es muy chico, el aprendizaje tarda muchísimo y casi no se nota avance.


7 Pregunta 6 — Bloques de una CNN
═════════════════════════════════

  Sin matemáticas, di el papel de cada pieza:
  1. Kernel / filtro convolucional
  2. Función de activación después de conv
  3. Max pooling
  4. Capa densa + softmax al final de un clasificador


7.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Un detector pequeño que recorre la imagen buscando un patrón.
  2. Decide qué señal “se enciende” y le da a la red la capacidad de aprender cosas no lineales.
  3. Reduce el tamaño de la imagen quedándose con el valor más fuerte de cada zona. Resume la información y hace la red menos sensible a movimientos pequeños.
  4. Junta todo lo que detectaron los filtros y da la clasificación final con probabilidades.


8 Pregunta 7 — XOR y la historia del aprendizaje
════════════════════════════════════════════════

  1. ¿Por qué XOR se volvió un “contraejemplo” famoso?
  2. ¿Qué elemento de un MLP permite patrones que no son una sola línea?
  3. ¿En qué tipo de tabla/problema del mundo real seguirías usando algo
     tan simple como un perceptrón o un modelo lineal?


8.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. XOR se volvió famoso porque un perceptrón de una sola capa no puede aprenderlo. 
  2. Las capas ocultas con activaciones no lineales permiten fronteras curvas o por partes.
  3. Seguiría usando un modelo lineal cuando los datos se separan bastante bien con una línea o un plano, por ejemplo en un filtro simple o en predicciones con pocas variables.


9 Pregunta 8 — De lo simple a lo abstracto en visión
════════════════════════════════════════════════════

  1. Contrasta lo que buscan capas tempranas vs capas profundas en una
     CNN.
  2. ¿Qué intuición da eso para *transfer learning* (aunque no lo hayas
     programado)?
  3. ¿Cuándo sospecharías que tu CNN es “profunda de más” para el
     dataset del curso?


9.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Las capas tempranas buscan cosas básicas como bordes, líneas y colores. Las profundas combinan esas piezas hasta reconocer partes de objetos o el objeto completo.
  2. Como las capas tempranas aprenden cosas generales, puedes reutilizar una red ya entrenada y solo reentrenar las últimas capas.
  3. Sospecharía que la red es demasiado profunda si el error de entrenamiento baja pero el de validación sube o se queda estancado.


10 Pregunta 9 — Análisis: matching problema → modelo
════════════════════════════════════════════════════

  Elige *Perceptrón/lineal* / *MLP* / *CNN* (una opción) y justifica en
  una frase:

  1. Predecir “compra / no compra” con edad, ingreso y visitas a la web
     (columnas numéricas).
  2. Detectar si hay un gato en una foto.
  3. Aproximar una frontera “curva” o a trozos en datos 2D tabulares.
  4. ¿CNN es la herramienta natural para predecir la siguiente palabra
     de un párrafo? Justifica y nombra una familia del curso más
     adecuada (RNN/Transformer a nivel nombre).


10.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Perceptrón o modelo lineal: son datos tabulares sencillos y con pocas variables.
  2. CNN: es un problema de imagen, justo para lo que está diseñada.
  3. MLP: con capas ocultas puede aproximar fronteras curvas o por partes en datos tabulares 2D.
  4. CNN es para datos con estructura espacial como imágenes, no para secuencias de palabras. 


11 Pregunta 10 — Análisis: auditoría de un equipo
═════════════════════════════════════════════════

  Un equipo entrega un modelo “muy preciso” en su laptop y falla con
  datos nuevos.

  1. ¿Qué diagnósticos conceptuales harías *antes* de tocar
     hiperparámetros al azar?
  2. Pide *dos* evidencias que deberían mostrar en la defensa (curvas,
     separación train/val, ejemplos de error, etc.).
  3. Redacta *tres* preguntas tuyas para comprobar si saben cuándo usar
     perceptrón, MLP o CNN (distintas a las del Grupo A si las conoces).


11.0.1 Respuesta
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  1. Primero hay que revisar si los datos de prueba estaban realmente separados del entrenamiento, si la métrica “muy precisa” se midió con los mismos datos de entrenamiento, si los datos nuevos son parecidos a los originales.
  2. Dos evidencias: Los datos que usaron para entrenar y para probar, y cómo los separaron. Un ejemplo de datos nuevos que el modelo no había visto, con la predicción que dio y si acertó o no.
  3. ¿Qué modelo usarían para detectar imperfecciones en un remache de avión a partir de fotos? ¿Qué modelo usarían para saber si el clima está soleado, nublado o lluvioso analizando una imagen del cielo?
