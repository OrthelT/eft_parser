from dataclasses import dataclass, field
from eft_parser.utils.db_handler import get_category_info
from typing import Optional, List
import json
import yaml
import logging

logger = logging.getLogger(__name__)

fit_db = "fits.db"
sde_db = "sde_types.db"


@dataclass
class Module:
    name: str
    charge: Optional[str] = None

    def to_dict(self):
        return {"name": self.name, "charge": self.charge}


@dataclass
class Rig:
    name: str

    def to_dict(self):
        return {"name": self.name}


@dataclass
class Subsystem:
    name: str

    def to_dict(self):
        return {"name": self.name}


@dataclass
class Drone:
    name: str
    quantity: int

    def to_dict(self):
        return {"name": self.name, "quantity": self.quantity}


@dataclass
class Cargo:
    name: str
    quantity: int

    def to_dict(self):
        return {"name": self.name, "quantity": self.quantity}


@dataclass
class Fit:
    """
    A class to represent a fit object. Import functions create a fit object, which
    can be converted to a dictionary, JSON, YAML, EFT string, or EFT2 string.
    """

    ship: str
    name: str
    low_slots: List[Module] = field(default_factory=list)
    mid_slots: List[Module] = field(default_factory=list)
    high_slots: List[Module] = field(default_factory=list)
    rigs: List[Module] = field(default_factory=list)
    subsystems: List[Module] = field(default_factory=list)
    service_slots: List[Module] = field(
        default_factory=list
    )  # New attribute for structures
    drones: List[Drone] = field(default_factory=list)
    fighters: List[Drone] = field(default_factory=list)  # Add fighters support
    cargo: List[Cargo] = field(default_factory=list)
    is_structure: bool = False  # Flag to determine if the fit is a structure

    def __repr__(self):
        return f"Fit(ship={self.ship}, name={self.name}, low_slots={self.low_slots}, mid_slots={self.mid_slots}, high_slots={self.high_slots}, rigs={self.rigs}, subsystems={self.subsystems}, service_slots={self.service_slots}, drones={self.drones}, fighters={self.fighters}, cargo={self.cargo}, is_structure={self.is_structure})"

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        """
        Convert a Fit object to a dictionary.
        """
        return {
            "ship": self.ship,
            "name": self.name,
            "low_slots": [m.to_dict() for m in self.low_slots],
            "mid_slots": [m.to_dict() for m in self.mid_slots],
            "high_slots": [m.to_dict() for m in self.high_slots],
            "rigs": [m.to_dict() for m in self.rigs],
            "subsystems": [m.to_dict() for m in self.subsystems],
            "service_slots": [
                m.to_dict() for m in self.service_slots
            ],  # Include service_slots in dict
            "drones": [d.to_dict() for d in self.drones],
            "fighters": [
                f.to_dict() for f in self.fighters
            ],  # Include fighters in dict
            "cargo": [c.to_dict() for c in self.cargo],
            "is_structure": self.is_structure,
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

        if self.is_structure:
            for service_slot in self.service_slots:
                eft_fit += f"{service_slot.name}\n"
        else:
            for subsystem in self.subsystems:
                eft_fit += f"{subsystem.name}\n"
        eft_fit += "\n"  # Blank line after subsystems/service_slots

        for drone in self.drones:
            eft_fit += f"{drone.name} x{drone.quantity}\n"
        eft_fit += "\n"  # Blank line after drones

        for cargo in self.cargo:
            eft_fit += f"{cargo.name} x{cargo.quantity}\n"
        eft_fit += "\n"  # Blank line after cargo

        for fighter in self.fighters:
            eft_fit += f"{fighter.name} x{fighter.quantity}\n"

        return eft_fit

    def to_eft2(self):
        """
        Convert a Fit object to an EFT2.0 string.
        """
        eft2_fit = f"# {self.ship}, {self.name}\n"

        eft2_fit += "## Low Slots\n"
        for low_slot in self.low_slots:
            eft2_fit += f"{low_slot.name},{low_slot.charge}\n"
        eft2_fit += "\n"  # Blank line after low slots

        eft2_fit += "## Mid Slots\n"
        for mid_slot in self.mid_slots:
            eft2_fit += f"{mid_slot.name},{mid_slot.charge}\n"
        eft2_fit += "\n"  # Blank line after mid slots

        eft2_fit += "## High Slots\n"
        for high_slot in self.high_slots:
            eft2_fit += f"{high_slot.name},{high_slot.charge}\n"
        eft2_fit += "\n"  # Blank line after high slots

        eft2_fit += "## Rigs\n"
        for rig in self.rigs:
            eft2_fit += f"{rig.name}\n"
        eft2_fit += "\n"  # Blank line after rigs

        if self.is_structure:
            eft2_fit += "## Service Slots\n"
            for service_slot in self.service_slots:
                eft2_fit += f"{service_slot.name}\n"
        else:
            eft2_fit += "## Subsystems\n"
            for subsystem in self.subsystems:
                eft2_fit += f"{subsystem.name}\n"
        eft2_fit += "\n"  # Blank line after subsystems/service_slots

        eft2_fit += "## Drones\n"
        for drone in self.drones:
            eft2_fit += f"{drone.name} ,{drone.quantity}\n"
        eft2_fit += "\n"  # Blank line after drones

        eft2_fit += "## Cargo\n"
        for cargo in self.cargo:
            eft2_fit += f"{cargo.name} ,{cargo.quantity}\n"

        return eft2_fit


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
        if not lines or not lines[0].startswith("["):
            raise ValueError("Invalid EFT format")

        ship_line = lines[0].strip("[]")
        ship, fit_name = map(str.strip, ship_line.split(",", 1))
        fit = Fit(ship=ship, name=fit_name)

        # Check if the fit is a structure and set the flag
        ship_category = get_category_info(ship)
        if ship_category == 65:
            fit.is_structure = True

        state = ParserState()

        for line in lines[1:]:
            fit_item = state.process_line(line)

            # Parse line into module or drone
            if state.section == 0 and fit_item:
                fit.low_slots.append(self._parse_module(fit_item))
            elif state.section == 1:
                if fit_item:
                    fit.mid_slots.append(self._parse_module(fit_item))
            elif state.section == 2:
                if fit_item:
                    fit.high_slots.append(self._parse_module(fit_item))
            elif state.section == 3:
                if fit_item:
                    fit.rigs.append(self._parse_rig(fit_item))

            elif state.section == 4:
                if fit_item:
                    if " x" in fit_item:
                        item = self._parse_cargo(fit_item)
                        item_category = get_category_info(item.name)
                        if item_category == 8:
                            fit.cargo.append(item)
                    else:
                        item = self._parse_module(fit_item)
                        item_category = get_category_info(item.name)

                    if fit.is_structure:
                        fit.service_slots.append(item)

                    if item_category == 32:
                        fit.subsystems.append(item)
                    else:
                        if item_category == 18:
                            fit.drones.append(item)
                        else:
                            fit.cargo.append(item)

            elif state.section == 5:
                if fit_item:
                    if fit.drones:
                        fit.cargo.append(self._parse_cargo(fit_item))
                    else:
                        fit.drones.append(self._parse_drone(fit_item))
            elif state.section == 6:
                if fit_item:
                    fit.cargo.append(self._parse_cargo(fit_item))
            elif state.section == 7:
                if fit_item:
                    fit.fighters.append(
                        self._parse_drone(fit_item)
                    )  # Fighters use same format as drones

        return fit

    # Parsing functions to parse the EFT file into the appropriate Fit object.
    def _parse_module(self, line: str) -> Module:
        if "," in line:
            name, charge = map(str.strip, line.split(",", 1))
            return Module(name=name.strip(), charge=charge.strip())
        return Module(name=line.strip(), charge=None)

    def _parse_rig(self, line: str) -> Rig:
        return Rig(name=line.strip())

    def _parse_subsystem(self, line: str) -> Subsystem:
        return Subsystem(name=line.strip())

    def _parse_drone(self, line: str) -> Drone:
        if " x" in line:
            name, qty = line.rsplit(" x", 1)
            return Drone(name=name.strip(), quantity=int(qty.strip()))
        return Drone(name=line.strip(), quantity=1)

    def _parse_cargo(self, line: str) -> Cargo:
        if " x" in line:
            name, qty = line.rsplit(" x", 1)
            return Cargo(name=name.strip(), quantity=int(qty.strip()))

        return Cargo(name=line.strip(), quantity=1)


class EFT2Parser:
    """
    Parses an EFT2 fit file into a Fit object. This is the same as the EFTParser, but uses
    the experimental EFT2.0 format, which is essentially markdown with explicit headings for each section.
    """

    def parse(self, text: str) -> Fit:
        lines = text.strip().splitlines()

        # Check if the file is in EFT2.0 format, which conveniently doubles as markdown.
        if not lines or not lines[0].startswith("#"):
            raise ValueError("Invalid EFT2.0 format")

        ship, fit_name = lines[0].strip("# ").split(",", 1)
        fit = Fit(ship=ship, name=fit_name)

        state = ParserState()

        for line in lines[1:]:
            fit_item = state.process_line2(line)
            if not fit_item:
                continue

            # Parsing functions use explicit headings rather than position in the file
            if state.heading == "Low Slots":
                fit.low_slots.append(self._parse_module(fit_item))
            elif state.heading == "Mid Slots":
                fit.mid_slots.append(self._parse_module(fit_item))
            elif state.heading == "High Slots":
                fit.high_slots.append(self._parse_module(fit_item))
            elif state.heading == "Rigs":
                fit.rigs.append(self._parse_rig(fit_item))
            elif state.heading == "Subsystems":
                fit.subsystems.append(self._parse_subsystem(fit_item))
            elif state.heading == "Drones":
                fit.drones.append(self._parse_drone(fit_item))
            elif state.heading == "Cargo":
                fit.cargo.append(self._parse_cargo(fit_item))

        return fit

    def _parse_module(self, line: str) -> Module:
        if "," in line:
            name, charge = map(str.strip, line.split(",", 1))
            return Module(name=name.strip(), charge=charge.strip())
        return Module(name=line.strip(), charge=None)

    def _parse_rig(self, line: str) -> Rig:
        return Rig(name=line.strip())

    def _parse_subsystem(self, line: str) -> Subsystem:
        return Subsystem(name=line.strip())

    def _parse_drone(self, line: str) -> Drone:
        # we now use a comma as the separator, not a x.
        if " ," in line:
            name, qty = line.rsplit(" ,", 1)
            return Drone(name=name.strip(), quantity=int(qty.strip()))
        return Drone(name=line.strip(), quantity=1)

    def _parse_cargo(self, line: str) -> Cargo:
        if " ," in line:
            name, qty = line.rsplit(" ,", 1)
            return Cargo(name=name.strip(), quantity=int(qty.strip()))
        return Cargo(name=line.strip(), quantity=1)


class ParserState:
    """
    A class to track the state of the parser, which is used to determine which section of the fit we are parsing.
    """

    def __init__(self):
        self.section = 0
        self.in_blank_block = False
        self.blank_block_count = 0

    def process_line(self, line: str):
        line = line.strip()

        if not line:
            self.blank_block_count += 1
            if self.section < 3 and self.blank_block_count > 1:
                self.section += 1
                self.blank_block_count = 0
            if self.section == 4 and self.blank_block_count > 2:
                self.section += 1
                self.blank_block_count = 0

            if not self.in_blank_block:
                self.in_blank_block = True

        else:
            # Handle section transitions when we encounter a non-empty line after blank(s)
            if self.in_blank_block:
                self.section += 1
                self.in_blank_block = False
                self.blank_block_count = 0

            # Special case handling for items that look like cargo/drones in wrong sections. EFT does not always populate enough lines for empty sections. This serves as a failsafe.
            if self.section == 1 and (
                " x" in line
                and any(
                    word in line
                    for word in ["Missile", "Torpedo", "Bomb", "Charge", "Ammo"]
                )
            ):
                # Skip ahead to cargo if we see cargo-like items early
                self.section = 6
            elif self.section == 5 and (
                " x" in line
                and any(
                    word in line
                    for word in [
                        "Missile",
                        "Torpedo",
                        "Bomb",
                        "Charge",
                        "Ammo",
                        "Fuel",
                        "Script",
                    ]
                )
            ):
                # Move from drones to cargo
                self.section = 6

        return line

    def process_line2(self, line: str):
        """
        Process a line of EFT2.0 data.
        """
        line = line.strip()
        if not line:
            return None

        if line.startswith("## "):
            heading = line.strip("## ")
            self.heading = heading
            return None
        if self.heading:
            return line
        return None


def fit_from_eft(data: str) -> Fit:
    """
    Create a Fit object from an EFT file. This is the same as the EFTParser.parse()
    method, but is added as a convenience function and for consistency with fit_from_yaml()
    and fit_from_json().

    Args:
        data (str): The EFT data to parse

    Returns:
        Fit: A Fit object created from EFT data
    """
    parser = EFTParser()
    return parser.parse(data)


def fit_from_yaml(data: yaml.YAMLObject) -> Fit:
    """
    Create a Fit object from a YAML file.

    Args:
        data (yaml.YAMLObject): The YAML data to parse

    Returns:
        Fit: A Fit object created from the YAML data
    """
    if isinstance(data, str):
        data = yaml.load(data, Loader=yaml.loader.SafeLoader)

    fit = Fit(ship=data["ship"], name=data["name"])

    fit.low_slots = [
        Module(low_slot["name"], low_slot["charge"]) for low_slot in data["low_slots"]
    ]
    fit.mid_slots = [
        Module(mid_slot["name"], mid_slot["charge"]) for mid_slot in data["mid_slots"]
    ]
    fit.high_slots = [
        Module(high_slot["name"], high_slot["charge"])
        for high_slot in data["high_slots"]
    ]
    fit.rigs = [Rig(rig["name"]) for rig in data["rigs"]]
    fit.subsystems = [
        Module(subsystem["name"], subsystem["charge"])
        for subsystem in data["subsystems"]
    ]
    fit.drones = [Drone(drone["name"], drone["quantity"]) for drone in data["drones"]]
    fit.cargo = [Cargo(cargo["name"], cargo["quantity"]) for cargo in data["cargo"]]

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

    fit = Fit(ship=data["ship"], name=data["name"])
    fit.low_slots = [
        Module(low_slot["name"], low_slot["charge"]) for low_slot in data["low_slots"]
    ]
    fit.mid_slots = [
        Module(mid_slot["name"], mid_slot["charge"]) for mid_slot in data["mid_slots"]
    ]
    fit.high_slots = [
        Module(high_slot["name"], high_slot["charge"])
        for high_slot in data["high_slots"]
    ]
    fit.rigs = [Rig(rig["name"]) for rig in data["rigs"]]
    fit.subsystems = [
        Module(subsystem["name"], subsystem["charge"])
        for subsystem in data["subsystems"]
    ]
    fit.drones = [Drone(drone["name"], drone["quantity"]) for drone in data["drones"]]
    fit.cargo = [Cargo(cargo["name"], cargo["quantity"]) for cargo in data["cargo"]]

    return fit


def state_to_section(state: int) -> str:
    """
    Convert a ParserState object to a section number.
    """
    return {
        0: "Low Slots",
        1: "Mid Slots",
        2: "High Slots",
        3: "Rigs",
        4: "Subsystems",
        5: "Drones",
        6: "Cargo",
    }.get(state, "Unknown")


def fit_from_eft2(data: str) -> Fit:
    """
    Parse an EFT2.0 file into a Fit object. This is the same as the EFT2Parser.parse()
    method, but is added as a convenience function and for consistency with fit_from_yaml()
    and fit_from_json(). This uses the experimental EFT2.0 format, which is essentially
    markdown with explicit headings for each section.

    Args:
        data (str): The EFT2.0 data to parse

    Returns:
        Fit: A Fit object created from the EFT2.0 data
    """
    parser = EFT2Parser()
    return parser.parse(data)


if __name__ == "__main__":
    pass