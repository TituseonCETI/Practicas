📘 README — Diferenciación Numérica con Interfaz Gráfica (Tkinter)
🔧 Descripción del proyecto
Este programa permite calcular derivadas numéricas a partir de una tabla de valores 
𝑥
𝑖
,
𝑦
𝑖
, utilizando distintos métodos de aproximación. La interfaz gráfica está diseñada con estilo Cyber-Neón y guía al usuario paso a paso en el proceso:

Ingreso de número de puntos

Captura de valores 
𝑥
 igualmente espaciados

Evaluación de función 
𝑓
(
𝑥
)
 o ingreso manual de 
𝑦

Selección del método de diferenciación

Cálculo de la derivada en un punto específico

🧮 Métodos de diferenciación implementados
Central 3 puntos (igualmente espaciado)

Extremo izquierdo (adelante)

Central simple

Extremo derecho (atrás)

Cada método incluye validaciones para asegurar que se cumplan las condiciones necesarias (por ejemplo, no estar en los extremos si se requiere).

🖥️ Requisitos
Python 3.7 o superior

Sistema operativo: Windows, macOS o Linux

Librerías estándar:

tkinter

math

No se requieren librerías externas.

🚀 Ejecución del programa
Clona el repositorio o descarga el archivo:

bash
git clone https://github.com/TituseonCETI/Practicas.git
Navega al directorio del proyecto:

bash
cd Practicas
Ejecuta el archivo principal:

bash
python Diferenciacion_Numerica_definitivo.py
🧭 Navegación por pantallas
Pantalla	Función
Pantalla 1	Ingreso de número de puntos 
𝑛
Pantalla 2	Captura de valores 
𝑥
𝑖
Pantalla 3	Evaluación de 
𝑓
(
𝑥
)
 o ingreso manual de 
𝑦
𝑖
Pantalla 4	Selección del método de diferenciación
Pantalla 5	Ingreso del índice 
𝑖
 para calcular derivada
🎨 Estilo visual
El programa utiliza un tema Cyber-Neón con colores oscuros y acentos turquesa para una experiencia moderna y clara. Las ventanas modales de error y resultado están estilizadas para mantener coherencia visual.

📂 Estructura del código
App: clase principal que gestiona la interfaz y el flujo entre pantallas.

mostrar_error(): ventana modal para mostrar errores.

mostrar_resultado(): ventana modal para mostrar resultados.

SAFE_MATH: diccionario seguro para evaluar funciones matemáticas.

Validaciones estrictas para entradas numéricas y espaciado constante.

🧠 Autoría y créditos
Desarrollado por Armando como parte de prácticas académicas en programación y métodos numéricos. Repositorio original: TituseonCETI/Practicas
