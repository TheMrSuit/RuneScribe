"""
Updated AST Node definitions for RuneScribe imperative mystical language
with realm-based type system
"""
from abc import ABC
from typing import List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

class RealmType(Enum):
    """Mystical realms that determine data types"""
    MORTAL = "mortal"      # int, char  
    SPIRIT = "spirit"      # double, long, string
    SHADOW = "shadow"      # bool, binary
    VOID = "void"          # null, undefined
    ASTRAL = "astral"      # arrays, lists
    DIVINE = "divine"      # objects, structs  
    TEMPORAL = "temporal"  # dates, times

class OperationType(Enum):
    """Mystical operations"""
    UNION = "union"           # addition
    DIFFERENCE = "difference" # subtraction
    FUSION = "fusion"         # multiplication
    DIVISION = "division"     # division
    POWER = "power"          # exponentiation
    ESSENCE = "essence"      # identity/no-op
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than" 
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"

class SpellNode(ABC):
    """Base class for all RuneScribe AST nodes"""
    pass

@dataclass
class InvokeNode(SpellNode):
    """INVOKE spirits x AND y FROM the mortal realm"""
    variables: List[str]
    realm: RealmType
    
    def __str__(self):
        vars_str = " AND ".join(self.variables)
        return f"Invoke({vars_str} from {self.realm.value} realm)"

@dataclass
class ChannelNode(SpellNode):
    """CHANNEL the essence OF variable"""
    variable: str
    
    def __str__(self):
        return f"Channel({self.variable})"

@dataclass
class WeaveNode(SpellNode):
    """WEAVE WITH the force OF variable"""
    variable: str
    
    def __str__(self):
        return f"Weave({self.variable})"

@dataclass
class ManifestNode(SpellNode):
    """MANIFEST their union AS result"""
    operation: OperationType
    operands: List[str]  # Variables involved in operation
    result_variable: str
    
    def __str__(self):
        op_str = " and ".join(self.operands)
        return f"Manifest({self.operation.value} of {op_str} -> {self.result_variable})"

@dataclass
class SpeakNode(SpellNode):
    """SPEAK FORTH variable TO target"""
    variable: str
    target: str
    
    def __str__(self):
        return f"Speak({self.variable} to {self.target})"

@dataclass
class ConditionalNode(SpellNode):
    """IF the spirits decree condition THEN ... ELSEWISE ..."""
    condition: Union['ComparisonNode', str]
    then_statements: List[SpellNode]
    else_statements: Optional[List[SpellNode]] = None
    
    def __str__(self):
        return f"Conditional({self.condition} -> {len(self.then_statements)} statements)"

@dataclass
class WhileLoopNode(SpellNode):
    """WHILE the essence flows AND condition"""
    condition: Union['ComparisonNode', str]
    body_statements: List[SpellNode]
    
    def __str__(self):
        return f"WhileLoop({self.condition} -> {len(self.body_statements)} statements)"

@dataclass
class ComparisonNode(SpellNode):
    """Comparison operations between variables"""
    left: str
    operation: OperationType
    right: str
    
    def __str__(self):
        return f"Compare({self.left} {self.operation.value} {self.right})"

@dataclass
class SpellProgramNode(SpellNode):
    """Root node containing the entire spell program"""
    statements: List[SpellNode]
    
    def __str__(self):
        return f"SpellProgram({len(self.statements)} statements)"

# Type inference utilities
class RealmTypeInference:
    """Utilities for inferring types based on realm and value"""
    
    @staticmethod
    def infer_mortal_type(value: str) -> str:
        """Infer int or char from mortal realm"""
        try:
            int(value)
            return "int"
        except ValueError:
            if len(value) == 1:
                return "char"
            return "string"  # fallback
    
    @staticmethod  
    def infer_spirit_type(value: str) -> str:
        """Infer double, long, or string from spirit plane"""
        try:
            if '.' in value:
                float(value)
                return "double"
            else:
                val = int(value)
                if abs(val) > 2**31:
                    return "long"
                return "int"  # Could be promoted to long if needed
        except ValueError:
            return "string"
    
    @staticmethod
    def infer_shadow_type(value: str) -> str:
        """Infer bool or binary from shadow dimension"""
        if value.lower() in ["true", "false", "yes", "no", "light", "dark"]:
            return "bool"
        if all(c in "01" for c in value):
            return "binary"
        return "bool"  # fallback
    
    @staticmethod
    def get_realm_types(realm: RealmType) -> List[str]:
        """Get possible types for a realm"""
        realm_map = {
            RealmType.MORTAL: ["int", "char"],
            RealmType.SPIRIT: ["double", "long", "string"],
            RealmType.SHADOW: ["bool", "binary"],
            RealmType.VOID: ["null", "undefined"], 
            RealmType.ASTRAL: ["array", "list"],
            RealmType.DIVINE: ["object", "struct"],
            RealmType.TEMPORAL: ["date", "time", "datetime"]
        }
        return realm_map.get(realm, ["unknown"])