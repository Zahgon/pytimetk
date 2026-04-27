import re
import matplotlib.colors as mcolors


def name_to_hex(color_name):
    pass


def parse_rgba(s):
    # Find all numbers (including floating points)
    pass


def hex_to_rgba(hex_color, alpha=1):
    """
    Convert hex to rgba.

    :param hex_color: str, hex color string (e.g. '#RRGGBB' or '#RRGGBBAA')
    :param alpha: float, alpha value ranging from 0 (transparent) to 1 (opaque)
    :return: str, a string representation of rgba color 'rgba(R, G, B, A)'
    """
    pass


def rgba_to_hex(r, g, b, a):
    """
    Convert RGBA values to their 8-character hexadecimal representation.

    Parameters:
    - r, g, b: Red, Green, and Blue components (integers from 0 to 255).
    - a: Alpha/opacity component (float from 0.0 to 1.0).

    Returns:
    - The 8-character hex representation of the RGBA values (string).
    """
    pass
