---
layout: post
comments: false
title : Writeup | CyberDefenders | Red Stealer
categories: [Writeups CyberDefenders]
tags: Writeups, Writeups Español, Cyberdefenders, Red Stealer
excerpt: "Este es una guía de cómo resolver, paso a paso, el reto Red Stealer de la plataforma Cyberdefenders.org"
image: red_stealer_portada.png
---

Esta es una guía de cómo resolver, paso a paso, el reto Red Stealer de la plataforma Cyberdefenders.org

Tags: Writeups, Writeups Español, Cyberdefenders, Red Stealer


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
    2.10 [Pregunta 10](#p10)
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
|Reto|Red Stealer|
|SHA1SUM|EC268750BE132D316B2CD71A73E10B00C540834A|
|Autor|Sameer_Fakhoury|
|Tags|Redline, ThreatFox, VirusTotal, MalwareBazzar, Whois|

# Escenario

Formas parte del equipo de Inteligencia de Amenazas en el SOC (Centro de Operaciones de Seguridad). Se ha descubierto un archivo ejecutable en la computadora de un colega, y se sospecha que está vinculado a un servidor de Comando y Control (C2), lo que indica una posible infección de malware.

Tu tarea es investigar este ejecutable analizando su hash. El objetivo es recopilar y analizar datos que sean beneficiosos para otros miembros del SOC, incluyendo el equipo de Respuesta a Incidentes, para responder de manera eficiente a este comportamiento sospechoso.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Writeup <a name="wu"></a>

Próximamente (cuando el reto sea "retirado").

**1. Categorizar malware permite una comprensión más rápida y fácil del malware, ayudando a entender sus comportamientos y vectores de ataque distintivos. ¿Cuál es la categoría identificada de este malware?** <a name="p1"></a>
**2. La identificación clara del nombre del archivo de malware facilita una mejor comunicación entre el equipo SOC. ¿Cuál es el nombre del archivo asociado con este malware?** <a name="p2"></a>
**3. Conocer la hora exacta en que se detectó por primera vez el malware puede ayudar a priorizar acciones. Si el malware se detecta recientemente, puede justificar esfuerzos más urgentes de contención y erradicación en comparación con amenazas antiguas y bien conocidas. ¿Puedes proporcionar la marca de tiempo UTC de la primera presentación de este malware en VirusTotal?**  <a name="p3"></a>
**4. Comprender las técnicas utilizadas por el malware ayuda en la planificación estratégica de seguridad. ¿Cuál es el ID de la técnica MITRE ATT&CK para la recolección de datos del sistema por parte del malware antes de la exfiltración?** <a name="p4"></a>
**5. Después de la ejecución, ¿qué resolución de nombre de dominio realiza el malware?** <a name="p5"></a>
**6. Una vez identificadas las direcciones IP maliciosas, los dispositivos de seguridad de la red, como los firewalls, pueden configurarse para bloquear el tráfico hacia y desde estas direcciones. ¿Puedes proporcionar la dirección IP y el puerto de destino con el que se comunica el malware?** <a name="p6"></a>
**7. Si un servicio de hosting se utiliza frecuentemente para actividades maliciosas, los equipos de seguridad pueden implementar reglas de filtrado estrictas para todo el tráfico hacia y desde las IP pertenecientes a ese proveedor de hosting. ¿A qué servicio de hosting pertenece la IP identificada?** <a name="p7"></a>
**8. Las reglas YARA están diseñadas para identificar patrones y comportamientos específicos de malware. ¿Cuál es el nombre de la regla YARA creada por "Varp0s" que detecta el malware identificado?** <a name="p8"></a>
**9. Entender qué familias de malware están atacando a la organización ayuda en la planificación estratégica de seguridad para el futuro y en la priorización de recursos basados en la amenaza. ¿Puedes proporcionar los diferentes alias de malware asociados con la dirección IP maliciosa?** <a name="p9"></a>
**10. Al identificar las DLL importadas por el malware, podemos configurar herramientas de seguridad para monitorear la carga o el uso inusual de estas DLL específicas. ¿Puedes proporcionar la DLL utilizada por el malware para la escalada de privilegios?** <a name="p10"></a>


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Preguntas y respuestas <a name="pyr"></a>

1. Categorizar malware permite una comprensión más rápida y fácil del malware, ayudando a entender sus comportamientos y vectores de ataque distintivos. ¿Cuál es la categoría identificada de este malware?
2. La identificación clara del nombre del archivo de malware facilita una mejor comunicación entre el equipo SOC. ¿Cuál es el nombre del archivo asociado con este malware?
3. Conocer la hora exacta en que se detectó por primera vez el malware puede ayudar a priorizar acciones. Si el malware se detecta recientemente, puede justificar esfuerzos más urgentes de contención y erradicación en comparación con amenazas antiguas y bien conocidas. ¿Puedes proporcionar la marca de tiempo UTC de la primera presentación de este malware en VirusTotal?
4. Comprender las técnicas utilizadas por el malware ayuda en la planificación estratégica de seguridad. ¿Cuál es el ID de la técnica MITRE ATT&CK para la recolección de datos del sistema por parte del malware antes de la exfiltración?
5. Después de la ejecución, ¿qué resolución de nombre de dominio realiza el malware?
6. Una vez identificadas las direcciones IP maliciosas, los dispositivos de seguridad de la red, como los firewalls, pueden configurarse para bloquear el tráfico hacia y desde estas direcciones. ¿Puedes proporcionar la dirección IP y el puerto de destino con el que se comunica el malware?
7. Si un servicio de hosting se utiliza frecuentemente para actividades maliciosas, los equipos de seguridad pueden implementar reglas de filtrado estrictas para todo el tráfico hacia y desde las IP pertenecientes a ese proveedor de hosting. ¿A qué servicio de hosting pertenece la IP identificada?
8. Las reglas YARA están diseñadas para identificar patrones y comportamientos específicos de malware. ¿Cuál es el nombre de la regla YARA creada por "Varp0s" que detecta el malware identificado?
9. Entender qué familias de malware están atacando a la organización ayuda en la planificación estratégica de seguridad para el futuro y en la priorización de recursos basados en la amenaza. ¿Puedes proporcionar los diferentes alias de malware asociados con la dirección IP maliciosa?
10. Al identificar las DLL importadas por el malware, podemos configurar herramientas de seguridad para monitorear la carga o el uso inusual de estas DLL específicas. ¿Puedes proporcionar la DLL utilizada por el malware para la escalada de privilegios?