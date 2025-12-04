"""
Variable Storage System for RuneScribe
Manages spirits and their essences across mystical realms
"""
from typing import Any, Dict, Optional
from ast_nodes.ritual_nodes import RealmType, RealmTypeInference

class SpiritRealm:
    """Storage and management of summoned spirits (variables)"""
    
    def __init__(self):
        """Initialize the spirit realm"""
        self.spirits: Dict[str, Any] = {}  # spirit_name -> value
        self.spirit_realms: Dict[str, RealmType] = {}  # spirit_name -> realm
        self.spirit_types: Dict[str, str] = {}  # spirit_name -> inferred_type
    
    def summon_spirit(self, name: str, raw_value: str, realm: RealmType) -> None:
        """Summon a spirit with a value from the specified realm"""
        # Convert raw input to appropriate type based on realm
        typed_value = self._convert_by_realm(raw_value, realm)
        
        self.spirits[name] = typed_value
        self.spirit_realms[name] = realm
        self.spirit_types[name] = self._infer_type(raw_value, realm)
    
    def get_spirit_essence(self, name: str) -> Any:
        """Retrieve the essence (value) of a summoned spirit"""
        if name not in self.spirits:
            raise ValueError(f"Spirit '{name}' has not been summoned. Use INVOKE first.")
        return self.spirits[name]
    
    def get_spirit_realm(self, name: str) -> RealmType:
        """Get the realm of a summoned spirit"""
        if name not in self.spirit_realms:
            raise ValueError(f"Spirit '{name}' has not been summoned.")
        return self.spirit_realms[name]
    
    def get_spirit_type(self, name: str) -> str:
        """Get the inferred type of a summoned spirit"""
        return self.spirit_types.get(name, "unknown")
    
    def has_spirit(self, name: str) -> bool:
        """Check if a spirit has been summoned"""
        return name in self.spirits
    
    def bind_manifestation(self, name: str, value: Any, realm: RealmType) -> None:
        """Bind the result of a manifestation as a new spirit"""
        self.spirits[name] = value
        self.spirit_realms[name] = realm
        self.spirit_types[name] = type(value).__name__
    
    def _convert_by_realm(self, raw_value: str, realm: RealmType) -> Any:
        """Convert raw string input to appropriate type based on realm"""
        try:
            if realm == RealmType.MORTAL:
                return self._convert_mortal(raw_value)
            elif realm == RealmType.SPIRIT:
                return self._convert_spirit(raw_value)
            elif realm == RealmType.SHADOW:
                return self._convert_shadow(raw_value)
            elif realm == RealmType.VOID:
                return None if raw_value.lower() in ['null', 'none', 'void', ''] else raw_value
            elif realm == RealmType.ASTRAL:
                # Try to parse as list/array
                if raw_value.startswith('[') and raw_value.endswith(']'):
                    return eval(raw_value)  # Simple eval for now
                return raw_value.split(',') if ',' in raw_value else [raw_value]
            elif realm == RealmType.DIVINE:
                # Try to parse as dict/object (simplified)
                if raw_value.startswith('{') and raw_value.endswith('}'):
                    return eval(raw_value)  # Simple eval for now
                return {"value": raw_value}
            elif realm == RealmType.TEMPORAL:
                # Basic date/time parsing
                from datetime import datetime
                try:
                    return datetime.fromisoformat(raw_value)
                except:
                    return raw_value
            else:
                return raw_value
        except Exception:
            # Fallback to string if conversion fails
            return raw_value
    
    def _convert_mortal(self, value: str) -> Any:
        """Convert to mortal realm types (int, char)"""
        # Try int first
        try:
            return int(value)
        except ValueError:
            pass
        
        # Single character -> char
        if len(value) == 1:
            return value
        
        # Fallback to string
        return value
    
    def _convert_spirit(self, value: str) -> Any:
        """Convert to spirit plane types (double, long, string)"""
        # Try float (double)
        try:
            if '.' in value:
                return float(value)
        except ValueError:
            pass
        
        # Try int/long
        try:
            num = int(value)
            if abs(num) > 2**31:
                return num  # Python handles big ints automatically
            return num
        except ValueError:
            pass
        
        # String
        return value
    
    def _convert_shadow(self, value: str) -> Any:
        """Convert to shadow dimension types (bool, binary)"""
        lower_val = value.lower()
        
        # Boolean conversion
        if lower_val in ['true', 'yes', 'light', '1', 'on']:
            return True
        elif lower_val in ['false', 'no', 'dark', '0', 'off']:
            return False
        
        # Binary conversion
        if all(c in '01' for c in value):
            return int(value, 2)
        
        # Fallback to boolean interpretation
        return bool(value)
    
    def _infer_type(self, raw_value: str, realm: RealmType) -> str:
        """Infer the specific type based on realm and value"""
        if realm == RealmType.MORTAL:
            return RealmTypeInference.infer_mortal_type(raw_value)
        elif realm == RealmType.SPIRIT:
            return RealmTypeInference.infer_spirit_type(raw_value)
        elif realm == RealmType.SHADOW:
            return RealmTypeInference.infer_shadow_type(raw_value)
        else:
            return realm.value
    
    def get_realm_status(self) -> str:
        """Get a status report of all spirits in the realm"""
        if not self.spirits:
            return "The spirit realm is empty. No spirits have been summoned."
        
        status_lines = ["=== SPIRIT REALM STATUS ==="]
        for name, value in self.spirits.items():
            realm = self.spirit_realms[name]
            spirit_type = self.spirit_types[name]
            status_lines.append(f"  {name}: {value} ({spirit_type} from {realm.value} realm)")
        
        return "\n".join(status_lines)