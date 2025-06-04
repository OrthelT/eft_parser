# EFT Parser

A Python library for parsing and converting EVE Online ship fittings between different formats (EFT, JSON, and YAML).


## Features

- Parse EFT (EVE Fitting Tool) format fittings
- Convert fittings between EFT, JSON, and YAML formats
- Structured data model for ship fittings
- Support for all fitting components:
  - Low/Medium/High slots
  - Rigs
  - Subsystems
  - Drones
  - Cargo

## Installation

```bash
pip install eft-parser
```

## Usage

### Creating a Fit Object

```python
from parse_fits import Fit, fit_from_eft, fit_from_json, fit_from_yaml

# From EFT format
eft_data = """
[Ship Name, Fit Name]
Module Name, Charge Name

[Empty Mid slot]

[Empty High slot]

Rig Name

Subsystem Name, Charge Name

Drone Name x5

Cargo Item x100
"""
fit = fit_from_eft(eft_data)
or fit = EFTParser.parse(eft_data)

# From JSON
json_data = {
    "ship": "Ship Name",
    "name": "Fit Name",
    "low_slots": [{"name": "Module Name", "charge": "Charge Name"}],
    "mid_slots": [],
    "high_slots": [],
    "rigs": [{"name": "Rig Name"}],
    "subsystems": [{"name": "Subsystem Name", "charge": "Charge Name"}],
    "drones": [{"name": "Drone Name", "quantity": 5}],
    "cargo": [{"name": "Cargo Item", "quantity": 100}]
}
fit = fit_from_json(json_data)

# From YAML
yaml_data = """
ship: Ship Name
name: Fit Name
low_slots:
  - name: Module Name
    charge: Charge Name
"""
fit = fit_from_yaml(yaml_data)
```

### Converting Between Formats

```python
# Convert to EFT format
eft_string = fit.to_eft()

# Convert to JSON
json_string = fit.to_json()

# Convert to YAML
yaml_string = fit.to_yaml()

# Convert to dictionary
fit_dict = fit.to_dict()
```

### Working with Fit Components

```python
# Access fit components
ship_name = fit.ship
fit_name = fit.name
low_slots = fit.low_slots
mid_slots = fit.mid_slots
high_slots = fit.high_slots
rigs = fit.rigs
subsystems = fit.subsystems
drones = fit.drones
cargo = fit.cargo

# Each component has its own properties
for module in fit.low_slots:
    print(f"Module: {module.name}, Charge: {module.charge}")

for drone in fit.drones:
    print(f"Drone: {drone.name}, Quantity: {drone.quantity}")
```

## Data Models

### Fit
- `ship`: Ship name
- `name`: Fit name
- `low_slots`: List of low slot modules
- `mid_slots`: List of mid slot modules
- `high_slots`: List of high slot modules
- `rigs`: List of rigs
- `subsystems`: List of subsystems
- `drones`: List of drones
- `cargo`: List of cargo items

### Module
- `name`: Module name
- `charge`: Optional charge name

### Drone
- `name`: Drone name
- `quantity`: Number of drones

### Cargo
- `name`: Cargo item name
- `quantity`: Number of items

### Rig
- `name`: Rig name

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

## Contact
OrthelToralen (Discord)
Orthel.Toralen@gmail.com (email)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
