---
layout: post
comments: false
title : Análisis de Malware | Documentos Ofimáticos Maliciosos (Maldocs)
categories: [Análisis de Malware]
tags: Análisis de Malware, TCM Security Academy, Análisis Estático, Documentos Ofimáticos, Excel
excerpt: "Excel y Word maliciosos: este es un ejemplo de un par de documentos ofimáticos maliciosos, excel y word, sobre los cuales se hace un análsis estático con la herramienta oledump."
---

# TCM Security Academy
# Practical Malware Analysis & Triage
# Documentos Ofimáticos Maliciosos

---

# Índice

1. [Maldocs: Excel](#excel)
    1. [Contenido del xlsm](#xlsm)
    2. [Contenido del .bin](#bin)
2. [Maldocs: Word](#word)
3. [Conclusiones](#conclusiones)

---

**Herramientas**

Análisis estático:
- oledump.py

---

# Maldoc: Excel <a name="excel"></a>

## Análisis estático

### Contenido del xlsm <a name="xlsm"></a>

Imagínate la siguiente situación: eres la persona a cargo de la facturación de tu empresa y recibes un correo de un supuesto cliente en el que te manda un archivo excel adjunto en el cual, según te escribe, están los montos correspondientes a las compras del mes. Descargas el archivo, das doble click para abrirlo y desactivas las medidas de seguridad del Office para que puedas manipular el documento. En ese momento, estás permitiendo que las macros embebidas en el documento hagan su trabajo.

Y es que en los documentos de Office hay más de lo que podemos ver a simple vista. Primero (y es lo que veremos en este ejemplo), la extensión de un archivo Office, cuando tiene una macro dentro, viene con una "m" en la extensión: en este caso el nombre del archivo es "sheetsForFinancial.xlsm".

De manera general, un simple archivo Office contiene un montón de otros archivos o ficheros. Es decir, podemos pensar un archivo de estos como una carpeta donde tiene dentro otros ficheros.

Si descomprimimos el excel del ejemplo podremos ver que dentro tiene lo siguiente:

![offMal1](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img1.png?raw=true)



De primeras, para el analista de malware podría saltarle a la vista que dentro hay un fichero ".bin", el cual indica que hay un binario embebido en el excel.

## Contenido del .bin <a name="bin"></a>

Analizando el contenido de este fichero, con la herramienta oledump[^1], se puede ver que ésta detectó la presencia de una macro[^2] la cual, siendo paranoico, el analista podría pensar que es una macro maliciosa:

![offMal2](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img2.png?raw=true)

Para determinar el riesgo de esa macro, mostramos su contenido. Normalmente, lo que encontraremos son un montón de strings contenidas dentro del ".bin". A simple vista, algunas podrían llamarnos la atención, aunque esto podría varias dependiendo de qué tan ofuscada o no podría estar la macro. En este ejemplo se pueden ver algunas cosas interesantes:

![offMal3](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img3.png?raw=true)

![offMal4](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img4.png?raw=true)

Intentemos recuperar la sintaxis de la macro para ver si podemos visualizar con más claridad lo que esta macro puede hacer:

![offMal5](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img5.png?raw=true)

Parece ser que la macro embebida dentro del documento xlsm analizado tiene la capacidad de hacer lo siguiente:

1. Crea una subrutina en la que crea un objeto "Adodb.Stream".
2. Luego hace una petición http por el método GET por el recurso "abc123.crt" a "http://srv3.wonderballfinancial.local/abc123.crt".
3. El cual es guardado como "encd.crt".
4. Después, mediante el emulador de comandos y la utilidad certutil, decodifica el fichero recién guardado y el contenido lo mete a un fichero que nombre "run.ps1" el cual lee desde una PowerShell en modo oculto.

# Maldocs: Word <a name="word"></a>

## Análisis Estático

Algunos podrán pensar que con verificar que en la extensión no esté especificado que haya una macro (la "m" en la extensión) sería sufciente para poder abrir un documento ofimático de manera segura. Sin embargo, no es el caso; en esta sección trataremos de mostrar que podría haber un gran riesgo al abrir un documento Word sin macros.

### Documento .docm

Al igual que con el ejemplo del excel, en la extensión del documento aparece la señal de la "m". Inspeccionando el documento con el oledump vemos lo mismo (esto es una prueba de concepto).

![offMal6](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img6.png?raw=true)

Con este ejemplo era obvio que habría una macro maliciosa. Pero lo que queremos probar es que, incluso sin tener la "m" en la extensión podría haber algo malicioso corriendo por detrás.

### Documento .docx

El archivo docx que analizaremos es el llamado "incrediblyPolishedResume.docx". El truco es el mismo, podemos tratar el archivo como un directorio para ver el contenido del documento.

![offMal7](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img7.png?raw=true)

Descomprimiendo el fichero "test.zip", podemos ver los siguiente:

![offMal8](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img8.png?raw=true)

El fichero en la ruta "word/_rels/settings.xml.rels" es el que nos interesa. En este fichero se establece la configuración del template del documento Word que estás usando. Lo que hace el programa Word es descargar un template y lo almacena en el sistema de ficheros en algún lugar del host. Usualmente es en el directorio llamado "custom word templates".

Dentro del fichero de configuración hay una variable "target" donde el programa almacena dicho template. Sin embargo, en esta variable se puede meter una url desde donde se descargue cualquier cosa a la que apunte:

![offMal9](https://github.com/Sokratica/sokratica/blob/master/assets/img/offMal/img9.png?raw=true)

En este caso, la url apunta al recurso "macro3.dotm" el cual es un "document template file" y si este fichero que se descarga tiene una macro embedida, cuando abras tu archivo word se descargará, almacenará y ejecutará.

En estricto sentido, un "docx" no tiene una macro embedida, pero no significa que no sea un riesgo abrir el documento sin medidas de seguridad.

# Conclusiones <a name="conclusiones"></a>

Al margen de lo que este archivo xlsm pueda hacer, la macro embebida implica un riesgo si se abre de manera descuidada.
Por otra parte, por la descripción del análisis realizado, podría parecer que solamente con tener en cuenta si la extensión del documento ofimático que querramos abrir contiene la letra "m" en su nombre, lo cual sería un indicativo de que contiene una macro, sería suficiente para descartar cualquier riesgo. Sin embargo, algunos documentos ofimáticos que no tienen explícitamente este indicativo también podrían o contener macros o script potencialmente maliciosos.

---
[^1]: OLE significa "Object Linking & Embedding" el cual es un protocolo desarrollado por Microsoft. Este protocolo, básicamente, permite que las aplicaciones de los diferentes docuementos Office tengan una interacción enriquecida como arrastrar tablas de excel a un documento word. Para saber más: https://es.wikipedia.org/wiki/Object_Linking_and_Embedding
[^2]: oledump es un programa hecho en python que permite analizar documentos OLE desde la cual se puede ver la información de estos documentos. Dentro de sus funcionalidades, detecta cuando en el documento analizado hay macros: un indicativo de esto es cuando a la derecha del índice "A3" hay una letra m mayúscula "M". Para saber más ver: https://blog.didierstevens.com/programs/oledump-py/


