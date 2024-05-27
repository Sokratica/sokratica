---
layout: post
comments: false
title : Writeup | CyberDefenders | Obfuscated
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, Obfuscated, Análisis de Malware
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto Obfuscated de la plataforma Cyberdefenders.org"
image: cd_obfuscated.png
---

Esta es una guía de cómo resolver, paso a paso, el reto Obfuscated de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, Obfuscated, Análisis de Malware, Maldocs, Análisis de Documentos Maliciosos.

## Escenario

Durante tu turno como analista del SOC, el EDR (Endpoint Detection and Response) de la empresa alertó de un comportamiento sospechoso de un equipo de usuario final. El usuario indicó que había recibido un correo electrónico reciente con un archivo DOC de un remitente desconocido y te pasó el documento para que lo analices.

# Índice

1. [Prámbulo](#pre)
2. [Introducción](#intro)
3. [Writeup](#wu)\\
    3.1 [Pregunta 1](#p1)\\
    3.2 [Pregunta 2](#p2)\\
    3.3 [Pregunta 3](#p3)\\
    3.4 [Pregunta 4](#p4)\\
    3.5 [Pregunta 5](#p5)\\
    3.6 [Pregunta 6](#p6)\\
    3.7 [Pregunta 7](#p7)\\
    3.8 [Pregunta 8](#p8)\\
    3.9 [Pregunta 9](#p9)\\
    3.10 [Pregunta 10](#p10)\\
    3.11 [Pregunta 11](#p11)\\
    3.12 [Pregunta 12](#p12)\\
    3.13 [Pregunta 13](#p13)\\
    3.14 [Pregunta 14](#p14)\\
    3.15 [Pregunta 15](#p15)\\
    3.16 [Pregunta 16](#p16)\\
    3.17 [Pregunta 17](#p17)\\
    3.18 [Pregunta 18](#p18)
4. [Preguntas y respuestas](#pyr)


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
|Reto|Obfuscaated|
|SHA1SUM|29c20b7eeac34715cbfe27dc4dbfe5451e89293|
|Autor|Josh Stroschein|
|Tags|Javascript, Malicious Document, Backdoor, CmdWatcher|


## Herramientas

**Recomendadas**
- CmdWatcher
- oledump
- sha256sum

**Usadas**
- VM Flare
- VM Remnux
- Hybrid Analysis
- oledump
- sha256sum


# Introducción <a name="intro"></a>

Otro retito de análisis de malware, esta vez se trata de un docx con un javascipt embebido.

En las herramientas recomendadas se sugiere usar el CmdWatcher. Esta herramienta reporta por pantalla los logs del cmd, supongo que esto sirve para conocer la ruta en la que se almacena el js en memoria para, después, analizar el código. Cuando estaba en esa parte del reto me di cuenta de que mi Flare no tiene el Word, así que no pude abir el documento malicioso.

Le di la vuelta a este problema usando la web de Hybrid Analysis y desde allí extraje el js. ¡Mucha suerte!

Si tienes dudas, ya sabes que me puedes contactar en mi Twitter.

---

# Writeup <a name="wu"></a>

Ya saben que, como metodología, creamos una serie de directorios donde iremos depositando nuestras muestras y evidencias. Yo operaré desde el Escritorio y crearé los directorios: obfuscated (nombre del reto), sample, evidencia.

Un paso muy importante antes de continuar es asegurarse de que las MV que estemos usando (Flare y Remnux) no tengan salida a internet:

- Hay que estar seguros de que en la configuración de Red de la MV esté en el modo "Adaptador sólo-anfitrión" y de que los otros adaptadores estén inhabilitados:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img1.png?raw=true)

- Por otra parte, podemos corroborar esta configuración pingeando a la ip de Google y, por si las dudas, desde el navegador que tengamos instalado, intentar acceder a cualquier web:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img2.png?raw=true)

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img3.png?raw=true)


**1. ¿Cuál es el hash sha256 del archivo doc?** <a name="p1"></a>

Una vez listos, lo primero hay que hacer extraer el hash del documento que extrajimos del zip:

```
 sha256sum.exe ..\sample\49b367ac261a722a7c2bbbc328c32545 > sha256.txt
```

Nuestra primera respuesta ya está en el txt que creamos:

```
ff2c8cadaa0fd8da6138cce6fce37e001f53a5d9ceccd67945b15ae273f4d751
```

- Dado que se trata de un documento malicioso, nuestras herramientas clásicas de análisis (pestudio, peview, capa) podrían no arrojar información valioso. A lo mucho, podemos constatar algo de información que ya teníamos si corremos la muestra en el PEStudio:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img4.png?raw=true)


**2. Varias secuencias contienen macros en este documento. Proporcione el número de la más baja.** <a name="p2"></a>

Así, pues, procedemos a usar la herramientas oletools a partir de aquí.

Inicialmente, correremos el oledump sobre la muestra:

```
 oledump.py ..\sample\49b367ac261a722a7c2bbbc328c32545 > oledump.txt
```

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img5.png?raw=true)

- Desde aquí ya podemos ver que hay una macro potencialmente maliciosa embebida en el documento. Ésta está señalada con la "M" en el objeto con índice **8**.


**3. ¿Cuál es la clave de descifrado del código ofuscado?** <a name="p3"></a>

Como podemos ver, la macro está insertada en un VBA, por lo que podemos usar la herramienta olevba para echar un vistazo a lo que hay dentro:

```
olevba.exe ..\sample\49b367ac261a722a7c2bbbc328c32545 > olevba.txt
```

- Entre otras cosas, podemos confirmar que hay un script en el objeto 8, llamado "Module1", del documento:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img6.png?raw=true)

Otra información relevante podemos encontrar:

- Hay un indicador de compromiso que señala un ejecutable escrito en "js", jscript, que es un lenguaje común para código hecho en wscript[^1]. Esta es la respuesta a la pregunta 5.

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img7.png?raw=true)

Asumiendo que el código se ejecutará dentro de una PowerShell, lo que hice fue buscar si había alguna string que indicara una llamada a la powershell:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img8.png?raw=true)

Con esto, podemos hacer un cat a nuestra evidencia y ver qué es lo que hay en la línea 80. Varias son las cosas interesantes alrededor de esta línea:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img9.png?raw=true)

- En primer lugar, podemos ver como se crea un fichero con el nombre "K764..." (línea 74). Después, asigna a una variable una ruta que termina en un js (esta es la respuesta a la pregunta 4). Después de algunos pasos, abre y corre una shell desde donde mete como argumentos la variable donde se encuentra el js, más una clave de descifrado: EzZETcSXyKAdF_e5I2i1.


**4. ¿Cuál es el nombre del archivo descartado?** <a name="p4"></a>

Ver pregunta 3: "maintools.js"


**5. ¿Qué lenguaje utiliza este script?** <a name="p5"></a>

Ver pregunta 3: jscript.


**6. Cómo se llama la variable a la que se asignan los argumentos de la línea de comandos?** <a name="p6"></a>

Para parsear el js embebido en el documento malicioso, subí el documento a la web Hybrid Analysis[^2] y desde allí pude obtener el código:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img10.png?raw=true)

- En la imagen de arriba podemos ver que la variable a la cual se le asignan los argumentos fue nombrada: "wvy1".


**7. ¿Cuántos argumentos de línea de comandos espera este script?** <a name="p7"></a>

En la variable "ssWZ" que se le asigna como valor la variable con los argumentos vemos que nuestra variable de interés está esperando como argumento el indexado como 0, por lo que está esperando un sólo argumento.


**8. ¿Qué instrucción se ejecuta si este script encuentra un error?** <a name="p8"></a>

En los códigos javascript, cuando se escribe un try;catch, primero se ejecuta el bloque de código que está dentro de try, si ocurre una excepción, el catch se ejecuta. En nuestro código podemos ver que la función que se ejecuta si ocurre un error en el bloque del try es: "WScript.Quit()"


**9. ¿Qué función devuelve la siguiente etapa de código (es decir, la primera ronda de código ofuscado)?** <a name="p9"></a>

Asumiendo que no ocurre ningún error, la siguiente función que se ejecutaría sería la que se asigna a la variable "ES3c", es decir, la función "y3zb()".


**10. La función LXv5 es una función importante, ¿a qué variable se le asigna un valor de cadena clave para determinar lo que hace esta función?** <a name="p10"></a>

Como se puede ver en la imagen, la variable "LUK7" es a la que se le asigna todo el rango de caracteres del abecedario, tanto en minúsculas como mayúsculas, más los números naturales y el caracteres especiales "/" y "+":

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img11.png?raw=true)


**11. ¿Qué esquema de codificación es responsable de decodificar esta función?** <a name="p11"></a>

Los caracetes asignados a la variable de la pregunta anterior son típicos del Base64. Por otra parte, en los resultados del análisis con el olevba ya se sugería que había cadenas de caracteres codificadas en base64.


**12. En la función CpPT, ¿los dos primeros bucles for son responsables de qué parte importante de esta función?** <a name="p12"></a>

Los bucles "for" son los encargados de realizar operaciones algebraicas sobre los argumentos metidos en la función.

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img12.png?raw=true)

- A esta técnica se le llama "Key-Scheduling".


**13. La función CpPT requiere dos argumentos, ¿de dónde procede el valor del primer argumento?** <a name="p13"></a>

Regresando al principio del código, vemos que la función "CpPT" tiene dos argumentos, el primero es el "ssWZ" al cual se le ha asignado el valor de la función "wvy1" que, a su vez, tiene como argumento lo que sea que entre como input desde la consola:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img13.png?raw=true)

Así que, el valor del argumento viene de la "command-line".


**14. En la función CpPT, ¿qué representa el primer argumento?** <a name="p14"></a>

Por lo que hemos estado revisando hasta ahora, el primer argumento hace referencia a la llave de desencriptado.


**15. ¿Qué algoritmo de cifrado implementa la función CpPT en este script?** <a name="p15"></a>

Por el algoritmo "key-scheduling" usado, más las características del código encontrado, al método que se usa en el malware es el algoritmo RC4[^3].


**16. ¿Qué función es responsable de ejecutar el código desofuscado?** <a name="p16"></a>

A la variable "ES3c" se le asigna lo que regresa la función "CpPT" que ya vimos. Después, esta variable funge como argumento de la función "eval".


**17. ¿Qué programa Windows Script Host puede utilizarse para ejecutar este script en modo de línea de comandos?** <a name="p17"></a>

No sabía la respuesta de esta pregunta así que lo que hice fue googlear, literalmente, cuáles eran los programas más comunes para el "windows script host" y me salió como resultado "cscript.exe"[^4].


**18. ¿Cuál es el nombre de la primera función definida en el código desofuscado?** <a name="p18"></a>

Finalmente, lo que nos queda es meter el input del código de la función "y3zb" al Cyberchef:

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img14.png?raw=true)

La recetas son:
- From Base64
- RC4
	- Sabemos que la clave de desencriptado es la de la pregunta 3.

![obfuscated1](https://github.com/Sokratica/sokratica/blob/master/assets/img/obfuscated/img15.png?raw=true)

---

# Preguntas y respuestas <a name="pyr"></a>

1. ¿Cuál es el hash sha256 del archivo doc?\\
**R: ff2c8cadaa0fd8da6138cce6fce37e001f53a5d9ceccd67945b15ae273f4d751**

2. Varias secuencias contienen macros en este documento. Proporcione el número de la más baja.\\
**R: 8**

3. ¿Cuál es la clave de descifrado del código ofuscado?\\
**R: EzZETcSXyKAdF_e5I2i1**

4. ¿Cuál es el nombre del archivo descartado?\\
**R: maintools.js**

5. ¿Qué lenguaje utiliza este script?\\
**R: jscript**

6. Cómo se llama la variable a la que se asignan los argumentos de la línea de comandos?\\
**R: wvy1**

7. ¿Cuántos argumentos de línea de comandos espera este script?\\
**R: 1**

8. ¿Qué instrucción se ejecuta si este script encuentra un error?\\
**R: WScript.Quit()**

9. ¿Qué función devuelve la siguiente etapa de código (es decir, la primera ronda de código ofuscado)?\\
**R:y3zb**

10. La función LXv5 es una función importante, ¿a qué variable se le asigna un valor de cadena clave para determinar lo que hace esta función?\\
**R: LUK7**

11. ¿Qué esquema de codificación es responsable de decodificar esta función?\\
**R: Base64**

12. En la función CpPT, ¿los dos primeros bucles for son responsables de qué parte importante de esta función?\\
**R: Key-Scheduling Algorithm**

13. La función CpPT requiere dos argumentos, ¿de dónde procede el valor del primer argumento?\\
**R: command-line argument**

14. En la función CpPT, ¿qué representa el primer argumento?\\
**R: key**

15. ¿Qué algoritmo de cifrado implementa la función CpPT en este script?\\
**R: RC4**

16. ¿Qué función es responsable de ejecutar el código desofuscado?\\
**R: eval**

17. ¿Qué programa Windows Script Host puede utilizarse para ejecutar este script en modo de línea de comandos?\\
**R: cscript.exe**

18. ¿Cuál es el nombre de la primera función definida en el código desofuscado?\\
**R: UspD**

---

[^1]: Más sobre [ECMAScript](https://262.ecma-international.org/12.0/#sec-intro).
[^2]: Link a la web de [Hybrid Analysis](https://www.hybrid-analysis.com/).
[^3]: Aquí podrás ver cómo todas las características del encriptado que hemos hallado en el script encajan con el [RC4](https://en.wikipedia.org/wiki/RC4).
[^4]: cscript para javasecripting en [Windows](https://technoresult.com/enable-windows-script-host-access-in-windows-10/).
