---
layout: post
comments: false
title : Análisis de Malware | Dropper
categories: [Análisis de Malware]
tags: Análisis de Malware, TCM Security Academy, Análisis Estático, Análisis Dinámico, Dropper 2 fases
excerpt: "Malware Dropper: Este es el primer análisis de la sección de análisis estático avanzado de un dropper usando el programa Cutter para verificar el disassembly y el decompiler."
---

# TCM Security Academy
# Practical Malware Analysis & Triage
# Ejercicio 1: Advanced Static Analysis 

---

# Índice

1. [Análisis estático](#estbas)
2. [Comportamiento](#compor)
3. [Análsis estático avanzado](#estavan)
4. [Conclusiones](#conclusiones)

---

**Herramientas**

Análisis estático básico:
- FLOSS
- PEStudio
- PEView
- Capa

Análisis estático avanzado:
- Cutter

---

# Análisis Estático Básico <a name="estbas"></a>

## Floss

Al correr el floss sobre la muestra del malware se pueden identificar algunas strings interesantes:

<html>
<body>
<style>
table, th, td {
  border:1px solid black;
}
</style>
</body>
</html>

|No.|String|
|---|------|
|1|SHELL32.dll|
|2|URLDownloadToFileW|
|3|InternetOpenUrlW|

Asimismo, el floss reveló mmás información relavante sobre la ejecución del binario:

![malware dropper1](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img1.png?raw=true)


- 1. Abre una consola y lanza una traza para verificar la conexión a internet. La flag "/C" indica que es un proceso que se abre desde consola, ejecuta la string como comando y luego termina. La parte del comando __Nul & Del /f /q "%s"__ indica que una parte del proceso fuerza el borrado de fichero en modo silencioso se lo que sea que haya sido introducido como string.
- 2. hay una petición http a una dirección en concreto pidiendo un recurso "favicon.ico".
- 3. Se está creando un fichero con nombre "CR433101.dat.exe" en la ruta especificada.
- 4. Se lanza otra traza y se busca al fichero descargado.
- 5. Se ejecuta el programa.


## PEStudio

|Campo|Valor|
|-----|-----|
|md5|1D8562C0ADCAEE734D63F7BAACA02F7C|
|sha256|92730427321A1C4CCFC0D0580834DAEF98121EFA9BB8963DA332BFD6CF1FDA8A|
|Primeros bytes|M Z... executable|
|Arquitectura|32-bits|
|Fecha de compilación|Sat Sep 04 2021|

![malware dropper 2](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img2.png?raw=true)

## peview

Comparación de tamaño

|Raw size|Virtual size|
|--------|------------|
|1600 -> 5.632|15A1 -> 5.537|

**No hay una diferencia significativa, por lo que probablemente se trate de un archivo que no esté comprimido.**

### IAT

Se encontraron las siguientes imports:

- ShellExecute
- EnternetEpenE
- InternetOpenURLW
- URLDownloadToFileW

Esta última es un indicativo de que sea crea un fichero con el recurso que se descarga desde una url.

# Capa

El módulo de capa reitera la información anteriormente encontrada: hay comunicación con una url, descarga un fichero y quizá con el proceso que se abre crea un fichero nuevo.

![malware dropper 3](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img3.png?raw=true)

## ATT&CK

**Id: [T1129] Shared Modules**
"Los adversarios pueden ejecutar cargas útiles maliciosas a través de la carga de módulos compartidos. El cargador de módulos de Windows puede ser instruido para cargar DLLs desde rutas locales arbitrarias y rutas de red arbitrarias de la Convención de Nombres Universales (UNC). Esta funcionalidad reside en NTDLL.dll y es parte de la API nativa de Windows que se llama desde funciones como CreateProcess, LoadLibrary, etc. de la API Win32"


# Comportamiento <a name="compor"></a>

## Detonación sin salida a internet

Al ejecutarse el binario y no tener conexión a internet, el ejecutable se borra de la memoria del disco.

## Detonación con salida a internet

### Procmon

Al encontrar conexión a internet, se ejecuta una consola:

![malware dropper 4](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img4.png?raw=true)

El árbol de procesos confirma que la consola se abre como un proceso hijo de la detonación del malware:

![malware dropper 5](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img5.png?raw=true)

Se encontró el fichero creado con el recurso descargado de internet de la petición desde consola en la ruta previamente identificada:

![malware dropper 6](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img6.png?raw=true)

Una comprobación extra afirma que el archivo se crea tras la ejecución del malware. Así, tras haber infectado la máquina, en una segunda instancia el malware instala otro binario.

### Wireshark

El wireshark encontró peticiones a través del protocolo http:

- Una de ellas se realizó por el método GET a la url anteriormente encontrada por el recurso "favicon.ico": 

![malware dropper 7](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img7.png?raw=true)


# Análisis estático avanzado <a name="estavan"></a>

## Cutter

La información del resumen confirma lo que ya teníamos:

![malware dropper 8](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img8.png?raw=true)

#### Disassembly y Decompiler

El primer gran bloque de la función principal del binario muestra cómo se almacena en memoria como string la petición http y el archivo "dat.exe", hay una llamada a esa información y hay una petición de descraga vía URL.

![malware dropper 10](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img10.png?raw=true)

Después hay una comparación de valores que determina el flujo del programa: si el valor almacenado en el espacio en memoria no es igual a algo, se ejecuta un bloque; si es igual, se ejecuta otro bloque. Si los valores cargados en la memoria eax encajan, se ejecuta el programa, de lo contrario el binario se borra del disco.

![malware dropper 9](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img9.png?raw=true)

El flujo dle programa es como sigue:

![malware dropper 11](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img11.png?raw=true)


# Conclusiones <a name="conclusiones"></a>

El malware se pueda catalogar como un "dropper" que se ejecuta en dos instancias o fases: 

>"Un dropper es un tipo de troyano que ha sido diseñado para instalar algún tipo de malware (virus, puertas traseras, etc.) en un sistema objetivo. El código del malware puede estar contenido dentro del dropper (de una sola etapa) de tal manera que se evite su detección por parte de los escáneres de virus o el dropper puede descargar el malware a la máquina objetivo una vez activado (dos etapas). El código del dropper extrae los componentes restantes (uno o más archivos) del archivo si están almacenados dentro de él, o los carga de la red, los escribe en el disco y los ejecuta. Normalmente un (o más) componente es un troyano, y al menos un componente es un "engaño": un programa de chistes, un juego, una imagen o algo así. El "engaño" debe distraer la atención del usuario y/o demostrar que el archivo que se está ejecutando realmente hace algo "útil", mientras que el componente troyano está instalado en el sistema.
Un dropper que instala malware sólo en la memoria a veces se llama inyector.3​El código del malware se incluye en el inyector o se descarga a la máquina desde Internet una vez activado. Una vez que el malware se activa, el inyector puede autodestruirse. Los inyectores son poco comunes."[^1]

En la primera etapa verifica si tiene acceso a internet y lanza una petición http a un recurso de la web (el "favicon.ico") y los resultados los almacena en memoria. Luego hace una verificación de este espacio: si está vacío, el binario se borra de la memoria del disco; si no está vacío, se ejecuta el programa descargado y almacenado en memoria de disco.

![malware dropper 12](https://github.com/Sokratica/sokratica/blob/master/assets/img/malandrop/img12.png?raw=true)


[^1]: https://es.wikipedia.org/wiki/Dropper_(malware)
