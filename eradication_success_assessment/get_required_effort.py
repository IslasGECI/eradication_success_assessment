#!/usr/bin/env python
#
#
from scipy.stats import genextreme
import numpy as np
import pandas as pd
import typer
import json
from esa import make_fit, plot_histogram_effort

app = typer.Typer()


def read_json(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data


@app.command()
def get_required_effort(
    name: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv",
    seed: bool = False,
    n_bootstrapping: int = 30,
    return_effort: bool = False,
):
    capture_date = pd.to_datetime("2019-11-09")

    datafile: str = name
    data = pd.read_csv(datafile)
    output = make_fit(data, capture_date, seed, n_bootstrapping, return_effort)
    print(json.dumps(output))
    return output


@app.command()
def write_methodology():
    print(
        """
\\subsection*{Análisis}
Utilizamos la función de distribución de valores extremos generalizada (GEV, por sus siglas en
inglés) para modelar la probabilidad de éxito en la erradiación de rata a partir de las
observaciones en cámaras trampa. La GEV es una familia de funciones continuas de probabilidad que
combina las funciones de Gumbel, Fréchet y Weibull, conocidas como funciones de distribución de
valores extremos de tipo I, II y III:
$$
f(s;\\xi) = \\left\\{
        \\begin{array}{ll}
            \\exp(-(1+\\xi s)^{\\frac{-1}{\\xi}}) & \\quad \\xi \\neq 0 \\\\
            \\exp(-\\exp(-s)) & \\quad \\xi = 0
        \\end{array}
    \\right.
$$
el tipo I es cuando $\\xi = 0$, el tipo II cuando $\\xi > 0$ y el tipo III con $\\xi<0$.

Considerando los esfuerzos entre avistamientos, definimos la probabilidad de obtener una captura
dependiendo del esfuerzo dado. De manera similar, podemos saber cuál es el esfuerzo necesario para
tener una probabilidad de éxito de erradicación deseada. A mayor esfuerzo, sin evidencia de rata, la
probabilidad del éxito en la erradicación será mayor.

Calculamos el esfuerzo necesario para alcanzar una probabilidad de
\\py{'%4.1f'% success_probability}\\%
en el éxito de la erradicación, con un nivel de significancia del
$\\alpha=$\\py{'%4.2f'% effort['significance_level']}.
"""
    )


@app.command()
def version():
    ver = "0.2.0"
    print(ver)


@app.command()
def plot_histogram_effort(path: str = "tests/data/salidita.json"):
    plot_histogram_effort(path)


def _clean_effort(data):
    to_plot = [x for x in data["effort"] if x < 1000]
    return to_plot


if __name__ == "__main__":
    app()
