---
layout: post
comments: false
title : Análisis de Malware | SillyPutty
categories: [Analisis de Malware]
tags: Análisis de Malware, TCM Security Academy, Reto 1, Análisis Estático, Análisis Dinámico, Reverse Shell
excerpt: "Malware: SillyPutty. Este es el primer reto, a nivel básico, propuesto en el curso de __Malware Analysis & Triage__ (Análisis de malware y protocolos de intervención)."
---

# TCM Security Academy
# Practical Malware Analysis & Triage
# Reto 1: Malware SillyPutty

---

# Índice

1. [El reto](#reto)
2. [Análisis estático](#estatico)
3. [Análisis dinámico](#dinamico)
4. [¿Qué es una reverse shell](#reverse)

---

**Objetivo**

Llevar a cabo un análisis estático y uno dinámico de la muestra de malware y extraer información observacional sobre el comportamiento del malware.

---

**Herramientas**

Análisis estático básico:
- Hashes de ficheros
- VirusTotal
- FLOSS
- PEStudio
- PEView

Análisis dinámico básico:
- Wireshark
- Inetsim
- Netcat
- TCPView
- Procmon

---

## Preguntas del reto: <a name="reto"></a>

**Análisis básico estático**

- ¿Cuál es el SHA256 de la muestra?
- ¿Qué arquitectura es el binario?
- ¿Hay algunos resultados al contrastar el SHA256 en VirusTotal?
- Describe los resultados de extraer las __strings__ del binario. Registra y describe cualquier string que sea potencialmente interesante. ¿Se puede extraer alguna información interesante de esas strings?
- Describe los resultados de inspeccionar los __IAT__ (Import Address Table) de este binario. ¿Hay algunos imports valiosos para nuestro propósito?
- ¿Es probable que este binario esté compactado (__packed__)?
---
**Basic Dynamic Analysis**
- Describe la detonación inicial. ¿Se dan sucesos interesantes en esta detonación?
- Desde la perspectiva de los indicadores locales (__host-based indicators__), ¿cuál es al principal __payload__ que es iniciado tras la detonación? ¿Qué herramienta se puede usar para indentificarlo?
- ¿Cuáles son los registros DNS (__Domain Name System__) que son consultados tras la detonación?
- ¿Cuál es el puerto de respuesta tras la detonación?
- ¿Cuál es el protocolo de respuesta de la detonación?
- ¿Cómo se puede usar la telemetría basada en local para identificar los registros DNS, puertos y protocolos?
- Intenta obtener el binario para iniciar la shell en local, ¿aparece la shell? ¿Qué se necesita para que aparezca?

---
---

# Análisis Estático <a name="estatico"></a>

## Hash sha256

0c82e654c09c8fd9fdf4899718efa37670974c9eec5a8fc18a167f93cea6ee83 *putty.exe.mlz

## Arquitectura
<html>
<body>
<style>
table, th, td {
  border:1px solid black;
}
</style>
</body>
</html>

|1st bytes|Tipo|CPU|Subsistema|Fecha de compilación|
|---------|----|---|----------|--------------------|
|M Z...|executable|32-bit|GUI|Sat Jul 10 09:51:55 2021 UTC|


## VirusTotal

|Nombre|Detecciones|Tamaño|Fecha|
|------|-----------|------|-----|
|PuTTY|59/70|1.47 mb|2022-11-10 06:43:21 UTC11 days ago|

![sillyputty1](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp1.png)
![sillyputty2](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp2.png)

## Strings

### Floss

**Se encontró un comando oneliner haciendo una llamada a la powershell:**

![sillyputtyoneliner](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sponeliner.png)

En una búsqueda en fuentes abiertas se encontró que este comando para la powershell está embebido en un payload de Metasploit usado para invocar una reverse shell, aprovechándose de las vulnerabilidades del SO.

**Texto encontrado**
```
	/#STRINGS
/#SYSTEM
/#TOCIDX
/#TOPICS
/#URLSTR
/#URLTBL
```

Omitiendo la información sobre la invocación de la reverse shell, las strings encontradas no parecen particularmente interesantes, en el contexto de que aún no detonamos el malware. De otra manera, que aparezca una powershell tras la ejecución de un programa (malicioso) podría ser una señal de alarma.

### PEStudio

**Librerías:**

- GDI32.dll
- USER32.dll
- COMDLG32.dll
- SHELL32.dll
- ole32.dll
- IMM32.dll
- ADVAPI32.dll
- KERNEL32.dll

Bajo el mismo contexto, estas librerías no parecen particularmente sospechosas.

## ¿Binario comprimido?

|Descripción|Hex|Decimal|
|-----------|---|-------|
|Virtual Size|95F6D|614.253|
|Raw Data|96000|614.400|

- Es poco probable que estemos frente a un binario empaquetado.

## Descubrimientos relevantes

- Es un .exe identificado en VirusTotal.
- Se encontró un comando en powershell: "powershell.exe -nop -w hidden -noni -ep bypass" -> Este comando se usa para invocar una powershell con la finalidad de ejecutar código.

---
---

# Análisis Dinámico <a name="dinamico"></a>


## Detonación sin salida a internet

- Se abre una powershell.
- Sale una pantalla de conexión para enlazarse a la ip o host que indiques.

![sillyputty3](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp3.png)


### Procmon

- El análisis del procmon revela que, tras la ejecución del putty.exe, aparece una powershell como proceso hijo del malware.
- Asimismo, en la información de la powershell se puede ver el oneliner que es un payload malicioso.

![sillyputty.4](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp4.png)

El onliner indica que está codificando en base64 un comando. El decodificar el código se puede ver lo siguiente:

![sillyputty5](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp5.png)


El método de decodificación se hizo en la máquina remnux mediante la siguiente serie de comandos:

![sillyputtydecode](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/spdecode.png)


### Wireshark

La captura del tráfico encontró que la powershell manda una petición DNS a "bonus2.corporatebonusapplication.local"

![sillyputty6](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp6.png)

al bonus2.corporatebonusapplication.local. Y actualizamos con el comando:

```
ipconfig /flushdns
```

Reiniciamos el wireshark en el canal: Ncap Loopback...
Vemos que recebimos el saludo de vuelta del puerto 8443.

![sillyputty7](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp7.png)

### Ncat

Finalmente, con ncat tratamos de capturar la información transmitida de vuelta por https y vemos que nos regresa información. Aunque no se puede interpretar y no podemos ejecutar comandos, debido a que no hemos podido completar el protocolo https, todo sugiere que se trata de una rever shell.

![sillyputty8](https://github.com/Sokratica/sokratica/blob/master/assets/img/masp/sp8.png)

---
---

## ¿Qué es una reverse shell? <a name="reverse"></a>

Una reverse shell, también conocida como shell remota o "connect-back shell", aprovecha las vulnerabilidades del sistema objetivo para iniciar una sesión de shell y luego acceder al ordenador de la víctima. El objetivo es conectarse a un ordenador remoto y redirigir las conexiones de entrada y salida de la shell del sistema objetivo para que el atacante pueda acceder a él de forma remota.

Las reverse shell permiten a los atacantes abrir puertos a las máquinas objetivo, forzando la comunicación y permitiendo una toma completa de la máquina objetivo. Por lo tanto, es una grave amenaza para la seguridad.

## ¿Cómo funciona una reverse shell?

En un ataque de reverse shell estándar, los atacantes conectan una máquina que controla al host de red remoto del objetivo, solicitando una sesión de shell. Esta táctica se conoce como bind shell. Los atacantes pueden utilizar una reverse shell si un host remoto no es accesible públicamente (por ejemplo, debido a la protección del cortafuegos o a una IP no pública). La máquina objetivo inicia la conexión saliente en un ataque de reverse shell y establece la sesión de shell con el host de red que escucha.

Para los hosts protegidos por una traducción de direcciones de red (NAT), una reverse shell puede ser necesaria para realizar el mantenimiento de forma remota. Aunque existen usos legítimos para las reverse shells, los ciberdelincuentes también las utilizan para penetrar en los hosts protegidos y ejecutar comandos del sistema operativo. Las reverse shells permiten a los atacantes eludir los mecanismos de seguridad de la red, como los cortafuegos.

Los atacantes pueden conseguir capacidades de reverse shell a través de correos electrónicos de phishing o sitios web maliciosos. Si la víctima instala el malware en una estación de trabajo local, inicia una conexión saliente con el servidor de comandos del atacante. La conexión saliente suele tener éxito porque los cortafuegos suelen filtrar el tráfico entrante [^1].

---
[^1]: Fuente: https://www.imperva.com/learn/application-security/reverse-shell/