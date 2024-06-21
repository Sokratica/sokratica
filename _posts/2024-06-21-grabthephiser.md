---
layout: post
comments: false
title : Writeup | CyberDefenders | GrabThePhisher
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, GrabThePhiser
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto GrabThePhiser de la plataforma Cyberdefenders.org"
image: grabthephisher_portada.png
---

Esta es una guía de cómo resolver, paso a paso, el reto GrabThePhiser de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, GrabThePhiser


# Índice

1. [Preámbulo](#pre)\\
  1.1 [Mitre ATT&CK](#mitre)
2. [Writeup](#wu)\\
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
    2.12 [Pregunta 12](#p12)
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
|:--:|:---------:|
|Reto|GrabThePhiser|
|SHA1SUM|a10658aa9561317b1f700331cec85f9a70ba1bf4|
|Autor|Milann Shrestha|
|Tags|Phishing, OSINT, T1567, T1016, T1566.003|

# Escenario

Un atacante comprometió un servidor e hizo suplantación de identidad de https[:]//pancakeswap[.]finance/, un intercambio descentralizado nativo de BNB Chain, para alojar un kit de phishing en https[:]//apankewk[.]soup.xyz/mainpage[.]php. El atacante lo configuró como un directorio abierto con el nombre de archivo "pankewk.zip".

Dado el kit de phishing, se te solicita como analista de SOC que lo analices y realices tu investigación de inteligencia de amenazas.

## Mitre ATT&CK <a name="mitre"></a>

[T1567](https://attack.mitre.org/techniques/T1567/)

**Exfiltración a través de Servicio Web**

Los adversarios pueden utilizar un servicio web externo legítimo existente para exfiltrar datos en lugar de utilizar su canal de comando y control principal. Servicios web populares que actúan como mecanismo de exfiltración pueden ofrecer una cantidad significativa de cobertura debido a la alta probabilidad de que los equipos dentro de una red ya estén comunicándose con ellos antes de la compromisión. Es posible que también existan reglas de firewall para permitir el tráfico hacia estos servicios.

Los proveedores de servicios web suelen utilizar encriptación SSL/TLS, proporcionando a los adversarios un nivel adicional de protección.

[T1016](https://attack.mitre.org/techniques/T1016/)

**Descubrimiento de Configuración de Red del Sistema**

Los adversarios pueden buscar detalles sobre la configuración y ajustes de red, como direcciones IP y/o MAC, de sistemas a los que acceden o mediante el descubrimiento de información de sistemas remotos. Existen varias utilidades de administración de sistemas operativos que pueden ser utilizadas para recopilar esta información. Ejemplos incluyen Arp, ipconfig/ifconfig, nbtstat y route.

Los adversarios también pueden aprovechar una Interfaz de Línea de Comandos (CLI) de Dispositivos de Red para obtener información sobre configuraciones y ajustes, como direcciones IP de interfaces configuradas y rutas estáticas/dinámicas (por ejemplo, show ip route, show ip interface).

Los adversarios pueden utilizar la información obtenida del Descubrimiento de Configuración de Red del Sistema durante el descubrimiento automatizado para determinar ciertos accesos dentro de la red objetivo y qué acciones realizar a continuación.

[T1566.003](https://attack.mitre.org/techniques/T1566/003/)

**Phishing: Spearphishing a través de Servicios**

Los adversarios pueden enviar mensajes de spearphishing a través de servicios de terceros en un intento de obtener acceso a sistemas de víctimas. El spearphishing a través de servicios es una variante específica de spearphishing. Se diferencia de otras formas de spearphishing en que utiliza servicios de terceros en lugar de canales de correo electrónico empresariales directos.

Todas las formas de spearphishing son ingeniería social entregada electrónicamente dirigida a un individuo, empresa o industria específica. En este escenario, los adversarios envían mensajes a través de varios servicios de redes sociales, correo web personal y otros servicios no controlados por la empresa. Estos servicios tienen políticas de seguridad generalmente menos estrictas que una empresa. Como con la mayoría de los tipos de spearphishing, el objetivo es generar una relación de confianza con la víctima o captar su interés de alguna manera. Los adversarios crearán cuentas falsas en redes sociales y enviarán mensajes a empleados ofreciendo posibles oportunidades laborales. Esto les permite tener una razón plausible para preguntar sobre servicios, políticas y software que se ejecutan en un entorno. El adversario puede luego enviar enlaces maliciosos o archivos adjuntos a través de estos servicios.

Un ejemplo común es establecer una relación de confianza con un objetivo a través de las redes sociales, y luego enviar contenido a un servicio de correo web personal que la víctima utiliza en su computadora de trabajo. Esto permite al adversario eludir algunas restricciones de correo electrónico en la cuenta de trabajo, y es más probable que la víctima abra el archivo porque es algo que esperaba. Si la carga útil no funciona como se esperaba, el adversario puede continuar con comunicaciones normales y ayudar a la víctima a solucionar cómo hacer que funcione.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Writeup <a name="wu"></a>

**1. ¿Qué billetera se usa para solicitar la frase semilla?** <a name="p1"></a>

Si abrimos el fichero “index[.]html” veremos 3 opciones para conectar una wallet de criptomonedas. Por otra parte, en los directorios de la muestra del kit the phishing, hay una carpeta que se llama como una de las wallets

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/1.png?raw=true)

**2. ¿Cuál es el nombre del archivo que contiene el código del kit de phishing?** <a name="p2"></a>

Si ingresamos en la carpeta de “metamask”, veremos otro fichero “index[.]html” y un “metamask[.]php”. En este último es donde encontraremos el código para loggearse en la supuesta web:

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/2.png?raw=true)


**3. ¿En qué lenguaje fue escrito el kit?** <a name="p3"></a>

Esta respuesta ya la tenemos en el lenguaje del fichero “metamask” de la pregunta a anterior.


**4. ¿Qué servicio utiliza el kit para recuperar la información de la máquina de la víctima?** <a name="p4"></a>

Dentro de este fichero, que podemos leer dese un editor de código o desde un navegador, vemos una llamada “request” para obtener ficheros a través de una API llamada “sypex geo”:

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/3.png?raw=true)


**5. ¿Cuántas frases semilla se han recopilado hasta ahora?** <a name="p5"></a>

La respuesta es 3 y están almacenadas en el fichero “log/log.txt”. Esto lo podemos descubrir si leemos el flujo del programa malicioso_

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/4.png?raw=true)


**6. Escribe la frase semilla del incidente de phishing más reciente.** <a name="p6"></a>

Revisando el código, en la parte final de éste hay una función de “append”, el cual agregar texto hasta el final de un fichero. 

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/5.png?raw=true)

Con esto en mente, lo natural sería que la última línea sea la frase semilla más reciente robada:

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/6.png?raw=true)


**7. ¿Qué medio se ha utilizado para el volcado de credenciales?** <a name="p7"></a>

Como se puede ver en el código, el mensaje con la frase semilla se envía a través de Telegram.


**8. ¿Cuál es el token del canal?** <a name="p8"></a>

Allí mismo podemos ver el token del canal que nos pide la pregunta:

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/7.png?raw=true)


**9. ¿Cuál es el ID de chat del canal del pescador?** <a name="p9"></a>

La respuesta la puedes encontrar en la sección de “$id” en la imagen anterior.


**10. ¿Quiénes son los aliados del desarrollador del kit de phishing?** <a name="p10"></a>

En el fichero de “metamask[.]php”, vemos que el cibercriminal deja un mensaje a la víctima firmado por alguien que se hace llamar:

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/8.png?raw=true)


**11. ¿Cuál es el nombre completo del actor de phishing?** <a name="p11"></a>

De acuerdo con lo que pude ver en internet, podemos obtener información del chat y el administrador del mismo a través de una request en un navegador con la siguiente estructura:

```
https:/api.telegram.org/botTOKEN/getChat?chat_id=ID

donde:
TOKEN=5457463144:AAG8t4k7e2ew3tTi0IBShcWbSia0Irvxm10
ID=5442785564
```

Así, obtenemos lo siguiente:

![grabthephisher](https://github.com/Sokratica/sokratica/blob/master/assets/img/grabthephishser/9.png?raw=true)


**12. ¿Cuál es el nombre de usuario del actor de phishing?**  <a name="p12"></a>

Allí mismo, podemos obtener el nombre de usuario de Telegram.


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Preguntas y respuestas <a name="pyr"></a>
1. ¿Qué billetera se usa para solicitar la frase semilla?\\
**metamask**

2. ¿Cuál es el nombre del archivo que contiene el código del kit de phishing?\\
**metamask.php**

3. ¿En qué lenguaje fue escrito el kit?\\
**php**

4. ¿Qué servicio utiliza el kit para recuperar la información de la máquina de la víctima?\\
**sypex geo**

5. ¿Cuántas frases semilla se han recopilado hasta ahora?\\
**3**

6. Escribe la frase semilla del incidente de phishing más reciente.\\
**father also recycle embody balance concert mechanic believe owner pair muffin hockey**

7. ¿Qué medio se ha utilizado para el volcado de credenciales?\\
**Telegram**

8. ¿Cuál es el token del canal?\\
**5457463144:AAG8t4k7e2ew3tTi0IBShcWbSia0Irvxm10**

9. ¿Cuál es el ID de chat del canal del "pescador"?\\
**5442785564**

10. ¿Quiénes son los aliados del desarrollador del kit de phishing?\\
**j1j1b1s@m3r0**

11. ¿Cuál es el nombre completo del actor de phishing?\\
**Marcus Aurelius**

12. ¿Cuál es el nombre de usuario del actor de phishing?\\
**pumpkinboii**