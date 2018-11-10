from dataclasses import dataclass

@dataclass
class Import:
    source: str
    destination: str

@dataclass
class Select:
    columns: [str]
    source: str
    condition: (str, str)
    destination: str

@dataclass
class Print:
    source: str
