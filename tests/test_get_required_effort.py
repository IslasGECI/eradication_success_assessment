import pytest
import pandas as pd
from pandas._testing import assert_frame_equal
from eradication_success_assessment import get_required_effort
from eradication_success_assessment import plot_histogram_effort
from eradication_success_assessment.get_required_effort import _clean_effort
from eradication_success_assessment.get_required_effort import app

input_test: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv"
data: pd.DataFrame = pd.read_csv(input_test)
capture_date = pd.to_datetime("2019-11-09")
d: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10", "2019-11-11"],
    "Cantidad_de_trampas_activas": [1, 2, 3, 4],
    "Cantidad_de_avistamientos": [1, 0, 0, 0],
    "is_sighting": [True, False, False, False],
}
dates: pd.DataFrame = pd.DataFrame(data=d)


OUTPUT_TESTS_2 = '{"required_effort": 381, "success_probability": 0.99, "significance_level": 0.050000000000000044, "effort_without_sighted": 681}\n'


def test_get_required_effort(capsys):
    get_required_effort(seed=True, n_bootstrapping=30)
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_TESTS_2
    get_required_effort(n_bootstrapping=30)
    captured = capsys.readouterr()
    assert captured.out != OUTPUT_TESTS_2
    get_required_effort(seed=True)
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_TESTS_2


d_2: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10", "2019-11-11"],
    "Cantidad_de_trampas_activas": [1, 2, 3, 4],
    "Cantidad_de_avistamientos": [1, 0, 0, 0],
    "is_sighting": [True, False, False, False],
    "sighting": [1, 1, 1, 1],
}
dates_2: pd.DataFrame = pd.DataFrame(data=d_2)


def test__clean_effort():
    DATA = {"effort": [1, 2, 3, 1000]}
    df_data = pd.DataFrame.from_dict(DATA)
    expected_effort = [1, 2, 3]
    obtained_effort = _clean_effort(df_data)
    assert expected_effort == obtained_effort


def test_app():
    assert app is not None
