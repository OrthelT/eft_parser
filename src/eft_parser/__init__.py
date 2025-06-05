"""
EFT Parser - A Python library for parsing and converting EVE Online ship fittings.
"""

from .parse_fits import (
    Fit,
    Module,
    Rig,
    Subsystem,
    Drone,
    Cargo,
    fit_from_eft,
    fit_from_eft2,
    fit_from_json,
    fit_from_yaml,
)

__version__ = "0.1.0"
__author__ = "OrthelToralen"
__email__ = "Orthel.Toralen@gmail.com"

__all__ = [
    "Fit",
    "Module",
    "Rig",
    "Subsystem",
    "Drone",
    "Cargo",
    "fit_from_eft",
    "fit_from_eft2",
    "fit_from_json",
    "fit_from_yaml",
] 