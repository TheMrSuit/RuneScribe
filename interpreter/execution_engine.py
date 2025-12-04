"""
Execution Engine for RuneScribe Mystical Operations
Performs the actual computational magic behind the spells
"""
from typing import Any, Dict, List
from ast_nodes.ritual_nodes import OperationType

class MysticalExecutor:
    """Executes mystical operations with proper magical ceremony"""
    
    def __init__(self):
        """Initialize the mystical executor"""
        self.channeled_essence = None  # Current channeled value
        self.woven_force = None       # Current woven value
        self.operation_history: List[str] = []  # Track operations for debugging
    
    def channel_essence(self, variable: str, value: Any) -> None:
        """Channel the essence of a spirit for use in operations"""
        self.channeled_essence = value
        self.operation_history.append(f"Channeled essence of {variable}: {value}")
    
    def weave_force(self, variable: str, value: Any) -> None:
        """Weave the force of a spirit with the channeled essence"""
        self.woven_force = value
        self.operation_history.append(f"Woven force of {variable}: {value}")
    
    def manifest_union(self, operation: OperationType, operands: List[str]) -> Any:
        """Manifest the result of a mystical operation"""
        # For essence operations, we only need channeled essence
        if operation == OperationType.ESSENCE:
            if self.channeled_essence is None:
                raise ValueError("Cannot manifest essence without channeled essence")
        else:
            # Other operations need both operands
            if self.channeled_essence is None or self.woven_force is None:
                raise ValueError("Cannot manifest without both channeled essence and woven force")
        
        left = self.channeled_essence
        right = self.woven_force
        
        try:
            if operation == OperationType.UNION:
                result = self._perform_union(left, right)
            elif operation == OperationType.DIFFERENCE:
                result = self._perform_difference(left, right)
            elif operation == OperationType.FUSION:
                result = self._perform_fusion(left, right)
            elif operation == OperationType.DIVISION:
                result = self._perform_division(left, right)
            elif operation == OperationType.POWER:
                result = self._perform_power(left, right)
            elif operation == OperationType.ESSENCE:
                result = self._perform_essence(left)  # Only need left operand
            else:
                raise ValueError(f"Unknown mystical operation: {operation}")
            
            self.operation_history.append(
                f"Manifested {operation.value}: {left} ⚡ {right} = {result}"
            )
            
            # Clear the channeled values for next operation
            self.channeled_essence = None
            self.woven_force = None
            
            return result
            
        except Exception as e:
            raise ValueError(f"Mystical operation failed: {e}")
    
    def _perform_union(self, left: Any, right: Any) -> Any:
        """Perform mystical union (addition)"""
        # Handle different type combinations
        if isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        elif isinstance(left, bool) or isinstance(right, bool):
            return left or right  # Logical OR for booleans
        elif isinstance(left, list) and isinstance(right, list):
            return left + right
        else:
            # Try numeric addition, fallback to concatenation
            try:
                return left + right
            except:
                return str(left) + str(right)
    
    def _perform_difference(self, left: Any, right: Any) -> Any:
        """Perform mystical difference (subtraction)"""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        elif isinstance(left, bool) and isinstance(right, bool):
            return left and not right  # Logical difference
        elif isinstance(left, str) and isinstance(right, str):
            return left.replace(right, "")  # String difference
        else:
            # Try numeric subtraction
            return float(left) - float(right)
    
    def _perform_fusion(self, left: Any, right: Any) -> Any:
        """Perform mystical fusion (multiplication)"""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        elif isinstance(left, str) and isinstance(right, int):
            return left * right  # String repetition
        elif isinstance(left, bool) and isinstance(right, bool):
            return left and right  # Logical AND
        elif isinstance(left, list) and isinstance(right, int):
            return left * right  # List repetition
        else:
            # Try numeric multiplication
            return float(left) * float(right)
    
    def _perform_division(self, left: Any, right: Any) -> Any:
        """Perform mystical division"""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if right == 0:
                raise ValueError("Cannot divide by zero - the void consumes all!")
            return left / right
        else:
            # Try numeric division
            right_num = float(right)
            if right_num == 0:
                raise ValueError("Cannot divide by zero - the void consumes all!")
            return float(left) / right_num
    
    def _perform_power(self, left: Any, right: Any) -> Any:
        """Perform mystical power (exponentiation)"""
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left ** right
        else:
            # Try numeric exponentiation
            return float(left) ** float(right)
    
    def _perform_essence(self, left: Any, right: Any = None) -> Any:
        """Perform essence extraction (identity/no-op, returns left)"""
        return left
    
    def get_operation_history(self) -> List[str]:
        """Get the history of performed operations"""
        return self.operation_history.copy()
    
    def clear_history(self) -> None:
        """Clear the operation history"""
        self.operation_history.clear()