# EFT Parser

A Python library for parsing and converting EVE Online ship fittings between different formats (EFT, JSON, and YAML). Now with full support for **structure fits**!


## Features

- Parse EFT (EVE Fitting Tool) format fittings for **both ships and structures**
- Convert fittings between EFT, JSON, and YAML formats
- Structured data model for ship and structure fittings
- **Automatic structure detection** using a slimmed-down version of the EVE SDE saved to a SQLite database
- Support for all fitting components:
  - Low/Medium/High slots
  - Rigs
  - **Subsystems** (for ships) / **Service Slots** (for structures)
  - Drones
  - **Fighters** (separate from drones)
  - Cargo
- Proposes EFT2, a new human readable fitting format that uses markdown headings to delineate fitting sections rather than file position. 

## Installation

```bash
pip install eft-parser
```

## Usage

### Creating a Fit Object

```python
from eft_parser import Fit, fit_from_eft, fit_from_json, fit_from_yaml

# Ship fitting example
ship_eft = """[Tengu, PVE Tengu]
Ballistic Control System II
Ballistic Control System II

Multispectrum Shield Hardener II
10MN Afterburner II
Pithum C-Type Medium Shield Booster
EM Shield Hardener II
Pith X-Type Shield Boost Amplifier
Thukker Large Cap Battery
Pithum C-Type Medium Shield Booster

Heavy Assault Missile Launcher II
Sisters Expanded Probe Launcher
Heavy Assault Missile Launcher II
Heavy Assault Missile Launcher II
Covert Ops Cloaking Device II
Heavy Assault Missile Launcher II
Heavy Assault Missile Launcher II
Heavy Assault Missile Launcher II

Medium Rocket Fuel Cache Partition I
Medium Hydraulic Bay Thrusters II
Medium Capacitor Control Circuit II

Tengu Core - Augmented Graviton Reactor
Tengu Defensive - Covert Reconfiguration
Tengu Offensive - Accelerated Ejection Bay
Tengu Propulsion - Fuel Catalyst

Scourge Rage Heavy Assault Missile x5000
Scourge Javelin Heavy Assault Missile x5000
Sisters Core Scanner Probe x16


"""

# Structure fitting example  
structure_eft = """
[Tatara, *05R-7A - Moon Station]
Standup Layered Armor Plating II
Standup Ballistic Control System I
Standup Missile Guidance Enhancer I

Standup Warp Disruption Burst Projector
Standup Focused Warp Disruptor II
Standup Stasis Webifier II
Standup Variable Spectrum ECM I

Standup Guided Bomb Launcher II
Standup Point Defense Battery II
Standup Multirole Missile Launcher II

Standup L-Set Moon Drilling Proficiency I


Standup Moon Drill I
Standup Reprocessing Facility I
Standup Composite Reactor I


Standup Light Missile x5000
Standup Heavy Guided Bomb x100

Standup Locust II x12

"""

ship_fit = fit_from_eft(ship_eft)
structure_fit = fit_from_eft(structure_eft)

# Automatic structure detection
print(f"Ship fit is structure: {ship_fit.is_structure}")      # False
print(f"Structure fit is structure: {structure_fit.is_structure}")  # True
```

### Structure vs Ship Differences

The parser automatically detects structures using the EVE SDE database and handles them differently:

```python
# For ships - subsystems are populated
if not fit.is_structure:
    for subsystem in fit.subsystems:
        print(f"Subsystem: {subsystem.name}")

# For structures - service_slots are populated  
if fit.is_structure:
    for service in fit.service_slots:
        print(f"Service Slot: {service.name}")
```

### Working with Fighters

Structures and carriers support fighters as a separate category from drones:

```python
# Both drones and fighters are supported
for drone in fit.drones:
    print(f"Drone: {drone.name} x{drone.quantity}")
    
for fighter in fit.fighters:
    print(f"Fighter: {fighter.name} x{fighter.quantity}")
```

### Converting Between Formats

```python
# Convert to EFT format
eft_string = fit.to_eft()

# Convert to JSON (includes structure flag and all new fields)
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
is_structure = fit.is_structure

# Slot components
low_slots = fit.low_slots
mid_slots = fit.mid_slots  
high_slots = fit.high_slots
rigs = fit.rigs

# Ship vs Structure specific
subsystems = fit.subsystems      # For ships
service_slots = fit.service_slots # For structures

# Combat units
drones = fit.drones
fighters = fit.fighters          # New!

# Items  
cargo = fit.cargo

# Each component has its own properties
for module in fit.low_slots:
    print(f"Module: {module.name}, Charge: {module.charge}")

for drone in fit.drones:
    print(f"Drone: {drone.name}, Quantity: {drone.quantity}")
```

## Data Models

### Fit
- `ship`: Ship/structure name
- `name`: Fit name
- `is_structure`: Boolean flag indicating if this is a structure fit
- `low_slots`: List of low slot modules
- `mid_slots`: List of mid slot modules
- `high_slots`: List of high slot modules
- `rigs`: List of rigs
- `subsystems`: List of subsystems (ships only)
- `service_slots`: List of service modules (structures only)
- `drones`: List of drones
- `fighters`: List of fighters (new!)
- `cargo`: List of cargo items

### Module
- `name`: Module name
- `charge`: Optional charge name

### Drone/Fighter
- `name`: Drone/Fighter name
- `quantity`: Number of units

### Cargo
- `name`: Cargo item name
- `quantity`: Number of items

### Rig
- `name`: Rig name

### Subsystem
- `name`: Subsystem name

## Database Integration

The parser uses an integrated EVE SDE (Static Data Export) database to:
- Automatically detect structures vs ships
- Validate item categories
- Ensure proper parsing of subsystems vs service slots

The database file (`sde_lite.sqlite`) is included with the package.

## EFT2 Fitting Format

Proposes a new format that uses markdown syntax to define fitting sections. Fitted charges and item quantities are delineated with commas.

Ship name and fit name appear at the top of the file separated by commas after a single hash sign:

```
# Caracal, RML v2.0
```

Fitting sections are defined by lines starting with a double hash sign:
```
## Low Slots
Ballistic Control System I
Ballistic Control System I
Ballistic Control System I
IFFA Compact Damage Control
```

Charges are separated by commas:
```
## High Slots
Prototype 'Arbalest' Heavy Assault Missile Launcher I, Scourge Heavy Assault Missile
Prototype 'Arbalest' Heavy Assault Missile Launcher I, Scourge Heavy Assault Missile
```

Quantities are also separated by commas:
```
## Drones
Hornet I, 2

## Fighters  
Standup Templar II, 1

## Cargo
Scourge Heavy Assault Missile, 300
```

For structures, use `## Service Slots` instead of `## Subsystems`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

## Contact
OrthelToralen (Discord)
Orthel.Toralen@gmail.com (email)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
