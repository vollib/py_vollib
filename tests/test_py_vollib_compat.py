import importlib


def test_py_vollib_black_scholes_import_path_works():
    module = importlib.import_module("py_vollib.black_scholes")

    assert module.black_scholes("c", 100, 100, 0.5, 0.01, 0.2) == (
        importlib.import_module("vollib.black_scholes").black_scholes(
            "c", 100, 100, 0.5, 0.01, 0.2
        )
    )


def test_py_vollib_nested_import_path_works():
    compat = importlib.import_module("py_vollib.black.greeks.analytical")
    canonical = importlib.import_module("vollib.black.greeks.analytical")

    assert compat.theta("c", 49, 50, 0.3846, 0.05, 0.2) == canonical.theta(
        "c", 49, 50, 0.3846, 0.05, 0.2
    )
