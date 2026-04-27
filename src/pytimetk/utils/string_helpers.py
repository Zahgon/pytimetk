import re


_MODERN_TO_LEGACY_FREQ_UNITS = {
    "H": "H",
    "MIN": "min",
    "T": "T",
    "S": "S",
    "L": "L",
    "MS": "MS",
    "U": "U",
    "US": "U",
    "N": "N",
    "NS": "N",
    "D": "D",
    "W": "W",
    "M": "M",
    "ME": "M",
    "Q": "Q",
    "QE": "Q",
    "QS": "QS",
    "Y": "Y",
    "YE": "Y",
    "YS": "YS",
    "A": "A",
    "AS": "AS",
    "BM": "BM",
    "BME": "BM",
    "BMS": "BMS",
    "BQ": "BQ",
    "BQE": "BQ",
    "BQS": "BQS",
    "BY": "BY",
    "BYE": "BY",
    "BYS": "BYS",
    "BA": "BA",
    "BAS": "BAS",
    "CBM": "CBM",
    "CBME": "CBM",
    "SM": "SM",
    "SME": "SM",
}


def canonicalize_frequency_unit(unit: str) -> str:
    """Map modern pandas frequency spellings back to pytimetk's canonical units."""
    pass


def parse_freq_str(freq_str):
    pass


def parse_freq_str2(freq_str):
    # Regular expression to match patterns like '2H', '30T', etc.
    pass
