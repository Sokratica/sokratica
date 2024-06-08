---
layout: post
comments: false
title : Writeup | CyberDefenders | Jailbroken
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, Jailbroken, Endpoint Forensics
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto Jailbroken de la plataforma Cyberdefenders.org"
image: x.png
---

Esta es una guía de cómo resolver, paso a paso, el reto Jailbroken de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, Ramnit, Endpoint Forensics


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
    2.8 [Pregunta 7](#p8)\\
    2.9 [Pregunta 7](#p9)\\
    2.10 [Pregunta 7](#p10)\\
    2.11 [Pregunta 7](#p11)\\
    2.12 [Pregunta 7](#p12)\\
    2.13 [Pregunta 7](#p13)\\
    2.14 [Pregunta 7](#p14)\\
    2.15 [Pregunta 7](#p15)\\
    2.16 [Pregunta 7](#p16)\\
    2.17 [Pregunta 7](#p17)\\
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
|Reto|Jailbroken|
|SHA1SUM|67b2d3bb549e32727b126232b8c862a3e7816bd0|
|Autor|Champlain College|
|Tags|Disk Forensics, iOS, iPad, iLEAPP, SQLite Browser, Mac, Autopsy, Jailbroke, T1555|

Este laboratorion me hace especial ilusión hacer. Principalmente porque, en nuestros días, los teléfonos celulares y otros dispositivos móviles como tablets (iPads) contienen muchísima información sobre nosotros los usuarios. En casos criminales de cualquier naturaleza, estos dispositivos son una pieza de evidencia probatoria de vital importancia. Por esta razón, y por motivos de gustos personales, me emociona hacer ejecicios sobre dispositivos móviles. El ejercicio en sí, está planteado como tal, no tiene un contexto ficticio de crimen o lo que sea... ya lo verás en la descripción del escenario.


# Escenario

Jailbroken es un caso de investigación de un iPad que expone diferentes aspectos de sistemas iOS donde podrás evaluar tus habilidades forenses y de investigador de sistemas operativos que casos de investigación típicos como miembro de un Blue Team.


## Herramientas

**Recomendadas**
- iLEAPP
- Autopsy
- mac_apt
- SQLiteDB Browser


## Mitre ATT&CK <a name="mitre"></a>

Como ya es habitual en este blogv-y no deja de ser una buena práctica-, siempre que nos dan un código de la matriz de Mitre ATT&CK nos vamos a ir de file a investigar qué nos dice la web al respecto.

[T1555](https://attack.mitre.org/techniques/T1555/)


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Writeup <a name="wu"></a>

**1. What is the IOS version of this device?** <a name="p1"></a>
**2. Who is using the iPad? Include their first and last name. (Two words)** <a name="p2"></a>
**3. When was the last time this device was 100% charged? Format: 01/01/2000 01:01:01 PM** <a name="p3"></a>
**4. What is the title of the webpage that was viewed the most? (Three words)** <a name="p4"></a>
**5. What is the title of the first podcast that was downloaded?** <a name="p5"></a>
**6. What is the name of the WiFi network this device connected to? (Two words)** <a name="p6"></a>
**7. What is the name of the skin/color scheme used for the game emulator? This should be a filename.** <a name="p7"></a>
**8. How long did the News App run in the background?** <a name="p8"></a>
**9. What was the first app download from AppStore? (Two words)** <a name="p9"></a>
**10. What app was used to jailbreak this device?** <a name="p10"></a>
**11. How many applications were installed from the app store?** <a name="p11"></a>
**12. How many save states were made for the emulator game that was most recently obtained?** <a name="p12"></a>
**13. What language is the user trying to learn?** <a name="p13"></a>
**14. The user was reading a book in real life but used their IPad to record the page that they had left off on. What number was it?** <a name="p14"></a>
**15. If you found me, what should I buy?** <a name="p15"></a>
**16. There was an SMS app on this device's dock. Provide the name in bundle format: com.provider.appname** <a name="p16"></a>
**17. A reminder was made to get something, what was it?** <a name="p17"></a>



++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Preguntas y respuestas <a name="pyr"></a>


