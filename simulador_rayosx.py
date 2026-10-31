"""Simulador interactivo de ejercicios de rayos X y efecto Compton."""

import argparse
import math


# Constantes solicitadas para los ejercicios de clase (Sistema Internacional).
C = 3.0e8  # Velocidad de la luz, m/s
H = 6.625e-34  # Constante de Planck, J·s
LONGITUD_COMPTON = 2.4e-12  # h / (m_e c), m
JOULES_POR_EV = 1.6e-19  # J/eV

UNIDADES_LONGITUD = {
    "angstrom": 1.0e-10,
    "nanometro": 1.0e-9,
    "picometro": 1.0e-12,
}


class SimuladorCompton:
    """Calcula magnitudes de fotones y electrones en el efecto Compton."""

    @staticmethod
    def a_metros(longitud, unidad):
        """Convierte una longitud ingresada a metros."""
        try:
            factor = UNIDADES_LONGITUD[unidad]
        except KeyError as error:
            mensaje = "La unidad debe ser angstrom, nanometro o picometro."
            raise ValueError(mensaje) from error
        if longitud <= 0 or not math.isfinite(longitud):
            raise ValueError(
                "La longitud de onda debe ser un numero positivo y finito."
            )
        return longitud * factor

    @staticmethod
    def energia(longitud):
        """Devuelve la energía del fotón en joules."""
        if longitud <= 0 or not math.isfinite(longitud):
            raise ValueError(
                "La longitud de onda debe ser un numero positivo y finito."
            )
        return H * C / longitud

    @staticmethod
    def cantidad_movimiento(longitud):
        """Devuelve la cantidad de movimiento del fotón en kg·m/s."""
        if longitud <= 0 or not math.isfinite(longitud):
            raise ValueError(
                "La longitud de onda debe ser un numero positivo y finito."
            )
        return H / longitud

    @staticmethod
    def longitud_onda_final(longitud_inicial, angulo_grados):
        """Calcula la longitud dispersada mediante la ecuación de Compton."""
        SimuladorCompton._validar_entrada(longitud_inicial, angulo_grados)
        angulo = math.radians(angulo_grados)
        return longitud_inicial + LONGITUD_COMPTON * (1.0 - math.cos(angulo))

    @staticmethod
    def energia_cinetica(longitud_inicial, longitud_final):
        """Calcula la energía cinética del electrón de retroceso en J."""
        energia_inicial = SimuladorCompton.energia(longitud_inicial)
        energia_final = SimuladorCompton.energia(longitud_final)
        return energia_inicial - energia_final

    @staticmethod
    def angulo_electron(longitud_inicial, longitud_final, angulo_foton_grados):
        """Calcula el ángulo del electrón de retroceso en grados."""
        SimuladorCompton._validar_entrada(
            longitud_inicial, angulo_foton_grados
        )
        if longitud_final <= 0 or not math.isfinite(longitud_final):
            raise ValueError(
                "La longitud de onda final debe ser positiva y finita."
            )
        angulo_foton = math.radians(angulo_foton_grados)
        numerador = longitud_inicial * math.sin(angulo_foton)
        denominador = longitud_final - longitud_inicial * math.cos(
            angulo_foton
        )
        return math.degrees(math.atan2(numerador, denominador))

    @staticmethod
    def _validar_entrada(longitud_inicial, angulo_grados):
        """Valida la longitud de onda inicial y el ángulo del fotón."""
        if longitud_inicial <= 0 or not math.isfinite(longitud_inicial):
            raise ValueError(
                "La longitud de onda inicial debe ser positiva y finita."
            )
        if (
            not math.isfinite(angulo_grados)
            or not 0 <= angulo_grados <= 180
        ):
            raise ValueError("El angulo debe estar entre 0 y 180 grados.")


def _leer_numero(mensaje):
    """Solicita un número finito y repite ante entradas inválidas."""
    while True:
        try:
            valor = float(input(mensaje).strip())
            if not math.isfinite(valor):
                raise ValueError
            return valor
        except ValueError:
            print("Entrada invalida. Escribe un numero finito.")


def _leer_longitud_inicial(simulador):
    """Solicita una longitud de onda y la convierte a metros."""
    unidades = {
        "1": ("angstrom", "angstroms"),
        "2": ("nanometro", "nanometros"),
        "3": ("picometro", "picometros"),
    }
    while True:
        print(
            "Unidad de longitud de onda: 1. angstroms  2. nanometros  "
            "3. picometros"
        )
        opcion = input("Selecciona una unidad (1-3): ").strip()
        if opcion not in unidades:
            print("Opcion invalida. Selecciona 1, 2 o 3.")
            continue
        unidad, nombre = unidades[opcion]
        mensaje = "Longitud de onda inicial en {}: ".format(nombre)
        longitud = _leer_numero(mensaje)
        try:
            return simulador.a_metros(longitud, unidad)
        except ValueError as error:
            print(error)


def _leer_angulo():
    """Solicita un ángulo de dispersión entre 0 y 180 grados."""
    while True:
        angulo = _leer_numero("Angulo de dispersion del foton (grados): ")
        if 0 <= angulo <= 180:
            return angulo
        print("El angulo debe estar entre 0 y 180 grados.")


def _mostrar_energia(nombre, energia_joules):
    """Muestra energía en joules, electronvoltios y megaelectronvoltios."""
    energia_ev = energia_joules / JOULES_POR_EV
    print(
        "{}: {:.6e} J | {:.6e} eV | {:.6e} MeV".format(
            nombre, energia_joules, energia_ev, energia_ev / 1.0e6
        )
    )


def _mostrar_resultados_foton(simulador, longitud_inicial, longitud_final):
    """Muestra las longitudes de onda y energías de los fotones."""
    energia_inicial = simulador.energia(longitud_inicial)
    energia_final = simulador.energia(longitud_final)
    print("Longitud de onda inicial: {:.6e} m".format(longitud_inicial))
    print("Longitud de onda dispersada: {:.6e} m".format(longitud_final))
    _mostrar_energia("Energia incidente", energia_inicial)
    _mostrar_energia("Energia dispersada", energia_final)


def ejecutar_prueba():
    """Comprueba el caso solicitado: 0.050 Å y un ángulo de 65 grados."""
    simulador = SimuladorCompton()
    longitud_inicial = simulador.a_metros(0.050, "angstrom")
    angulo = 65.0
    longitud_final = simulador.longitud_onda_final(
        longitud_inicial, angulo
    )
    energia_cinetica = simulador.energia_cinetica(
        longitud_inicial, longitud_final
    )
    angulo_electron = simulador.angulo_electron(
        longitud_inicial, longitud_final, angulo
    )

    assert math.isclose(
        longitud_final - longitud_inicial,
        LONGITUD_COMPTON * (1.0 - math.cos(math.radians(angulo))),
        rel_tol=1.0e-12,
    )
    assert math.isclose(
        energia_cinetica,
        (
            simulador.cantidad_movimiento(longitud_inicial)
            - simulador.cantidad_movimiento(longitud_final)
        )
        * C,
        rel_tol=1.0e-12,
    )

    print(
        "Prueba preprogramada: lambda inicial = 0.050 angstrom, "
        "theta = 65 grados"
    )
    _mostrar_resultados_foton(simulador, longitud_inicial, longitud_final)
    _mostrar_energia("Energia cinetica del electron", energia_cinetica)
    print("Angulo del electron: {:.6f} grados".format(angulo_electron))
    print("Comprobacion matematica: correcta.")


def ejecutar_menu():
    """Ejecuta el menú interactivo del simulador en la terminal."""
    simulador = SimuladorCompton()
    while True:
        print("\n--- Simulador de Rayos X: Efecto Compton ---")
        print("1. Calcular longitud de onda final y energia")
        print("2. Calcular energia cinetica y angulo del electron")
        print("3. Ver cantidad de movimiento de los fotones")
        print("4. Salir")
        opcion = input("Elige una opcion (1-4): ").strip()

        if opcion == "4":
            print("Simulacion finalizada.")
            return
        if opcion not in {"1", "2", "3"}:
            print("Opcion invalida. Selecciona un numero del 1 al 4.")
            continue

        longitud_inicial = _leer_longitud_inicial(simulador)
        angulo = _leer_angulo()
        longitud_final = simulador.longitud_onda_final(
            longitud_inicial, angulo
        )

        if opcion == "1":
            _mostrar_resultados_foton(
                simulador, longitud_inicial, longitud_final
            )
        elif opcion == "2":
            energia_cinetica = simulador.energia_cinetica(
                longitud_inicial, longitud_final
            )
            _mostrar_energia("Energia cinetica del electron", energia_cinetica)
            angulo_electron = simulador.angulo_electron(
                longitud_inicial, longitud_final, angulo
            )
            print(
                "Angulo del electron: {:.6f} grados".format(angulo_electron)
            )
        else:
            momento_inicial = simulador.cantidad_movimiento(longitud_inicial)
            momento_final = simulador.cantidad_movimiento(longitud_final)
            print(
                "P0 (foton incidente): {:.6e} kg m/s".format(momento_inicial)
            )
            print(
                "Pf (foton dispersado): {:.6e} kg m/s".format(momento_final)
            )


def main():
    """Inicia el modo de prueba o el menú interactivo."""
    parser = argparse.ArgumentParser(
        description="Simulador interactivo de ejercicios del efecto Compton."
    )
    parser.add_argument(
        "--prueba",
        action="store_true",
        help="ejecuta el caso preprogramado de 0.050 Å y 65 grados",
    )
    argumentos = parser.parse_args()
    if argumentos.prueba:
        ejecutar_prueba()
    else:
        ejecutar_menu()


if __name__ == "__main__":
    main()
