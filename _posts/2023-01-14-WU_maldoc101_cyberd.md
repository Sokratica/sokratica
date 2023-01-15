---
layout: post
comments: false
title : Writeup | CyberDefenders | MalDoc101
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, MalDoc101, Análisis de Malware, Maldocs, Análisis de Documentos Maliciosos
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto MalDoc101 de la plataforma Cyberdefenders.org"
---

# Índice

1. [Preámbulo](#pre)\\
    1.1 [Introducción](#intro)\\
2. [Write Up](#wu)\\
    2.1 [Pregunta 1](#p1)\\
    2.2 [Pregunta 2](#p2)\\
    2.3 [Pregunta 3](#p3)\\
    2.4 [Pregunta 4](#p4)\\
    2.5 [Pregunta 5](#p5)\\
    2.6 [Pregunta 6](#p6)\\
    2.7 [Pregunta 7](#p7)\\
    2.8 [Pregunta 8](#p8)\\
    2.9 [Pregunta 9](#p9)\\
3. [Preguntas y respuestas](#pyr)

# Preámbulo <a name="pre"></a>

<html>
<body>
<style>
table, th, td {
  border:1px solid black;
}
</style>
</body>
</html>

|Info|Descripción|
|----|-----------|
|Reto|MalDoc101|
|SHA1SUM|4d482527cf63400dc98ff574903f1ea7dbffb6cd|
|Autor|Josh Stroschein|
|Tags|Macro, Oledump, base64, Malicious Document|


## Escenario

Es común que los actores de amenazas utilicen técnicas de Living Off The Land (LOTL), como la ejecución de PowerShell para avanzar en sus ataques y la transición de código de macros. Este desafío pretende mostrar cómo se puede realizar a menudo un análisis rápido para extraer COI importantes. Este ejercicio se centra en técnicas estáticas de análisis.


## Herramientas

- REMnux Virtual Machine
- Oletools
    - Oledump
	- Olevba
	- Oledir
- Virustotal
- Cyberchef


## Introducción <a name="intro"></a>

Como antecedente, que sepas en en este mismo blog hay un post en el que analicé un maldoc (documento malicioso) como parte del curso "Practical Malware Analysis" de TCM Academy. En éste se extrae un binario dentro de un documento Excel (te dejo la referencia por si quieres echarle un ojo, allí hay un poco más de información al respecto[^1]).

En este reto, sin embargo, se nos provee directamente de un binario sobre el cual realizaremos el análisis. La herramienta que usaremos, como en el ejemplo a los cuales dirijo, es "oledump" que no es otra cosa más que una herramienta programada en python que nos permite analizar documentos OLE ("Object Linking & Embedding") desde la cual se puede ver la información de estos documentos.

Si tienes dudas, ya sabes que me puedes contactar en mi Twitter.

---

# WriteUp <a name="wu"> </a>

## **1. Este documento contiene varias macros. Indique el número de la más alta.** <a name="p1"></a>

Como primer movimiento estratégico y, sobretodo, como buenas práctica yo renombré el fichero para evitar desastres. Esto es recomendable porque imagínate que tienes en frente un maldoc identificado por tu empresa y no tienes medidas las consecuencias de lo que podría ocurrir si abres/ejecutas el documento/binario. Al final del día, cualquiera puede missclickear cualquier archivo y comprometer su equipo. Así, entonces, yo agregué un ".malz" como extensión del fichero para que, si llegase a missclickearlo, no se ejecute nada.

Con lo anterior dicho, pues, lo primero que hay que hacer no es otra cosa más que ejecutar el comando:

```
oledump.py sample.bin.malz
```

Lo que nos arroja la herramienta es lo siguiente:

![[WriteUps/CyberDefenders/MalDoc101/imgs/img1.png]]

- Como primer indicador de potencial riesgo son aquellos objetos que tienen una "M/m" inmediatamente después del índice asociado. Esta letra describe una propiedad del objeto señalado que, en este caso, se trata de un objeto que es una macro. 

- De esta manera, tenemos los objetos 13, 15 y 16 son los que tienen macros embebidas.


## **2. ¿Qué evento se utiliza para iniciar la ejecución de las macros?** <a name="p2"></a>

La segunda herramienta que usaremos para este paso es "olevba". Es importante mencionar que esta herramienta y la anterior que hemos usado viene preinstaladas en la MV Remnux la cual es ampliamente usada para hacer análisis de malware (te dejo el link a pie de página a la web oficial desde donde puedes descargarte la iso y leer más sobre este proyecto)[^2].

Ejecutamos la herramienta sobre nuestro binario malicioso. El output es una locura de grande, pero lo que nos interesa para esta pregunta viene al principio:

```
olevba.py sample.bin.malz
```

![[WriteUps/CyberDefenders/MalDoc101/imgs/img2.png]]

- La respuesta a la pregunta ye la señalo en un recuadro rojo. Sin embargo, hay otras cosas interesantes que señalar.

- Como puedes ver, lo que se nos arroja por pantalla tiene, más o menos, el siguiente formato: nombre del objeto (que la herramienta te muestra los que ya está identificados como macros) y su contenido.

    - Así pues, si tienes al lado tuyo el output cuando corrimos el oledump sobre el binario, podrás observar que el nombre de la macro (1) se corresponde con el objeto 13 identificado como una macro, lo puedes constatar porque tienen el mismo nombre aunque en olevba no te indique el índice de los objetos. Lo mismo ocurre para las macros (2) y (3) arriba señaladas.

- En una búsqueda "exhaustiva" por Google puedes encontrar que "Document_open()" es el evento por medio del cual, los documentos ofimáticos de Microsoft, simplemente se abren para que los puedas visualizar en tu programa. La estructura de esta función es la siguiente (te dejo varios links para que puedas obtener más información sobre este evento, el método open de VBA y qué es VBA (Visual Basic for Applications)[^3]:

```
Private Sub Document_open()
	nombre_del_fichero
End Sub
```

- Con esta información adicional podemos afirmar que el lo que está tratando de abrir el binario es un objeto llamado "boaxvoebxiotqueb":

![[WriteUps/CyberDefenders/MalDoc101/imgs/img3.png]]

**Nota: no agregues los paréntesis en la respuesta.**


## **3. ¿Qué familia de malware intentaba soltar este maldoc?** <a name="p3"></a>


Para este paso lo que hice fue sacar el hash del binario, subirlo a Virustotal y con la información encontrada sacar conclusiones:

```
shasum sample.bin.mlz
```

![[WriteUps/CyberDefenders/MalDoc101/imgs/img4.png]]

- Para nuestra buena suerte, ya se había identificado previamente este malware por lo que hay bastante información sobre él.

![[WriteUps/CyberDefenders/MalDoc101/imgs/img5.png]]

- Respuesta rápida: el malware es de la familia **Emotet**. Pero, ¿qué significa eso? En la página de Karspersky se puede leer lo siguiente[^4]:

> "Emotet es un malware que se concibió originalmente como un troyano bancario. Su fin era obtener acceso a dispositivos en otros países y espiar información privada confidencial. Emotet es famoso por su capacidad de engañar a los programas antivirus básicos y esconderse de ellos. Una vez infectado, el malware se propaga como un gusano informático e intenta infiltrarse en otras computadoras de la red.
 
> La principal vía de propagación de Emotet son los correos electrónicos de spam. Dicho correo electrónico contiene un vínculo malicioso o un documento infectado. Si se descarga el documento o se abre el vínculo, se descargará automáticamente más malware en tu computadora.

> Emotet fue detectado por primera vez en 2014, cuando los clientes de bancos alemanes y austriacos se vieron afectados por este troyano. Emotet había obtenido acceso a los datos de inicio de sesión de los clientes. En los años siguientes, el virus se propagó a escala mundial.

> Emotet pasó de ser un troyano bancario a un _dropper_, lo que significa que descarga programas maliciosos en los dispositivos. Estos son los responsables de los daños reales en el sistema."


## **4. ¿Qué stream es responsable del almacenamiento de la cadena codificada en base64?** <a name="p4"></a>

Para responder a esta pregunta no necesitamos ejecutar ningún nuevo comando. Si aún tienes el output cuando corrimos el "olevba", si recorres los resultados llegarás eventualmente a ver una cadena de caracteres enorme que están en base64 (te pongo como evidencia sólo una parte de la string):

![[WriteUps/CyberDefenders/MalDoc101/imgs/img6.png]]

- Lo que a nosotros nos interesa es identificar qué cadena es responsable de esto. Como lo mencioné anteriormente, la herramienta nos da el nombre del objeto que está analizando. Si contrastamos el nombre con la lista que arroja el "oledump" podemos ver que corresponde al objeto **34**.

- En un escenario en el que no supiéramos que hay una cadena en base64, podríamos obtener este hecho revisando el "resumen" del comportamiento del binario que se encuentra al final de todo el output del "olevba":

![[WriteUps/CyberDefenders/MalDoc101/imgs/img7.png]]


## **5. Este documento contiene un formulario de usuario. Da el nombre.** <a name="p5"></a>

La respuesta a esta pregunta es sencilla. ¿Recuerdas que el "oledump" te ofrece información sobre los objetos encontrados en el binario? Pues la "m" significa que se trata de un "formulario", similar a como "M" indica la presencia de macros. Por lo que el objeto que nos interesa para esta pregunta es el **16**.

- Alternativamente, podemos usar otra de las herramientas de "oletools" para visualizar la estructura del binario como directorios y subdirectorios:

```
oledir sample.bin.malz
```

![[WriteUps/CyberDefenders/MalDoc101/imgs/img8.png]]


## **6. Este documento contiene una cadena codificada en base64 ofuscada; ¿qué valor se utiliza para rellenar (u ofuscar) esta cadena?** <a name="p6"></a>

Este paso es un poco tedioso pues hay que analizar lo que hay dentro de las macros. Con lo que nos arroja el "olevba" podemos responder a esta pregunta. Si vamos revisando el output veremos que empieza a ver "strings" que parecen asignación de valores, llamadas a funciones, etc.:

![[WriteUps/CyberDefenders/MalDoc101/imgs/img9.png]]

- Revisando la información, podemos ver que estas llamadas a funciones perteneces al objeto llamado "govwiahtoozfaid" número **15** (una macro).

- Con esta información lo que podemos hacer es correr el "oledump" de nuevo para ver los procesos relacionados con el objeto de nuestro interés:

```
oledump.py -s 15 --vbadecompresscorrupt sample.bin.malz
```

- *Grosso modo*, lo que veremos inmediatamente son una serie de bucles, asignación de variables, reemplazos, etc. Para darme una pista de lo que estamos buscando, le eché un ojo a la enorme cadena string en base64 y lo que se puede ver es que hay una cadena que se repite constantemente: `2342772g3&*gs7712ffvs626fq`.

- Analizando los resultados del último comando que corrimos podemos ver que hay una línea que "splitea" justamente esa cadena:

![[WriteUps/CyberDefenders/MalDoc101/imgs/img10.png]]

- La cadena de caracteres que se está spliteando es nuestra respuesta.


## **7. ¿Cuál es el programa ejecutado por la cadena codificada en base64?** <a name="p7"></a>

Aquí es donde recurrimos a nuestro chef preferido: el cyberchef. De antemano ya sabemos que el objeto 34 es donde se almacena la string codificada en base64. Lo que podemos hacer es dumpear esa información para poder manipularla más fácilmente:

```
oledump.py -s 34 -d sample.bin.malz > dumped64.txt
```

- Copiamos y pegamos todo como input en el cyberchef. Vamos a utilizar la función "Find/Replace" para buscar la cadena de la pregunta anterior, que es la cadena en base64 ofuscada que encontramos.
- Hay que asegurarnos de buscarla como "cadena simple" y como output obtendremos nuestro tesoro:

![[WriteUps/CyberDefenders/MalDoc101/imgs/img11.png]]


## **8. ¿Qué clase WMI se utiliza para crear el proceso para lanzar el troyano?** <a name="p8"></a>

Para responder a esta pregunta vamos a reciclar el output del cyberchef y usarlo, ahora, como input. Le pasamos la función "From base64" y podemos ver el código malicioso (**asegúrate de quitar la string "powersheLL -e"**):

- Funciones que utilizaremos para esta receta:
	- From Base64
	- Generic Code Beauty
	- Remove null bytes

![[Pasted image 20230114192511.png]]

- Allí podemos ver cómo se define la wmiclass a "win32_Process".


## **9. Varios dominios fueron conectados para descargar un troyano. Proporcione el primer FQDN según la pista proporcionada.** <a name="p9"></a>

En el mismo resultado del código en texto claro podemos ver todas las llamadas a los dominios:

![[Pasted image 20230114192953.png]]

- De allí extraemos sólo la primera y esa es nuestra respuesta.

---

# Preguntas y respuestas <a name="pyr"></a>

1. Este documento contiene varias macros. Indique el número de la más alta. **R: 16**

2. ¿Qué evento se utiliza para iniciar la ejecución de las macros? **R: Document_open**

3. ¿Qué familia de malware intentaba soltar este maldoc? **R: emotet**

4. ¿Qué stream es responsable del almacenamiento de la cadena codificada en base64? **R: 34**

5. Este documento contiene un formulario de usuario. Da el nombre. **R: roubhaol**

6. Este documento contiene una cadena codificada en base64 ofuscada, ¿qué valor se utiliza para rellenar (u ofuscar) esta cadena? **R: 2342772g3&*gs7712ffvs626fq** 

7. ¿Cuál es el programa ejecutado por la cadena codificada en base64? **R: powershell**

8. ¿Qué clase WMI se utiliza para crear el proceso para lanzar el troyano? **R: win32_process**

9. Varios dominios fueron conectados para descargar un troyano. Proporcione el primer FQDN según la pista proporcionada. **R: haoqunkong.com**

---
[^1]: "Documentos Ofimáticos Maliciosos" en [Sokratica](https://sokratica.github.io/sokratica/an%C3%A1lisis%20de%20malware/2022/12/03/officeMal.html).
[^2]: [Remnux VM](https://remnux.org/).
[^3]: [Evento Document_open](https://learn.microsoft.com/en-us/office/vba/api/word.document.open), [Método OpenDoc](https://learn.microsoft.com/en-us/office/vba/api/Word.Documents.Open) y [qué es BVA](https://es.wikipedia.org/wiki/Visual_Basic_for_Applications)
[^4]: [¿Qué es un Emotet?](https://latam.kaspersky.com/resource-center/threats/emotet)