"""
Tests for the parse_fits module.
"""
import pytest
from eft_parser import (
    Fit,
    Module,
    Rig,
    Drone,
    Cargo,
    fit_from_eft,
    fit_from_json,
    fit_from_yaml,
)

def test_parse_simple_eft():
    eft_data = """[Venture, Venture - Mining]
Mining Laser Upgrade II
Mining Laser Upgrade II



Mining Laser II
Mining Laser II

Small Core Defense Field Extender I
Small Core Defense Field Extender I



Mining Drone I x5
"""
    fit = fit_from_eft(eft_data)
    
    assert fit.ship == "Venture"
    assert fit.name == "Venture - Mining"
    assert len(fit.low_slots) == 2
    assert len(fit.mid_slots) == 0  # No mid slots in this fit
    assert len(fit.high_slots) == 2
    assert len(fit.rigs) == 2
    assert len(fit.drones) == 1
    assert fit.drones[0].quantity == 5

def test_convert_formats():
    eft_data = """[Venture, Venture - Mining]
Mining Laser Upgrade II



"""
    fit = fit_from_eft(eft_data)
    
    # Test conversion to JSON
    json_data = fit.to_json()
    fit_from_json_data = fit_from_json(json_data)
    assert fit_from_json_data.ship == fit.ship
    assert fit_from_json_data.name == fit.name
    
    # Test conversion to YAML
    yaml_data = fit.to_yaml()
    fit_from_yaml_data = fit_from_yaml(yaml_data)
    assert fit_from_yaml_data.ship == fit.ship
    assert fit_from_yaml_data.name == fit.name

def test_parse_module_with_charge():
    eft_data = """[Venture, Test Fit]
Capacitor Flux Coil II,Capacitor Flux Coil II
"""
    fit = fit_from_eft(eft_data)
    assert len(fit.low_slots) == 1
    assert fit.low_slots[0].name == "Capacitor Flux Coil II"
    assert fit.low_slots[0].charge == "Capacitor Flux Coil II"

def test_parse_drone_quantity():
    eft_data = """[Venture, Test Fit]
Mining Laser Upgrade II



Mining Laser II

Small Core Defense Field Extender I




Hobgoblin II x5
"""
    fit = fit_from_eft(eft_data)
    assert len(fit.drones) == 1
    assert fit.drones[0].name == "Hobgoblin II"
    assert fit.drones[0].quantity == 5

def test_parse_cargo():
    eft_data = """[Venture, Test Fit]
Mining Laser Upgrade II



Mining Laser II

Small Core Defense Field Extender I



Mining Drone I x2

Nanite Repair Paste x100
Cap Booster 150 x50
"""
    fit = fit_from_eft(eft_data)
    assert len(fit.cargo) == 2
    assert fit.cargo[0].name == "Nanite Repair Paste"
    assert fit.cargo[0].quantity == 100
    assert fit.cargo[1].name == "Cap Booster 150"
    assert fit.cargo[1].quantity == 50

def test_invalid_eft_format():
    with pytest.raises(ValueError, match="Invalid EFT format"):
        fit_from_eft("Invalid EFT data") 