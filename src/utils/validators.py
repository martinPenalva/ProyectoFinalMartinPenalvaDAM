"""
Utilidades para validación de datos
"""

import re
from datetime import datetime
from typing import Optional, Tuple


class Validator:
    """Clase con métodos de validación"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_dni_nie(identifier: str) -> bool:
        """Valida formato de DNI/NIE español"""
        # DNI: 8 dígitos + letra
        # NIE: X/Y/Z + 7 dígitos + letra
        pattern = r'^[0-9]{8}[A-Z]$|^[XYZ][0-9]{7}[A-Z]$'
        return bool(re.match(pattern, identifier.upper()))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Valida formato de teléfono (9 dígitos)"""
        # Eliminar espacios y guiones
        phone_clean = phone.replace(' ', '').replace('-', '')
        return phone_clean.isdigit() and len(phone_clean) == 9
    
    @staticmethod
    def validate_datetime_range(start: datetime, end: datetime) -> Tuple[bool, Optional[str]]:
        """Valida que la fecha de fin sea posterior a la de inicio"""
        if end <= start:
            return False, "La fecha de fin debe ser posterior a la fecha de inicio"
        return True, None
    
    @staticmethod
    def validate_capacity(capacity: int) -> Tuple[bool, Optional[str]]:
        """Valida que la capacidad sea un número positivo"""
        if capacity <= 0:
            return False, "La capacidad debe ser mayor que 0"
        if capacity > 10000:
            return False, "La capacidad no puede ser mayor a 10000"
        return True, None
    
    @staticmethod
    def validate_required_field(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """Valida que un campo obligatorio no esté vacío"""
        if not value or not value.strip():
            return False, f"El campo '{field_name}' es obligatorio"
        return True, None

