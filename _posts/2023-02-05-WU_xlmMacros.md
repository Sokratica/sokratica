---
layout: post
comments: false
title : Writeup | CyberDefenders | xlm-macros 4.0
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, xlm-macros 4.0, Análisis de Malware
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto xml-macros 4.0 de la plataforma Cyberdefenders.org"
image: cd_xmlmacros.png
---

Esta es una guía de cómo resolver, paso a paso, el reto xlm-macros 4.0 de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, xlm-macros 4.0, Análisis de Malware, Análisis de Documentos Maliciosos.

## Escenario

Recientemente, hemos visto un resurgimiento de documentos de oficina maliciosos basados en Excel. Sin embargo, en lugar de utilizar macros de estilo VBA, están utilizando macros de Excel 4 de estilo antiguo. Esto cambia nuestro enfoque para analizar estos documentos, requiriendo un conjunto ligeramente diferente de herramientas. En este desafío, se pondrá manos a la obra con dos documentos que utilizan macros de Excel 4.0 para realizar el antianálisis y descargar la siguiente fase del ataque.


# Índice

1. [Preámbulo](#pre)
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
    3.14 [Pregunta 14](#p14)
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
|Reto|XLM Macros|
|SHA1SUM|35fb4497de1633d6887fd1453ee1426ca627eeec|
|Autor|Josh Stroschein|
|Tags|Macro, Oledump, XLM, XLS, Excel 4 Macros, Remnux, Anti-analysis, Office Ide|

## Herramientas

**Recomendadas**
- REMnux VM
- XLMDeobfuscator
- OLEDUMP with PLUGIN_BIFF
- Office IDE

**Usadas**
- MV Remnux
- Exiftool
- msoffcrypto-crack


# Introducción <a name="intro"></a> 

Otro reto de nuestro Josh Stroschein de confianza.

Empecemos creando nuestros directorios de trabajo: samples y evidence.

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img1.png?raw=true)

Inmediatamente después, hay que verificar que estamos trabajando con los ficheros correctos comparando los md5 y el shasum:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img2.png?raw=true)

¡Hasta ahora, todo en orden! Empecemos.


# Writeup <a name="wu"></a>


La pregunta 1 del reto nos dice que el sample1 está encriptado, así que podemos correr el **Exiftool** para echarle un ojo a la info que nos arroje:

```
exiftool sample1-fb5ed444ddc37d748639f624397cff2a.bin
```

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img3.png?raw=true)

- Efectivamente, Exiftool nos dice que el binario está protegido con contraseña.

## Primera Parte

**1. Muestra1: ¿Cuál es la contraseña de descifrado del documento?** <a name="p1"></a>

Con esto en mente, podemos usar una de las herramientas que vienen instaladas por defecto con la máquina virtual Remnux, a saber, la **msoffcrypto-crack**:

```
msoffcrypto-crack.py sample1-fb5ed444ddc37d748639f624397cff2a.bin
```

Lo que nos arroja al toque por pantalla esta herramienta, cuando al corremos sobre la muestra, es la contraseña:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img5.png?raw=true)


**2. Muestra1: Este documento contiene seis hojas ocultas. ¿Cómo se llaman? Proporcione el valor de la que empieza por S.** <a name="p2"></a>

Cuando usamos el Exiftool sobre la muestra 1, en la sección de "Title of Parts", la herramienta mostró por pantalla el nombre de algunas de las secciones que vienen en el binario. Podemos ver que hay algunos recursos que tiene como nombre "Sheet", es decir, algo así como "hoja" haciendo alusión a las hojas de cálculo de Excel. Por pura inferencia (y por la extensión de la respuesta), podemos asumir que la respuesta a esta pregunta es: **SOCWNEScLLxkLhtJp**

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img4.png?raw=true)


**3. Muestra1: ¿Qué URL utiliza el malware para descargar la siguiente etapa? Incluya sólo el dominio de segundo y primer nivel. Por ejemplo, xyz.com.** <a name="p3"></a>

Con lo que tenemos hasta aquí, podemos empezar a usar nuestras herramientas de oletools. Si corremos el oledump sobre nuestra muestra, veremos lo siguiente:

```
oledump.py sample1-fb5ed444ddc37d748639f624397cff2a.bin
```
![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img6.png?raw=true)

- Lo cual no nos dice mucho.

Lo que podemos hacer en segundo momento es correr el olevba:

```
olevba sample1-fb5ed444ddc37d748639f624397cff2a.bin
```

La herramienta nos va a arrojar un montón de información, pero la que nos interesa es la que está en el cuadro resumen del final:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img7.png?raw=true)

- Entre otra información interesante, como el ejecutable que se descarga, el olevba nos arroja como indicador de compromiso (IoC) identificado una URL desde donde se descarga el recurso en cuestión, allí está nuestra repuesta.


**4. Muestra1: ¿Qué familia de malware intentaba descargar este documento?** <a name="p4"></a>

Tuve que buscar por internet el tipo de familia usando el hash, el nombre del sample y algunas de las TTC que se encontraron en el análisis. La respuesta, directamente, es:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img8.png?raw=true)

**NOTA: Me hace falta encontrar una metodología más robusta para detectar las familias de los malwares. Por favor, si tienes aportes, contáctame para probar metodologías.**


## Segunda Parte

**5. Muestra2: Este documento tiene una hoja muy oculta. ¿Cuál es el nombre de esta hoja?** <a name="p5"></a>

Lo primero que hice para esta parte fue la misma metodología: oletools. El oledump no arroja mucha información, pero el olevba muestra la siguiente información relacionada con una hoja de cálculo con una macro:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img9.png?raw=true)

- Allí está nuestra respuesta.


**6. Muestra2: Este documento utiliza reg.exe. Qué clave del registro está comprobando?** <a name="p6"></a>

Continué con el olevba para esta pregunta. Si nos fijamos en lo que hay en la hoja de cálculo que anteriormente ya habíamos identificado (la de la pregunta 2), veremos un montón de celdas con valores, algunos son caracteres y otras contienen fórmulas. Hasta el final de todo lo que revela el olevba vemos una cadena de caracteres que arroja la macro:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img10.png?raw=true)


**7. Muestra2: A partir del uso de reg.exe, ¿qué valor de la clave evaluada indica un entorno sandbox?** <a name="p7"></a>

La información que se imprime por pantalla tras la ejecución del olevba en la sección de "EMULATION - DEOBFUSCATED EXCEL4/XLM MACRO FORMULAS" nos proporciona muy buena información para las siguientes preguntas.

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img11.png?raw=true)

- Después de usar el reg en una de las celdas, hace una búsqueda de la cadena "0001" en la celda "J731".

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img12.png?raw=true)

- Asumo que el valor en texto de "0001" se puede interpretar simplemente como "1", por lo que en hexadecimal sería **0x1**.


**8. Muestra2: Este documento realiza varias comprobaciones adicionales antianálisis. Qué función de macro de Excel 4 utiliza?** <a name="p8"></a>

Si la fórmula anterior arroja un "FALSE", te manda a la celda "J1". Desde allí se empiezan a hacer varias comprobaciones:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img13.png?raw=true)


**9. Muestra2: Este documento comprueba el nombre del entorno en el que se ejecuta Excel. ¿Qué valor utiliza para comparar?** <a name="p9"></a>

En la celda "J6" se hace una búsqueda de una cadena de caracteres en el resultado de "get.workspace(1)":

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img14.png?raw=true)


10. **Muestra2: ¿Qué tipo de payload se descarga?** <a name="p10"></a>

En las siguientes líneas de la emulación vemos lo siguiente:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img15.png?raw=true)

- No nos dice qué se descarga, pero sí vemos una llamada a al proceso "rundll32" por lo que asumí que se descarga un **DLL**.
- Por otra parte, vemos bajo qué nombre se descarga el recurso el cuál luego se va a ejecutar: es lo que vemos en la celda "J9".
- Asimismo, podemos ver el link desde donde se descarga el payload.


**11. Muestra2: ¿De qué URL descarga el malware el payload?** <a name="p11"></a>

Como ya vimos en la imagen anterior, el payload se descarga desde **httpx://ethelenecrace[.]xyz/fbb3**.

**12. Sample2: ¿Cuál es el nombre de archivo con el que se guarda el payload?** <a name="p12"></a>

Al igual que con la pregunta anterior, en la celda "J7" nos dice bajo qué nombre se descarga el payload: **bmjn5ef[.]html**.

**13. Muestra2: ¿Cómo se ejecuta el payload? Por ejemplo, mshta.exe** <a name="p13"></a>

Como ya dijimos, vimos que se hace una llamada para abrir un proceso desde donde se corra el payload: **rundll32[.]exe**

**14. Sample2: ¿Cuál era la familia del malware?** <a name="p14"></a>

Si metemos el dm5 en virustotal, podemos ver que hay algunos análisis que muestran qué tipo de malware es:

![xlmmacros](https://github.com/Sokratica/sokratica/blob/master/assets/img/xlmmacros/img16.png?raw=true)


# Preguntas y respuestas <a name="pyr"></a>

1. Muestra1: ¿Cuál es la contraseña de descifrado del documento?\\
**R: VelvetSweatshop**

2. Muestra1: Este documento contiene seis hojas ocultas. ¿Cómo se llaman? Proporcione el valor de la que empieza por S.\\
**R: SOCWNEScLLxkLhtJp**

3. Muestra1: ¿Qué URL utiliza el malware para descargar la siguiente etapa? Incluya sólo el dominio de segundo y primer nivel. Por ejemplo, xyz.com.\\
**R: httx://rilaer[.]com**

4. Muestra1: ¿Qué familia de malware intentaba descargar este documento?\\
**R: Dridex**

5. Muestra2: Este documento tiene una hoja muy oculta. ¿Cuál es el nombre de esta hoja?\\
**R: CSHykdYHvi**

6. Muestra2: Este documento utiliza reg.exe. Qué clave del registro está comprobando?\\
**R: VBAWarnings**

7. Muestra2: A partir del uso de reg.exe, ¿qué valor de la clave evaluada indica un entorno sandbox?\\
**R:0x1**

8. Muestra2: Este documento realiza varias comprobaciones adicionales antianálisis. Qué función de macro de Excel 4 utiliza?\\
**R: get.workspace**

9. Muestra2: Este documento comprueba el nombre del entorno en el que se ejecuta Excel. ¿Qué valor utiliza para comparar?\\
**R: Windows**

10. Muestra2: ¿Qué tipo de payload se descarga?\\
**R: DLL**

11. Muestra2: ¿De qué URL descarga el malware la carga útil?\\
**R: httpx://ethelenecrace[.]xyz/fbb3**

12. Sample2: ¿Cuál es el nombre de archivo con el que se guarda la carga útil?\\
**R: bmjn5ef[.]html**

13. Muestra2: ¿Cómo se ejecuta la carga útil? Por ejemplo, mshta.exe\\
**R: rundll32[.]exe**

14. Sample2: ¿Cuál era la familia del malware?\\
**R: zloader**
