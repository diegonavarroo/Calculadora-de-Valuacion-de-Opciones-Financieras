Proyecto derivados 
Integrantes del equipo:  
Adame Mejía Victor René 
Galindo Becerra Eduardo  
Hernández García Ángel  
Navarro Gomez Diego 
Rodríguez Jiménez Lorien Egladil Arellano 
Lopez Checa Aarón  
Realizamos una calculadora para la valuación de instrumentos financieros 
derivados, específicamente opciones financieras, mediante la implementación de un 
modelo binomial. 
Es importante mencionar que nuestro modelo considera opciones cuyo activo 
subyacente no paga dividendos durante la vigencia del contrato, por lo que este 
supuesto se mantiene en los cálculos realizados. 
La aplicación permite al usuario introducir diferentes parámetros del mercado y del 
activo subyacente para calcular el valor teórico de distintas opciones financieras. A 
partir de ello, genera una representación gráfica del árbol binomial, en la que se 
muestran los posibles precios que puede alcanzar el activo subyacente. 
El objetivo de este proyecto es facilitar la comprensión del proceso que se lleva a 
cabo para valuar una opción financiera, aplicando conocimientos matemáticos y de 
programación, para lograr un modelo binomial con una interfaz intuitiva. 
Nuestra calculadora es capaz de calcular 16 distintos tipos de opciones financieras, 
las cuales se dividen en tres categorías: las opciones europeas, las opciones 
americanas y, por último, las opciones exóticas. 
● Opciones europeas: Call europea y Put europea. 
● Opciones americanas: Call americana y Put americana. 
● Opciones exóticas: Lookback, Double No Touch, Call Digital, Put Digital, 
Call Up-and-Out, Put Up-and-Out, Call Down-and-Out, Put Down-and-Out, 
Call Up-and-In, Put Up-and-In, Call Down-and-In y Put Down-and-In. 
Una vez teniendo las opciones disponibles, procedemos a introducir los parámetros 
que el usuario debe proporcionar para calcular la opción deseada. Estos son: el 
precio inicial del activo subyacente, el strike, la tasa de interés libre de riesgo, el 
tiempo entre los periodos, el número de periodos y la volatilidad. 
Ya ingresados los parámetros correspondientes, la calculadora utiliza el modelo 
binomial para construir un árbol que representa los posibles movimientos del precio 
del activo subyacente. Una vez obtenidos, realiza los cálculos necesarios para 
determinar el valor teórico de la opción. Estos datos son procesados mediante las 
funciones del programa, que utilizan los valores ingresados para realizar las 
operaciones correspondientes y actualizar los resultados de acuerdo con el 
instrumento seleccionado. 
El procedimiento general consiste en seleccionar el instrumento financiero, introducir 
sus parámetros, construir el árbol binomial y aplicar el procedimiento de valuación 
correspondiente, para presentar el resultado obtenido junto con una representación 
gráfica del árbol. Para esto, el código utiliza estructuras condicionales que permiten 
identificar el tipo de opción seleccionada y ejecutar los cálculos específicos para 
cada instrumento. 
El modelo binomial, el cual es con el que estamos trabajando, nos permite 
determinar el valor teórico de una opción financiera mediante la representación de 
sus posibles movimientos, por lo que construimos un árbol en el que cada periodo 
tiene dos posibles trayectorias: subir o bajar. 
Para poder construirlo, necesitamos los siguientes parámetros: precio inicial del 
activo subyacente, factor de subida (u), factor de bajada (d), tasa de interés libre de 
riesgo (R), probabilidad neutral al riesgo de subir y probabilidad neutral al riesgo de 
bajar. El código utiliza estos parámetros para calcular los posibles precios del activo 
en cada nodo, almacenando los valores obtenidos para posteriormente utilizarlos en 
el proceso de valuación. 
Una vez construido el árbol de los precios, se determinan los payoffs y 
posteriormente se utiliza el procedimiento llamado backward induction para calcular 
su valor en los periodos anteriores hasta llegar al momento inicial. Este proceso se 
implementa mediante ciclos que recorren los diferentes periodos del árbol en 
sentido inverso, calculando en cada nodo el valor correspondiente a partir de los 
valores de los nodos siguientes, las probabilidades neutrales al riesgo y el factor de 
descuento. 
En el caso de las opciones americanas, además del valor obtenido por continuación, 
se considera la posibilidad de ejercer anticipadamente el derecho que se tiene, por 
lo que se compara el valor de continuación con el valor que se obtendría si se 
ejerciera inmediatamente. De esta manera, el programa evalúa ambas posibilidades 
en cada nodo y conserva el mayor valor para determinar la valuación de la opción. 
Para el desarrollo de la calculadora, utilizamos Python como lenguaje de 
programación, acompañado de distintas bibliotecas que permitieron realizar los 
cálculos. Para la interfaz gráfica usamos Streamlit y para la estructura del árbol 
binomial utilizamos NetworkX. Por último, nos apoyamos de Matplotlib para generar 
y visualizar las gráficas con los posibles precios del subyacente y con los valores 
correspondientes de la opción. También utilizamos arreglos para almacenar los 
valores calculados durante el proceso de valuación, lo que permite organizar la 
información y utilizarla tanto en los cálculos posteriores como en la representación 
gráfica del árbol.
