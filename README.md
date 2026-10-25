# ChamiMesh

Proyecto TEL343: planificación de una red Mesh comunitaria en Fundo Chamiza,
considerando equipos nuevos y reacondicionados.

## Primer avance

Modelo de programación lineal entera (ILP) en Python con PuLP y el solver HiGHS.
Selecciona sitios y tipos de equipo para minimizar emisiones, sujeto a:

- Cubrir todos los puntos de demanda.
- Respetar el inventario de equipos.
- Instalar como máximo un equipo por sitio.

La variable binaria `x[sitio, equipo]` indica si se instala ese equipo en ese sitio.
Se comparan un escenario con equipos nuevos y otro que permite reutilización.

Los datos son **sintéticos**: cuatro sitios, seis puntos de demanda y dos tipos
de equipo. La cobertura es una relación supuesta, igual para ambos tipos.
Las emisiones representan totales ficticios de instalación y operación durante
cinco años, en kg CO2e. No son datos medidos ni resultados de Fundo Chamiza.

El modelo todavía no incluye conectividad al gateway, capacidad, rutas ni
propagación radioeléctrica. Resuelve solo cobertura y asignación de equipos.

## Ejecución

Requiere uv y Python 3.10 o posterior.

```bash
uv run optimizacion.py
```

uv crea el entorno e instala las dependencias automáticamente. Se incluye
`uv.lock` para reproducir las versiones utilizadas.

El programa muestra el estado del solver, las instalaciones elegidas y las
emisiones totales. Con este ejemplo, el óptimo es 100 kg CO2e usando solo equipos
nuevos y 70 kg CO2e permitiendo reutilización. Puede haber varias selecciones
de sitios con el mismo valor óptimo.
