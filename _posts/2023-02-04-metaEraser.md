---
layout: post
comments: false
title : Herramientas | metaEraser | Borrador de metadatos
categories: [Herramientas]
tags: Herramientas, Tools, Borrador de metadatos, python, Exiftool
excerpt: "Esta herramienta sirve para borrar los metadatos de ficheros con capacidad de escritura como pdfs."
image: flujo.png
---

# Índice

1. [Limitaciones](#limitaciones)
2. [¿Qué es lo que pasa por detrás?](#what)
3. [Requisitos](#req)
4. [Código fuente](#script)\\
    4.1 [Linux](#lin)\\
    4.2 [Windows](#wind)


<html>
<body>
<style>
table, th, td {
  border:1px solid black;
}
</style>
</body>
</html>

# Limitaciones <a name="limitaciones"></a>

En la idea original, esta herramienta estaba pensada para poder eliminar los metadatos de los ficheros de uso más comunes, es decir: docx, xlsx y pdf. Sin embargo, debido a la herramienta **Exiftool** sobre la cual la presente se basa, no tiene soporte para poder escribir en archivos tipo docx ni xlsx. En la web oficial de Phil Harvey ---el genio detrás de Exiftool---, podemos leer lo siguiente respecto de las capacidades de la herramienta:[^1]

> ExifTool can **R**ead, **W**rite and/or **C**reate files in the following formats. Also listed are the support levels for EXIF, IPTC (IIM), XMP, ICC_Profile and other metadata types for each file format.

|File Type|Support|Description|
|---------|-------|-----------|
|DOCX, DOCM|**R**|Office Open XML Document (macro-enabled)|
|PDF|**R/W\***|Adobe Portable Document Format|
|XLSX, XLS, XSLB|**R**|Office Open XML Spreadsheet (macro-enabled/binary)|

\* Philly nos advierte, respecto de las capacidades de escritura para los pdfs, "los metadatos viejos nunca de hecho se eliminan". Valdría la pena investigar más a fondo cómo se "eliminan" los metadatos, pero no será en esta ocasión.

Al margen de lo anterior, aun se pueden "borrar" los metadatos de archivos pdf, que tampoco nos viene nada mal.


# ¿Qué es lo que pasa por detrás? <a name="what"></a>

![metaE](https://github.com/Sokratica/sokratica/blob/master/assets/img/metaE/flujo.png?raw=true)

Y te estarás preguntando, ¿y en qué momento me metes la reverse-shell? Pues, no; nada de eso. El script es sencillo y, además, puedes ver el código ya sea para comprobar que no haya cosas turbias, o para que lo modifiques a tu gusto para que haga más cosas.

El flujo del programa es sencillo:
1. Es un comando que se ejecuta desde consola invocando el script de python (metaE) más un parámetro que es el nombre del fichero.
2. Se usa el Exiftool, se filtra el output por los valores más relevantes.
3. Se pide al usuario que confirme el borrado de los metadatos.
4. Se crea un fichero nuevo y permanece el antiguo.


# Requisitos <a name="req"></a>

+ Simplemente, tener la herramienta Exiftool instalada en tu equipo (ve la nota al pie 1 donde está el link a la web oficial de la herramienta).
+ Por supuesto, tener instalado python para que puedas ejecutar el programa.


# Ejemplo

**Linux**

comando

```
python3 metaE.py test.pdf
```

![metaE](https://github.com/Sokratica/sokratica/blob/master/assets/img/metaE/linex.png?raw=true)


**Windows**

Comando:
```
py metaE.py test.pdf
```

![metaE](https://github.com/Sokratica/sokratica/blob/master/assets/img/metaE/winex.png?raw=true)


# Código <a name="script"></a>

Aquí te dejo el código para que lo revises y luego lo copies y pegues donde quieras.

## Para Linux <a name="lin"></a>

Script de python para Linux. Link al script en bruto [metaE](https://github.com/Sokratica/sokratica/tree/master/assets/img/metaE/scripts/Linux)

```
import argparse, os, time

from pwn import *

parser = argparse.ArgumentParser(description='Borrador de metadados para varias extensiones.')

parser.add_argument('name', action='store', type=str, help='Nombre del fichero.')

args = parser.parse_args()

def extractor():
	p1 = log.progress('Extrayendo los metadatos')
	p1.status('Iniciando')
	
	time.sleep(2)

	print(f'Tu archivo tiene la siguiente información:\n')

	au = os.system("exiftool " + args.name + " | grep -i author")
	print(au)
	cr = os.system("exiftool " + args.name + " | grep -i creator")
	print(cr)
	pr = os.system("exiftool " + args.name + " | grep -i producer")
	print(pr)
	cd = os.system("exiftool " + args.name + " | grep -i 'create date'")
	print(cd)
	md = os.system("exiftool " + args.name + "| grep -i 'modify date'")
	print(md)
	
	p1.success("Listo")

	q1 = input("¿Deseas borrar todos los metadatos de tu archivo? [S/n]\n" "Introduce 'e' para salir.\n")

	if q1 == ("s") or q1 == ("S"):
		os.system("exiftool -all= " + args.name)
		print("No toda la información se puede borrar. La que permanece en tu archivo es la siguiente:\n")
		os.system("exiftool " + args.name)
	elif q1 == ("n") or q1 == ("N"):
		print("No sé lo que quieres entonces.\nEmpecemos de nuevo.")
		extractor()
	elif q1 == ("d") or q1 == ("D"):
		print("Opción paranoica.")
	elif q1 == ("e") or q1 == ("E"):
		return 0
	else:
		print("Opción inválida. Te daré una oportunidad más.\n")
		extractor()
	
	print("\nAhora tienes dos archivos, el original '{}_original' y el nuevo '{}'.".format(args.name, args.name))

	return 0


def main():
	extractor()


if __name__ == '__main__':
	main()
```
## Para Windows <a name="wind"></a>

Script de python para Windows. Link al script raw [metaE](https://github.com/Sokratica/sokratica/tree/master/assets/img/metaE/scripts/Windows)

```
import argparse, os, time
from pwn import *

parser = argparse.ArgumentParser(description='Borrador de metadados para varias extensiones.')
parser.add_argument('name', action='store', type=str, help='Nombre del fichero.')

args = parser.parse_args()

def extractor():
	p1 = log.progress('Extrayendo los metadatos')
	p1.status('Iniciando')
	time.sleep(2)

	print(f'Tu archivo tiene la siguiente información:\n')

	au = os.system("exiftool " + args.name + " | findstr /i author")
	print(au)
	cr = os.system("exiftool " + args.name + " | findstr /i creator")
	print(cr)
	pr = os.system("exiftool " + args.name + " | findstr /i producer")
	print(pr)
	cd = os.system("exiftool " + args.name + " | findstr /i create ")
	print(cd)
	md = os.system("exiftool " + args.name + "| findstr /i modify")
	print(md)
	p1.success("Listo")

	q1 = input("¿Deseas borrar todos los metadatos de tu archivo? [S/n]\n" "Introduce 'e' para salir.\n")

	if q1 == ("s") or q1 == ("S"):
		os.system("exiftool -all= " + args.name)
		print("No toda la información se puede borrar. La que permanece en tu archivo es la siguiente:\n")
		os.system("exiftool " + args.name)
	elif q1 == ("n") or q1 == ("N"):
		print("No sé lo que quieres entonces.\nEmpecemos de nuevo.")
		extractor()
	elif q1 == ("d") or q1 == ("D"):
		print("Opción paranoica.")
	elif q1 == ("e") or q1 == ("E"):
		return 0
	else:
		print("Opción inválida. Te daré una oportunidad más.\n")
		extractor()

	print("\nAhora tienes dos archivos, el original '{}_original' y el nuevo '{}'.".format(args.name, args.name))

	return 0


def main():
	extractor()


if __name__ == '__main__':
	main()
```

---
[^1]: Te dejo el link a la página web oficial del Exiftool para que le puedas echar un ojo al manual de usuario como para descargarla: [Exiftool](https://exiftool.org/).
