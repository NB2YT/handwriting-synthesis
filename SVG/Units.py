from typing import Annotated

class Millimeter:
    def __init__(self, value: str | float | int):
        # 1. If it's a string, verify the format
        if isinstance(value, str):
            if not value.endswith("mm"):
                raise ValueError("String must end with 'mm'")
            
            # Verify the part before 'mm' is a valid number
            try:
                self.value = float(value[:-2])
            except ValueError:
                raise ValueError(f"'{value[:-2]}' is not a valid number")
        
        # 2. If it's a number, convert to string + "mm"
        elif isinstance(value, (int, float)):
            self.value = value

        else:
            raise TypeError("Value must be a string (e.g., '10mm') or a number (e.g., 10)")
    
    def __str__(self):
        return f"{self.value}mm"
    
    def __repr__(self):
        return f"Millimeter({self.value}mm)"
    
    def __float__(self):
        return self.value
    
    def _determine_other_value(self, other):
        if isinstance(other, Millimeter):
            return other.value
        elif isinstance(other, (int, float)):
            return other
        else:
            raise TypeError("Unsupported type for running math operations with Millimeter")
    
    def __add__(self, other):
        return Millimeter(self.value + self._determine_other_value(other))
    
    def __sub__(self, other):
        return Millimeter(self.value - self._determine_other_value(other))
    
    def __truediv__(self, other):
        return Millimeter(self.value / self._determine_other_value(other))
    
    def __mul__(self, other):
        return Millimeter(self.value * self._determine_other_value(other))

def px_to_mm(px: float) -> Millimeter:
    dpi = 96 # standard screen DPI
    return Millimeter(px * 25.4 / dpi)

def assert_px_to_mm(str: str) -> Millimeter:
    try:
        value = float(str)
        return px_to_mm(value)
    except ValueError:
        return Millimeter(str)