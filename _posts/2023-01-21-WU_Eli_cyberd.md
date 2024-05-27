---
layout: post
comments: false
title : Writeup | CyberDefenders | Eli
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, Eli, Digital Forensics, Auditoria Digital
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto Eli de la plataforma Cyberdefenders.org"
image: cd_eli.png
---

Esta es una guía de cómo resolver, paso a paso, el reto MalDoc101 de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, MalDoc101, Análisis de Malware, Maldocs, Análisis de Documentos Maliciosos.

## Escenario:
Un entusiasta del lacrosse a la caza de un delicioso sándwich de pollo.

# Índice

1. [Preámbulo](#pre)
    1.1 [Introducción](#intro)
2. [Write Up](#wu)
    2.1 [Pregunta 1](#p1)\\
    2.2 [Pregunta 2](#p2)\\
    2.3 [Pregunta 3](#p3)\\
    2.4 [Pregunta 4](#p4)\\
    2.5 [Pregunta 5](#p5)\\
    2.6 [Pregunta 6](#p6)\\
    2.7 [Pregunta 7](#p7)\\
    2.8 [Pregunta 8](#p8)\\
    2.9 [Pregunta 9](#p9)\\
    2.10 [Pregunta 10](#p10)\\
    2.11 [Pregunta 11](#p11)\\
    2.12 [Pregunta 12](#p12)\\
    2.13 [Pregunta 13](#p13)\\
    2.14 [Pregunta 14](#p14)\\
    2.15 [Pregunta 15](#p15)\\
    2.16 [Pregunta 16](#p16)
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
|Reto|Eli|
|SHA1SUM|b167983c5014b0b8a78b8ba7475910865b20e9cc|
|Autor|Jessica Hyde, Alayna Cash, Hayley Froio, Dylan Navarro, Jordan Kimball y Magnet Forensics|
|Tags|Chromebook, Gmail, Chromeos, Takeout|


## Herramientas

- CLEAPP


# Introducción <a name="intro"></a>

No tenía mucha idea de qué me esperaría en este reto así que, en mi total ignorancia, preparé mi mejor laboratorio para Digital Forensics[^1] con una serie de herramientas para esta rama incrustadas en un Windows Server 2010 y resulta que no usé nada de eso y, por otra parte, lo pude haber hecho de manera más sencilla desde un Linux. Dicho lo anterior, los comandos que usé para el reto son para Windows pero se podrían perfectamente ejecutar desde tu OS Linux.

Pese a que no tiene mucha chicha en cuanto a Forensics duro, el reto está muy bueno para profundizar en lo que se puede obtener de registros de uso de Google Chrome.

Si tienes dudas, ya sabes que me puedes contactar en mi Twitter.

¡Por cierto! Al día en que hice el reto, en la plataforma se salta una pregunta: la 9 no está. Desconozco la razón, pero ten en cuenta que no está contemplada en este writeup.

## Reconocimiento previo

Vistazo de los que viene como evidencia en el CTF.
Cuando descomprimes el zip del reto, se encuentran otros 4 objetos:
- Chromebook.tgz
- Chromebook.tgz:Zone.Identifier
- Takeout.zip:Zone.Identifier
- Takeout.zip
	- Al descomprimir este zip es donde se puede encontrar lo bueno:
	- Calendar
	- Chrome
	- Drive
	- Google Account
	- Google My Business
	- Google Pay
	- Google Play Movies_TV
	- Google Shopping
	- Google Workspace Marketplace
	- Hangouts
	- Home App
	- Mail
	- Maps
	- My Activity
	- New
	- Profile
	- YouTube and YouTube Music
	- archive_browser.html
	- archive_browser.html:Zone.Identifier

![eli1](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img1.png?raw=true)

![eli2](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img2.png?raw=true)

- En los directorios de "Takeout" es donde parece estar la carnita del CFT. Así que procederemos artesanalmente (directorio por directorio) a buscar lo que nos pide el reto.

---

# Writeup <a name="wu"></a>

## **1. La carpeta en la que guardar todos los datos - ¿Cuántos archivos hay en el directorio de descargas de Eli?** <a name="p1"></a>

La información para esta pregunta se encuentra en el comprimido "2021 CTF - Chromebook.tgz". Yo extraje los directorios del zip con la herramienta "7-Zip". Si ya tienes instalada la herramienta, literal sólo hay que darle click derecho -> "Abrir con" y elegimos 7-zip y extraemos el comprimido "2021 CTF - Chromebook.tar" al directorio de trabajo actual.

![Eli3](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img3.png?raw=true)

Lo que hice una vez teniendo el .tar fue extraer la información de dentro desde consola con el siguiente comando:

- Yo almacené los archivos del reto en el escritorio para operar desde allí.
- Adicionalmente, y como buenas prácticas, podemos crear un directorio "Evidencia" hacia donde mandar lo que extraigamos.

```
tar -xvzt "C:\Users\tu_usuario\Desktop\c78-Chromebook\2021 CTF - Chromebook.tar" -C C:\Users\tu_usuario\Desktop\c78-Chromebook\Evidencia
```
![Eli4](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img4.png?raw=true)


- Si todo salió bien con la extracción del tar, esto es más o menos lo que deberías poder ver.

Si estamos familiarizados con el sistema de ficheros de de un usuario normal en un entorno de windows, por ejemplo, lo que estamos buscando es el directorio personal de nuestro usuario (supongo que se trata de Eli) para, así, poder encontrar el directorio de descargas y enumerar lo que nos interesa en esta pregunta.

Si le ya pudiste echarle un ojo a lo que hay dentro de todos los directorios que acabamos de extraer, verás que hay muchísimos subdirectorios y ficheros. Buscar uno a uno para localizar el directorio "Downloads" sería una locura. Lo que yo hice para agilizar el trabajo fue mostrar la estructura de directorios, pero que se me muestren sólo las carpetas de descargas.

El trabajo lo podemos hacer en dos pasos:
(1) Pasar la estructura de árbol de los directorios a un txt sobre el cual vamos a trabajar:

```
tree . > structure.txt
```

- Espero que sea obvio que lo que queremos mostrar por ventana es la info que metimos en nuestra carpeta de Evidencia.

(2) Después, busqué las carpetas de descargas con el siguiente comando:

```
tree - | findstr /N Downloads
```

- La flag "/N" nos va a mostrar la línea donde se encontró el match.

![Eli5](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img5.png?raw=true)


Nuestras carpetas están en las líneas **33, 91, 198, 1135**. Si abrimos nuestro fichero txt podremos deducir la ruta de la carpeta que nos interesa. Ya te digo que la que nos interesa es la de la línea 198.

![Eli6](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img6.png?raw=true)

La ruta es: decrypted/mount/user/Downloads

![Eli7](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img7.png?raw=true)


## **2. Sonríe a la cámara - ¿Cuál es el hash MD5 de la foto de perfil del usuario?** <a name="p2"></a>

Si te dio por curiosear, habrás podido ver que en las imágenes que hay en la carpeta de descargas no hay alguna de perfil. Por otra parte, la pregunta misma nos da pistas sobre dónde buscar la foto de perfil. Podemos usar la misma metodología que antes: tree + findstr. El comando es el siguiente:

```
tree . | findstr Account
```

- Como no está buscando un match exacto, en el output podemos ver un match en la línea 183.

![Eli8](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img8.png?raw=true)


- Lo que podemos ver cuando vamos a nuestro txt es que dentro de ese carpeta hay un subdirectorio llamado "Avatar Images"... bastante  sugerente.

Dentro de esta carpeta hay un fichero llamado "eflatt610Xgmail.com". Lo que hice fue usar una aplicación web para extraer el MD5:

![Eli9](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img9.png?raw=true)


La web que usé fue [conversion-tool](https://www.conversion-tool.com/md5/).

MD5:
```
5ddd4fe0041839deb0a4b0252002127b
```

## **3. ¡Viaje por carretera! - ¿En qué ciudad estaba el destino de Eli?** <a name="p3"></a>

Si recordamos, en la carpeta de descargas de Eli había varias imágenes. Una de ellas, en concreto la llamada "Screenshot 2021-03-04 at 3.17.06 AM.png", es una captura de pantalla de una ruta trazada desde el Maps. En esa captura se puede ver que la ciudad de destino es Plattsburgh:

![Eli10](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img10.png?raw=true)


## **4. Prométemelo - ¿Cuántas promesas hace Wickr?** <a name="p4"></a>

En el mismo directorio podemos ver que hay un archivo pdf que se llama "Wickr-Customer-Security-Promises-November-2020". En el nombre podemos ver la string "Wickr", dentro del pdf veremos nuestra respuesta:

![Eli11](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img11.png?raw=true)


## **5. Key-ty Cat - ¿Cuáles son los cinco últimos caracteres de la clave de la extensión Tabby Cat?** <a name="p5"></a>

Para contestar esta pregunta utilicé una de las herramientas recomendadas por el mismo reto: cleapp.

Una vez instalado e importados los ficheros de nuestra carpeta Evidencia, podemos ver lo siguiente (yo usé el GUI de la herramienta):

![Eli12](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img12.png?raw=true)

En la pregunta se comenta algo de una extensión, por lo que busqué la string "tabby" en el "Chromebook History" y nos arroja dos urls que hacen referencia a la "webstore". Si buscamos la extensión "tabby-cat" incluso podemos constatar que esa extensión de navegador existe.

![Eli13](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img13.png?raw=true)

- En la url se hace referencia al recurso "mefhakmgclhhfbdadeojlkbllmecialg". Si buscamos esta string con nuestro método del tree y luego buscamos en nuestro txt veremos que dentro del directorio "user" hay una carpeta llamada "Extensions".
- Dentro veremos una carpeta llamada "2.0.0_0" y, dentro, un fichero llamado "manifest": allí es donde se encuentra la información que buscamos.
- Desde la consola de Windows podemos correr el siguiente comando para visualizar el contenido:

```
type manifest.json
```
![Eli14](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img14.png?raw=true)

**Ruta al json:** decrypted/mount/user/Extensions/mefhakmgclhhfbdadeojlkbllmecialg/2.0.0_0/


## **6. Hora de improvisar - ¿Cuántas canciones se ha descargado Eli?** <a name="p6"></a>

De manera natural podemos inferir dónde podría estar almacenada la música de un usuario. Los diferentes sistemas operativos tienen una carpeta llamada "Music": allí es donde se encuentra nuestra respuesta.

Sin embargo, debo admitir que me dejé llevar por la pregunta y estuve buscando la respuesta en las carpetas de descargas que podemos encontrar con nuestro método. No obstante, los archivos mp3 se encuentran en la ruta: decrypted/mount/user/MyFiles/Music:

![Eli15](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img15.png?raw=true)


## **7. Autocompletar, desplegar - ¿Qué palabra se autocompletó más?** <a name="p7"></a>

La herramienta cleaap tiene una opción para extraer un reporte del autocompletado. Allí podemos ver lo que buscamos: email.

![Eli16](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img16.png?raw=true)


## **8. Vestirse para el éxito - ¿Cuál es el tamaño lógico de la imagen de este pájaro en bytes?** <a name="p8"></a>

La curiosidad mató al gato, dice el dicho; pero en nuestro caso, ayudó a resolver esta pregunta. Si viste las imágenes que descargó Eli, habrás visto que una de ellas, la llamada "tux", es una imagen del "pájaro" de Linux. Esta es la imagen a la que hace referencia la pregunta:

![Eli17](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img17.png?raw=true)

**Asegúrate que cuando metas la respuesta en la web de cyberdefenders, separes los decimales con una coma (,).**


## **9. Cliente habitual - ¿Cuál fue el sitio web más visitado de Eli?** <a name="p9"></a>

En el cleapp hay un reporte de los sitios web más visitados. Allí encontramos nuestra respuesta: protonmail.com:

![Eli18](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img18.png?raw=true)


## **10. Vroom Vroom, ¿Cómo se llama el tema relacionado con los coches?** <a name="p10"></a>

La pregunta hace referencia a un "tema", supuse que se trataba de algún tema para el navegador que Eli usa. Bajo esta hipótesis, mi razonamiento fue el siguiente: al igual que con la extensión "tabby-cat", quizá el tema elegido para el navegador se almacene en la misma ruta. Así, busqué "theme" en la barra del buscador y me arrojó, entre otros resultados, unas imágenes de nombre "theme_frame" y "theme_ntp_background", que son la misma imagen: un carro rojo.

![Eli19](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img19.png?raw=true)

Una vez ubicada la carpeta donde se encuentran esas imágenes, busqué el "manifest.json" y al leerlo encontré el nombre de "Lamborghini Cherry"; esa es nuestra respuesta.

Bueno, en realidad, en el manifest de puede leer Lam**bro**ghini. No sé si es una error o qué pero nuestra respuesta es Lamborghini.

![Eli20](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img20.png?raw=true)


## **11. Tienes correo - ¿Cuántos correos electrónicos has recibido de notificationXservice.tiktok.com?** <a name="p11"></a>

Para esta pregunta hay que irnos a otro lugar. En la evidencia que nos provee el reto hay un directorio que se llama "Takeout". Dentro hay otro directorio llamado "Mail", allí hay un fichero con extensión mbox. Sabemos el correo que estamos buscando. Lo que podemos hacer en correr el siguiente comando para encontrar lo que buscamos:

```
findstr notification@service.tiktok.com "All mail Including Spam and Trash.mbox" | findstr From
```
![Eli21](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img21.png?raw=true)


## **12. Hambriento de direcciones - ¿A dónde pidió el usuario direcciones en Mar 4, 2021, at 4:15:18 AM EDT** <a name="p12"></a>

Esta es una pregunta difícil de responder. La pregunta misma ya nos da una pista de que Eli pidió transporte hacia alguna dirección. Recordando lo que hemos hecho, volví a la imagen de la ruta que trazó en el Maps y vi que era la misma fecha.

Lo que hice después fue abrir el html de la actividad del navegador en el Firefox y me fui a la opción de "My Activity". En "Exported Files" busqué uno a uno en los html la hora especificada en la pregunta y allí pude ver, dentro de **"Maps"** lo siguiente:

![Eli22](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img22.png?raw=true)


## **13. ¿Quién define lo esencial? - Lo que se buscó el Mar 4, 2021, at 4:09:35 AM EDT** <a name="p13"></a>

Para esta pregunta usamos el mismo método que la pregunta anterior. Ahora vemos lo que hay en la opción de "Search" y se buscamos por la hora, podemos ver que hay una búsqueda que se realizó bajo los criterios que tenemos:

![Eli23](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img23.png?raw=true)

La búsqueda es: "is travelling to get chicken essential travel".


## **14. Tengo tres suscriptores, y contando - ¿A cuántos canales de YouTube está suscrito el usuario?** <a name="p14"></a>

La lógica de esta serie de preguntas nos obliga a buscar en la información rescatada y que podemos ver dese nuestro navegador. Si buscamos, hay una opción de Youtube y, también, un fichero json llamado "subscriptions". A esa es al que hay que apuntar, si visualizamos el contenido vemos que:

![Eli24](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img24.png?raw=true)

- Al principio creí que era un error, pero al tener una cadena vacía, sólo puse **0** como respuesta y listo.


## **15. El tiempo vuela cuando ves YT - ¿En qué fecha se subió el primer vídeo de YouTube que vio el usuario?** <a name="p15"></a>

En la misma sección de Youtube, en el html de "watch-history" se puede ver qué vídeos visualizó el usuario. Para obtener la fecha en que se subió el vídeo a la plataforma lo abrimos y extraemos la fecha:

![Eli25](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img25.png?raw=true)


## **16. ¿Cuánto cuesta? - ¿Cuál es el precio del cinturón?** <a name="p16"></a>

Bajo la misma lógica me puse a buscar en las opciones del navegador hasta que encontré un archivo excel llamado "To-Purchase". Dentro encontrarás una celda que dice "Pebbled Leather Belt" cuyo precio es 98.5

![Eli26](https://github.com/Sokratica/sokratica/blob/master/assets/img/Eli/img26.png?raw=true)

---

# Preguntas y respuestas <a name="pyr"></a>

1. La carpeta en la que guardar todos los datos - ¿Cuántos archivos hay en el directorio de descargas de Eli?
**R: 6**

2. Sonríe a la cámara - ¿Cuál es el hash MD5 de la foto de perfil del usuario?
**R: 5ddd4fe0041839deb0a4b0252002127b**

3. ¡Viaje por carretera! - ¿En qué ciudad estaba el destino de Eli?
**R: Plattsburgh**

4. Prométemelo - ¿Cuántas promesas hace Wickr?
**R: 9**

5. Key-ty Cat - ¿Cuáles son los cinco últimos caracteres de la clave de la extensión Tabby Cat?
**R: DAQAB**

6. Hora de improvisar - ¿Cuántas canciones se ha descargado Eli?
**R: 2**

7. Autocompletar, desplegar - ¿Qué palabra se autocompletó más?
**R: email**

8. Vestirse para el éxito - ¿Cuál es el tamaño lógico de la imagen de este pájaro en bytes?
**R: 46,791**

9. Cliente habitual - ¿Cuál fue el sitio web más visitado de Eli?
**R: protonmail.com**

10. Vroom Vroom, ¿Cómo se llama el tema relacionado con los coches?
**R: Lamborghini Cherry**

11. Tienes correo - ¿Cuántos correos electrónicos has recibido de notificationXservice.tiktok.com?
**R: 6**

12. Hambriento de direcciones - ¿A dónde pidió el usuario direcciones en Mar 4, 2021, at 4:15:18 AM EDT
**R: Chick-fil-A**

13. ¿Quién define lo esencial? - Lo que se buscó el Mar 4, 2021, at 4:09:35 AM EDT
**R: is travelling to get chicken essential travel**

14. Tengo tres suscriptores, y contando - ¿A cuántos canales de YouTube está suscrito el usuario?
**R: 0**

15. El tiempo vuela cuando ves YT - ¿En qué fecha se subió el primer vídeo de YouTube que vio el usuario?
**R: 27/01/2021**

16. ¿Cuánto cuesta? - ¿Cuál es el precio del cinturón?
**R: 98.5**

---
[^1]: El laboratorio que tengo montado en mi PC, para quienes estén interesados, está basado en las recomendaciones de BlueCapSecurity. Te dejo el link al recurso por si quieres montar tu lab: [Laboratorio de BlueCap](https://bluecapesecurity.com/build-your-forensic-workstation/).
