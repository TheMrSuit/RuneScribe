"""
Updated Lark Transformer for imperative mystical syntax
"""
from lark import Transformer, Token
from typing import List, Optional, Any
from ast_nodes.ritual_nodes import *

class SpellTransformer(Transformer):
    """Transforms parse trees into RuneScribe AST nodes"""
    
    def __init__(self):
        super().__init__()
        self.current_operands = []  # Track operands for manifestation
    
    def start(self, children):
        """Root rule - creates SpellProgramNode"""
        return children[0]  # Return the spell_program
        
    def spell_program(self, children):
        """Transform spell program"""
        statements = [child for child in children if isinstance(child, SpellNode)]
        return SpellProgramNode(statements)
    
    def invocation(self, children):
        """INVOKE spirits x AND y FROM realm"""
        # Extract variables and realm
        variables = []
        realm = None
        
        for child in children:
            if isinstance(child, list):  # variable_list
                variables.extend(child)
            elif isinstance(child, str) and child not in ["INVOKE", "spirit", "spirits", "FROM"]:
                variables.append(child)
            elif isinstance(child, RealmType):
                realm = child
            
        return InvokeNode(variables=variables, realm=realm)
    
    def channeling(self, children):
        """CHANNEL the essence OF variable"""
        # Find the variable (last identifier)
        for child in reversed(children):
            if hasattr(child, 'type') and child.type == 'IDENTIFIER':
                variable = str(child)
                self.current_operands.append(variable)
                return ChannelNode(variable=variable)
            elif isinstance(child, str) and not child in ["CHANNEL", "the", "essence", "OF"]:
                variable = child
                self.current_operands.append(variable)
                return ChannelNode(variable=variable)
        
        raise ValueError(f"No variable found in CHANNEL statement: {children}")
    
    def weaving(self, children):
        """WEAVE WITH the force OF variable"""  
        # Find the variable
        for child in reversed(children):
            if hasattr(child, 'type') and child.type == 'IDENTIFIER':
                variable = str(child)
                self.current_operands.append(variable)
                return WeaveNode(variable=variable)
            elif isinstance(child, str) and not child in ["WEAVE", "WITH", "the", "force", "OF"]:
                variable = child
                self.current_operands.append(variable)
                return WeaveNode(variable=variable)
                
        raise ValueError(f"No variable found in WEAVE statement: {children}")
    
    def manifestation(self, children):
        """MANIFEST operation AS result_variable"""
        # Find operation and result variable
        operation = None
        result_variable = None
        
        for child in children:
            if isinstance(child, OperationType):
                operation = child
            elif hasattr(child, 'type') and child.type == 'IDENTIFIER':
                result_variable = str(child)
            elif isinstance(child, str) and child not in ["MANIFEST", "AS"]:
                # Could be variable name as string
                if not any(word in child.lower() for word in ["their", "union", "difference", "fusion", "division", "power", "essence"]):
                    result_variable = child
                
        # Use accumulated operands from CHANNEL/WEAVE
        operands = self.current_operands.copy()
        self.current_operands.clear()  # Reset for next manifestation
        
        return ManifestNode(
            operation=operation,
            operands=operands,
            result_variable=result_variable
        )
    
    def speaking(self, children):
        """SPEAK FORTH variable TO target"""
        variable = None
        target = "the void"  # default
        
        for child in children:
            if hasattr(child, 'type') and child.type == 'IDENTIFIER':
                variable = str(child)
            elif isinstance(child, str) and child not in ["SPEAK", "FORTH", "TO"]:
                if any(word in child.lower() for word in ["the", "void", "mortal", "sacred"]):
                    target = child
                else:
                    variable = child
                
        return SpeakNode(variable=variable, target=target)
    
    # Output target transformations
    def void_target(self, children):
        return "the void"
        
    def mortal_eyes_target(self, children):
        return "the mortal eyes"
        
    def sacred_scroll_target(self, children):
        return "the sacred scroll"
    
    # Operation transformations
    def union_op(self, children):
        return OperationType.UNION
        
    def difference_op(self, children):
        return OperationType.DIFFERENCE
        
    def fusion_op(self, children):
        return OperationType.FUSION
        
    def division_op(self, children):
        return OperationType.DIVISION
        
    def power_op(self, children):
        return OperationType.POWER
        
    def essence_op(self, children):
        return OperationType.ESSENCE
    
    def comparison_phrase(self, children):
        """Transform comparison phrases"""
        # Extract variables and determine operation based on phrase
        variables = [child for child in children if hasattr(child, 'type') and child.type == 'IDENTIFIER']
        phrase_words = [str(child) for child in children]
        
        if len(variables) >= 2:
            left = str(variables[0])
            right = str(variables[1])
            
            if "battle" in phrase_words:
                return ComparisonNode(left, OperationType.GREATER_THAN, right)
            elif "harmony" in phrase_words:
                return ComparisonNode(left, OperationType.LESS_THAN, right)
            elif "truth" in phrase_words:
                return ComparisonNode(left, OperationType.EQUALS, right)
            elif "conflict" in phrase_words:
                return ComparisonNode(left, OperationType.NOT_EQUALS, right)
        
        # Fallback
        return ComparisonNode("unknown", OperationType.EQUALS, "unknown")
    
    # Realm transformations
    def mortal_realm(self, children):
        return RealmType.MORTAL
        
    def spirit_realm(self, children):
        return RealmType.SPIRIT
        
    def shadow_realm(self, children):
        return RealmType.SHADOW
        
    def void_realm(self, children):
        return RealmType.VOID
        
    def astral_realm(self, children):
        return RealmType.ASTRAL
        
    def divine_realm(self, children):
        return RealmType.DIVINE
        
    def temporal_realm(self, children):
        return RealmType.TEMPORAL
    
    # Variable handling
    def variable(self, children):
        """Transform variable token"""
        return str(children[0])
        
    def variable_list(self, children):
        """Transform variable list"""
        return [str(child) for child in children if str(child) != "AND"]
    
    def conditional_ritual(self, children):
        condition = children[0]
        then_statements = []
        else_statements = None
        
        # Parse the statements (simplified)
        i = 1
        while i < len(children):
            if isinstance(children[i], SpellNode):
                then_statements.append(children[i])
            i += 1
            
        return ConditionalNode(
            condition=condition,
            then_statements=then_statements,
            else_statements=else_statements
        )
    
    def loop_ritual(self, children):
        condition = children[0] 
        body_statements = [child for child in children[1:] if isinstance(child, SpellNode)]
        
        return WhileLoopNode(
            condition=condition,
            body_statements=body_statements
        )