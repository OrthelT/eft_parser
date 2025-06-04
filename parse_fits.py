from dataclasses import dataclass, field
from typing import Optional, List

import json
import yaml

fit_db = "fits.db"
sde_db = "sde_types.db"

@dataclass
class Module:
    name: str
    charge: Optional[str] = None

    def to_dict(self):
        return {'name': self.name, 'charge': self.charge}

@dataclass
class Drone:
    name: str
    quantity: int

    def to_dict(self):
        return {'name': self.name, 'quantity': self.quantity}

@dataclass
class Cargo:
    name: str
    quantity: int

    def to_dict(self):
        return {'name': self.name, 'quantity': self.quantity}

@dataclass
class Rig:
    name: str

    def to_dict(self):
        return {'name': self.name}

@dataclass
class Fit:
    ship: str
    name: str
    low_slots: List[Module] = field(default_factory=list)
    mid_slots: List[Module] = field(default_factory=list)
    high_slots: List[Module] = field(default_factory=list)
    rigs: List[Module] = field(default_factory=list)
    subsystems: List[Module] = field(default_factory=list)
    drones: List[Drone] = field(default_factory=list)
    cargo: List[Cargo] = field(default_factory=list)

    def __repr__(self):
        return f"Fit(ship={self.ship}, name={self.name}, low_slots={self.low_slots}, mid_slots={self.mid_slots}, high_slots={self.high_slots}, rigs={self.rigs}, subsystems={self.subsystems}, drones={self.drones}, cargo={self.cargo})"
    
    def __str__(self):
        return self.__repr__()


    def to_dict(self):
        """
        Convert a Fit object to a dictionary.
        """
        return {
            'ship': self.ship,
            'name': self.name,
            'low_slots': [m.to_dict() for m in self.low_slots],
            'mid_slots': [m.to_dict() for m in self.mid_slots],
            'high_slots': [m.to_dict() for m in self.high_slots],
            'rigs': [m.to_dict() for m in self.rigs],
            'subsystems': [m.to_dict() for m in self.subsystems],
            'drones': [d.to_dict() for d in self.drones],
            'cargo': [c.to_dict() for c in self.cargo]
        }
    
    def to_json(self):
        """
        Convert a Fit object to a JSON string.
        """
        return json.dumps(self.to_dict(), indent=4)
    
    def to_yaml(self):
        """
        Convert a Fit object to a YAML string.
        """
        return yaml.dump(self.to_dict())
    
    def to_eft(self):
        """
        Convert a Fit object to an EFT string.
        """

        eft_fit = f"[{self.ship},{self.name}]\n"
        
        for low_slot in self.low_slots:
            eft_fit += f"{low_slot.name},{low_slot.charge}\n"
        eft_fit += "\n"  # Blank line after low slots
        
        for mid_slot in self.mid_slots:
            eft_fit += f"{mid_slot.name},{mid_slot.charge}\n"
        eft_fit += "\n"  # Blank line after mid slots
        
        for high_slot in self.high_slots:
            eft_fit += f"{high_slot.name},{high_slot.charge}\n"
        eft_fit += "\n"  # Blank line after high slots
        
        for rig in self.rigs:
            eft_fit += f"{rig.name}\n"
        eft_fit += "\n"  # Blank line after rigs
        
        for subsystem in self.subsystems:
            eft_fit += f"{subsystem.name},{subsystem.charge}\n"
        eft_fit += "\n"  # Blank line after subsystems
        
        for drone in self.drones:
            eft_fit += f"{drone.name} x{drone.quantity}\n"
        eft_fit += "\n"  # Blank line after drones
        
        for cargo in self.cargo:
            eft_fit += f"{cargo.name} x{cargo.quantity}\n"
        
        return eft_fit

class EFTParser:
    """
    Parse an EFT file into a Fit object.

    Args:
        text (str): The EFT data to parse

    Returns:
        Fit: A Fit object created from the EFT data
    """

    def parse(self, text: str) -> Fit:
        lines = text.strip().splitlines()
        if not lines or not lines[0].startswith('['):
            raise ValueError("Invalid EFT format")

        ship_line = lines[0].strip('[]')
        ship, fit_name = map(str.strip, ship_line.split(',', 1))
        fit = Fit(ship=ship, name=fit_name)

        state = ParserState()

        for line in lines[1:]:
            stripped = state.process_line(line)
            if not stripped:
                continue

            # Parse line into module or drone
            if state.section == 0:
                fit.low_slots.append(self._parse_module(stripped))
            elif state.section == 1:
                fit.mid_slots.append(self._parse_module(stripped))
            elif state.section == 2:
                fit.high_slots.append(self._parse_module(stripped))
            elif state.section == 3:
                fit.rigs.append(self._parse_rig(stripped))
            elif state.section == 4:
                fit.subsystems.append(self._parse_module(stripped))
            elif state.section == 5:
                fit.drones.append(self._parse_drone(stripped))
            elif state.section == 6:
                fit.cargo.append(self._parse_cargo(stripped))
        return fit

    def _parse_module(self, line: str) -> Module:
        if ',' in line:
            name, charge = map(str.strip, line.split(',', 1))
            return Module(name, charge)
        return Module(line.strip())

    def _parse_rig(self, line: str) -> Rig:
        return Rig(line.strip())
    
    def _parse_drone(self, line: str) -> Drone:
        if ' x' in line:
            name, qty = line.rsplit(' x', 1)
            return Drone(name.strip(), int(qty.strip()))
        return Drone(line.strip())
    
    def _parse_cargo(self, line: str) -> Cargo:
        if ' x' in line:
            name, qty = line.rsplit(' x', 1)
            return Cargo(name.strip(), int(qty.strip()))
        return Cargo(line.strip())

class ParserState:
    def __init__(self):
        self.section = 0
        self.in_blank_block = False

    def process_line(self, line: str):
        line = line.strip()
        if not line:
            if not self.in_blank_block:
                self.section += 1
                self.in_blank_block = True
        else:
            self.in_blank_block = False
        return line

def fit_from_eft(data: str) -> Fit:
    """
    Create a Fit object from an EFT file. This is the same as the EFTParser.parse() 
    method, but is added as a convenience function and for consistency with fit_from_yaml()
    and fit_from_json().
    
    Args:
        data (str): The EFT data to parse
        
    """
    parser = EFTParser()
    return parser.parse(data)

def fit_from_yaml(data: yaml.YAMLObject) -> Fit:
    """
    Create a Fit object from a YAML file.
    
    Args:
        data (yaml.YAMLObject): The YAML data to parse
        
    """
    if isinstance(data, str):
        data = yaml.load(data, Loader=yaml.loader.SafeLoader)

    fit = Fit(ship=data['ship'], name=data['name'])

    fit.low_slots = [Module(low_slot['name'], low_slot['charge']) for low_slot in data['low_slots']]
    fit.mid_slots = [Module(mid_slot['name'], mid_slot['charge']) for mid_slot in data['mid_slots']]
    fit.high_slots = [Module(high_slot['name'], high_slot['charge']) for high_slot in data['high_slots']]
    fit.rigs = [Rig(rig['name']) for rig in data['rigs']]
    fit.subsystems = [Module(subsystem['name'], subsystem['charge']) for subsystem in data['subsystems']]
    fit.drones = [Drone(drone['name'], drone['quantity']) for drone in data['drones']]
    fit.cargo = [Cargo(cargo['name'], cargo['quantity']) for cargo in data['cargo']]

    return fit

def fit_from_json(data: dict) -> Fit:
    """
    Create a Fit object from a JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file containing the fit data
        
    Returns:
        Fit: A Fit object created from the JSON data
    """
    if isinstance(data, str):
        data = json.loads(data)

    fit = Fit(ship=data['ship'], name=data['name'])
    fit.low_slots = [Module(low_slot['name'], low_slot['charge']) for low_slot in data['low_slots']]
    fit.mid_slots = [Module(mid_slot['name'], mid_slot['charge']) for mid_slot in data['mid_slots']]
    fit.high_slots = [Module(high_slot['name'], high_slot['charge']) for high_slot in data['high_slots']]
    fit.rigs = [Rig(rig['name']) for rig in data['rigs']]
    fit.subsystems = [Module(subsystem['name'], subsystem['charge']) for subsystem in data['subsystems']]
    fit.drones = [Drone(drone['name'], drone['quantity']) for drone in data['drones']]
    fit.cargo = [Cargo(cargo['name'], cargo['quantity']) for cargo in data['cargo']]
    
    return fit

if __name__ == '__main__':
    pass