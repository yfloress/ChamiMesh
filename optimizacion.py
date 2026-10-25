import pulp


# Datos sintéticos, no corresponden a las parcelas de Fundo Chamiza.
DEMANDA = [1, 2, 3, 4, 5, 6]
COBERTURA = {
    "A": [1, 2, 3],
    "B": [3, 4, 5],
    "C": [4, 5, 6],
    "D": [1, 2, 6],
}
EMISIONES = {"nuevo": 50, "reacondicionado": 20}  # kg CO2e en cinco años


def resolver(nombre, inventario):
    modelo = pulp.LpProblem("Cobertura", pulp.LpMinimize)
    x = {
        (sitio, equipo): pulp.LpVariable(f"x_{sitio}_{equipo}", cat="Binary")
        for sitio in COBERTURA
        for equipo in inventario
    }

    modelo += pulp.lpSum(
        EMISIONES[equipo] * variable
        for (sitio, equipo), variable in x.items()
    )

    for punto in DEMANDA:
        modelo += pulp.lpSum(
            x[sitio, equipo]
            for sitio in COBERTURA
            for equipo in inventario
            if punto in COBERTURA[sitio]
        ) >= 1

    for sitio in COBERTURA:
        modelo += pulp.lpSum(x[sitio, equipo] for equipo in inventario) <= 1

    for equipo, cantidad in inventario.items():
        modelo += pulp.lpSum(x[sitio, equipo] for sitio in COBERTURA) <= cantidad

    modelo.solve(pulp.HiGHS(msg=False))
    estado = pulp.LpStatus[modelo.status]
    print(f"\n{nombre}: {estado}")

    if modelo.status != pulp.LpStatusOptimal:
        return

    for (sitio, equipo), variable in x.items():
        if variable.value() > 0.5:
            print(f"  Sitio {sitio}: {equipo}")
    print(f"  Emisiones: {pulp.value(modelo.objective):.1f} kg CO2e")


if __name__ == "__main__":
    resolver("Solo nuevos", {"nuevo": 4})
    resolver("Con reutilización", {"nuevo": 4, "reacondicionado": 1})
