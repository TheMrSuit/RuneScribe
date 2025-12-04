"""
Main RuneScribe Interpreter
Executes mystical spells with proper ceremony and power
"""
import sys
from typing import Any, Dict, List, Optional
from ast_nodes.ritual_nodes import *
from .variable_storage import SpiritRealm
from .execution_engine import MysticalExecutor
from .io_handler import MysticalIO

class SpellInterpreter:
    """Main interpreter for executing RuneScribe spells"""
    
    def __init__(self, mystical_mode: bool = True):
        """Initialize the spell interpreter"""
        self.spirit_realm = SpiritRealm()
        self.executor = MysticalExecutor()
        self.io_handler = MysticalIO(mystical_mode)
        self.mystical_mode = mystical_mode
        
    def execute_spell_program(self, program: SpellProgramNode) -> None:
        """Execute a complete spell program"""
        if self.mystical_mode:
            self.io_handler.announce_ritual_beginning()
            
        try:
            for statement in program.statements:
                self.execute_statement(statement)
                
            if self.mystical_mode:
                self.io_handler.announce_ritual_completion()
                
        except Exception as e:
            if self.mystical_mode:
                self.io_handler.announce_ritual_failure(str(e))
            else:
                print(f"Execution error: {e}")
            raise
    
    def execute_statement(self, statement: SpellNode) -> None:
        """Execute a single statement"""
        if isinstance(statement, InvokeNode):
            self._execute_invocation(statement)
        elif isinstance(statement, ChannelNode):
            self._execute_channeling(statement)
        elif isinstance(statement, WeaveNode):
            self._execute_weaving(statement)
        elif isinstance(statement, ManifestNode):
            self._execute_manifestation(statement)
        elif isinstance(statement, SpeakNode):
            self._execute_speaking(statement)
        else:
            raise ValueError(f"Unknown statement type: {type(statement)}")
    
    def _execute_invocation(self, invocation: InvokeNode) -> None:
        """Execute INVOKE - summon spirits (get input values)"""
        for variable in invocation.variables:
            if self.mystical_mode:
                prompt = self.io_handler.get_invocation_prompt(variable, invocation.realm)
            else:
                prompt = f"Enter value for {variable} ({invocation.realm.value} realm): "
                
            raw_value = input(prompt)
            
            # Store the spirit with realm-based type inference
            self.spirit_realm.summon_spirit(
                variable, 
                raw_value, 
                invocation.realm
            )
            
            if self.mystical_mode:
                self.io_handler.announce_spirit_summoned(variable, invocation.realm)
    
    def _execute_channeling(self, channeling: ChannelNode) -> None:
        """Execute CHANNEL - prepare variable for use"""
        value = self.spirit_realm.get_spirit_essence(channeling.variable)
        self.executor.channel_essence(channeling.variable, value)
        
        if self.mystical_mode:
            self.io_handler.announce_essence_channeled(channeling.variable)
    
    def _execute_weaving(self, weaving: WeaveNode) -> None:
        """Execute WEAVE - prepare second variable for operation"""
        value = self.spirit_realm.get_spirit_essence(weaving.variable)
        self.executor.weave_force(weaving.variable, value)
        
        if self.mystical_mode:
            self.io_handler.announce_force_woven(weaving.variable)
    
    def _execute_manifestation(self, manifestation: ManifestNode) -> None:
        """Execute MANIFEST - perform the mystical operation"""
        result = self.executor.manifest_union(
            manifestation.operation,
            manifestation.operands
        )
        
        # Determine result realm based on operand realms
        result_realm = self._infer_result_realm(manifestation.operands)
        
        # Store the result
        self.spirit_realm.bind_manifestation(
            manifestation.result_variable,
            result,
            result_realm
        )
        
        if self.mystical_mode:
            self.io_handler.announce_manifestation(
                manifestation.operation,
                manifestation.result_variable,
                result
            )
    
    def _execute_speaking(self, speaking: SpeakNode) -> None:
        """Execute SPEAK FORTH - output the result"""
        value = self.spirit_realm.get_spirit_essence(speaking.variable)
        
        if self.mystical_mode:
            self.io_handler.speak_to_realm(speaking.variable, value, speaking.target)
        else:
            target_desc = speaking.target.replace("the ", "")
            print(f"[{target_desc}] {speaking.variable}: {value}")
    
    def _infer_result_realm(self, operands: List[str]) -> RealmType:
        """Infer the realm type for operation results"""
        realms = []
        for operand in operands:
            if self.spirit_realm.has_spirit(operand):
                realms.append(self.spirit_realm.get_spirit_realm(operand))
        
        if not realms:
            return RealmType.MORTAL
        
        # Promotion rules: spirit > mortal, shadow for booleans
        if RealmType.SPIRIT in realms:
            return RealmType.SPIRIT
        elif RealmType.SHADOW in realms:
            return RealmType.SHADOW
        else:
            return RealmType.MORTAL
    
    def get_spirit_realm_status(self) -> str:
        """Get status of all summoned spirits"""
        return self.spirit_realm.get_realm_status()