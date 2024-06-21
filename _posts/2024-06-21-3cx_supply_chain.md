---
layout: post
comments: false
title : Writeup | CyberDefenders | 3CX Sypply Chain
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, 3CX Sypply Chain
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto 3CX Sypply Chain de la plataforma Cyberdefenders.org"
image: 3cx_supply_chain_portada.png
---

Esta es una guía de cómo resolver, paso a paso, el reto 3CX Sypply Chain de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, 3CX Sypply Chain


# Índice

1. [Preámbulo](#pre)
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
|Reto|3CX Sypply Chain|
|SHA1SUM|2F7F7B5B15F99AB35DF099F1F4140E387C28103F|
|Autor|CyberDefenders|
|Tags|Malware Analysis, APTs, Virustotal|

|Herramientas recomendadas|
|:-----------------------:|
|VirusTotal|

# Escenario

Una gran corporación multinacional depende en gran medida del software 3CX para la comunicación telefónica, lo que lo convierte en un componente crítico de sus operaciones comerciales. Después de una actualización reciente de la aplicación de escritorio 3CX, las alertas del antivirus señalan instancias esporádicas de que el software es eliminado de algunas estaciones de trabajo, mientras que otras permanecen sin afectar. Al descartar esto como un falso positivo, el equipo de TI pasa por alto las alertas, solo para notar un rendimiento degradado y tráfico de red extraño hacia servidores desconocidos. Los empleados informan problemas con la aplicación 3CX, y el equipo de seguridad de TI identifica patrones de comunicación inusuales vinculados a las actualizaciones recientes del software.

Como analista de inteligencia de amenazas, es tu responsabilidad examinar este posible ataque a la cadena de suministro. Tus objetivos son descubrir cómo los atacantes comprometieron la aplicación 3CX, identificar al posible actor de la amenaza involucrado y evaluar la magnitud general del incidente.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Writeup <a name="wu"></a>

Próximamente (cuando el reto sea "retirado").

**1. Entender el alcance del ataque e identificar qué versiones presentan comportamiento malicioso es crucial para tomar decisiones informadas si estas versiones comprometidas están presentes en la organización. ¿Cuántas versiones de 3CX que se ejecutan en Windows han sido señaladas como malware?** <a name="p1"></a>
**2. Determinar la antigüedad del malware puede ayudar a evaluar la magnitud del compromiso y a rastrear la evolución de las familias y variantes de malware. ¿Cuál es la hora de creación UTC del malware en el archivo .msi?** <a name="p2"></a>
**3. Los archivos ejecutables (.exe) se utilizan frecuentemente como cargas útiles primarias o secundarias de malware, mientras que las bibliotecas de enlace dinámico (.dll) a menudo cargan código malicioso o mejoran la funcionalidad del malware. Analizar los archivos depositados por el Microsoft Software Installer (.msi) es crucial para identificar archivos maliciosos e investigar su potencial completo. ¿Cuáles DLL maliciosas fueron depositadas por el archivo .msi?** <a name="p3"></a>
**4. Reconocer las técnicas de persistencia utilizadas en este incidente es esencial para las estrategias de mitigación actuales y las mejoras de defensa futuras. ¿Cuál es el ID de la sub-técnica de MITRE empleada por los archivos .msi para cargar la DLL maliciosa?**  <a name="p4"></a>
**5. Reconocer el tipo de malware (categoría de amenaza) es esencial para tu investigación, ya que puede ofrecer información valiosa sobre las posibles acciones maliciosas que estarás examinando. ¿Cuál es la familia de malware de las dos DLL maliciosas?** <a name="p5"></a>
**6. Como analista de inteligencia de amenazas que realiza análisis dinámico, es vital comprender cómo el malware puede evadir la detección en entornos virtualizados o sistemas de análisis. Este conocimiento te ayudará a mitigar o abordar eficazmente estas tácticas evasivas. ¿Cuál es el ID de MITRE para las técnicas de evasión de virtualización/sandbox utilizadas por las dos DLL maliciosas?** <a name="p6"></a>
**7. Al realizar análisis de malware e ingeniería inversa, comprender las técnicas de anti-análisis es vital para evitar perder tiempo. ¿Qué hipervisor es objetivo de las técnicas de anti-análisis en el archivo ffmpeg.dll?** <a name="p7"></a>
**8. Identificar el método criptográfico utilizado en el malware es crucial para comprender las técnicas empleadas para eludir los mecanismos de defensa y ejecutar sus funciones completamente. ¿Qué algoritmo de cifrado es utilizado por el archivo ffmpeg.dll?** <a name="p8"></a>
**9. Como analista, has reconocido algunas TTPs involucradas en el incidente, pero identificar el grupo APT responsable te ayudará a buscar sus TTPs habituales y descubrir otras posibles actividades maliciosas. ¿Qué grupo es responsable de este ataque?** <a name="p9"></a>




++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Preguntas y respuestas <a name="pyr"></a>

1. Entender el alcance del ataque e identificar qué versiones presentan comportamiento malicioso es crucial para tomar decisiones informadas si estas versiones comprometidas están presentes en la organización. ¿Cuántas versiones de 3CX que se ejecutan en Windows han sido señaladas como malware?
2. Determinar la antigüedad del malware puede ayudar a evaluar la magnitud del compromiso y a rastrear la evolución de las familias y variantes de malware. ¿Cuál es la hora de creación UTC del malware en el archivo .msi?
3. Los archivos ejecutables (.exe) se utilizan frecuentemente como cargas útiles primarias o secundarias de malware, mientras que las bibliotecas de enlace dinámico (.dll) a menudo cargan código malicioso o mejoran la funcionalidad del malware. Analizar los archivos depositados por el Microsoft Software Installer (.msi) es crucial para identificar archivos maliciosos e investigar su potencial completo. ¿Cuáles DLL maliciosas fueron depositadas por el archivo .msi?
4. Reconocer las técnicas de persistencia utilizadas en este incidente es esencial para las estrategias de mitigación actuales y las mejoras de defensa futuras. ¿Cuál es el ID de la sub-técnica de MITRE empleada por los archivos .msi para cargar la DLL maliciosa?
5. Reconocer el tipo de malware (categoría de amenaza) es esencial para tu investigación, ya que puede ofrecer información valiosa sobre las posibles acciones maliciosas que estarás examinando. ¿Cuál es la familia de malware de las dos DLL maliciosas?
6. Como analista de inteligencia de amenazas que realiza análisis dinámico, es vital comprender cómo el malware puede evadir la detección en entornos virtualizados o sistemas de análisis. Este conocimiento te ayudará a mitigar o abordar eficazmente estas tácticas evasivas. ¿Cuál es el ID de MITRE para las técnicas de evasión de virtualización/sandbox utilizadas por las dos DLL maliciosas?
7. Al realizar análisis de malware e ingeniería inversa, comprender las técnicas de anti-análisis es vital para evitar perder tiempo. ¿Qué hipervisor es objetivo de las técnicas de anti-análisis en el archivo ffmpeg.dll?
8. Identificar el método criptográfico utilizado en el malware es crucial para comprender las técnicas empleadas para eludir los mecanismos de defensa y ejecutar sus funciones completamente. ¿Qué algoritmo de cifrado es utilizado por el archivo ffmpeg.dll?
9. Como analista, has reconocido algunas TTPs involucradas en el incidente, pero identificar el grupo APT responsable te ayudará a buscar sus TTPs habituales y descubrir otras posibles actividades maliciosas. ¿Qué grupo es responsable de este ataque?