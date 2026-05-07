# Guía del Equipo SISVENIN

## Nuestro compromiso como equipo

### 1. Primero la prueba, después el código (TDD)

**Regla:** Nunca escribimos una línea de código de producción sin tener una prueba que falle primero.

**Cómo lo hacemos:**
1. Creamos el archivo de prueba en `tests/`
2. Escribimos lo que QUEREMOS que pase
3. Ejecutamos `pytest` → debe fallar (ROJO)
4. Escribimos el código mínimo para que pase
5. Ejecutamos `pytest` → debe pasar (VERDE)
6. Refactorizamos (mejoramos sin romper)

### 2. Todo el código en parejas (Pair Programming)

**Regla:** Siempre somos dos personas frente a una computadora.

**Roles:**
- **Conductor:** Escribe el código (tiene el teclado)
- **Navegante:** Revisa, piensa, busca errores (NO toca el teclado)

**Rotación:** Cada 30 minutos cambiamos roles.

### 3. Nadie programa solo

**Regla:** No existe el código escrito por una sola persona.

**Cómo lo garantizamos:**
- Cada commit tiene al menos 2 autores (ej: "Firma: Fiorela y Lenin")
- Los Pull Requests necesitan revisión de otra pareja
- Si alguien está programando solo, se lo decimos: "Pausa, busquemos a tu pareja"

### 4. Preguntar es obligatorio

**Regla:** No hay preguntas tontas. Preguntar es un acto de coraje.

**Cómo lo hacemos:**
- En el daily (9 AM) cada uno dice "me bloquea..."
- Tenemos un canal de WhatsApp para preguntas rápidas
- Todos tenemos un "buddy" a quien preguntar primero

## Herramientas que usamos

| Herramienta | ¿Para qué? |
|-------------|------------|
| GitHub | Repositorio de código |
| Trello | Tablero de tareas (historias de usuario) |
| WhatsApp | Comunicación rápida |
| Google Docs | Bitácora del equipo |
| pytest | Ejecutar pruebas |
| PySide6 | Interfaz gráfica |

## Horarios

| Hora | Actividad |
|------|-----------|
| 9:00 - 9:15 | Daily (de pie, 15 min máximo) |
| 9:15 - 12:00 | Programación en parejas |
| 12:00 - 1:00 | Almuerzo |
| 1:00 - 3:00 | Programación en parejas |
| 3:00 - 3:15 | Break |
| 3:15 - 5:00 | Programación en parejas |
| 5:00 - 5:30 | Integración + retrospectiva del día |

## Qué hacer si...

**...te bloqueas más de 15 minutos:**
1. Pregunta a tu pareja
2. Si no saben, pregunta al grupo de WhatsApp
3. Si nadie sabe, lo anotas en la pizarra de bloqueos

**...falta tu pareja:**
1. Te unes a otra pareja
2. No programas solo bajo ninguna circunstancia

**...las pruebas fallan después de tu cambio:**
1. No subas nada hasta que pasen
2. Revisa qué rompiste
3. Pide ayuda si no encuentras el error

**...el cliente pide un cambio urgente:**
1. Lo anotamos en Trello
2. Lo priorizamos en la próxima iteración
3. No cambiamos la iteración actual (a menos que sea una emergencia real)

## Firmas de compromiso

Yo, ____________________, me comprometo a seguir estas reglas.

Firma: ____________________
Fecha: ____________________