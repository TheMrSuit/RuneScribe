"""
Mystical I/O Handler for RuneScribe
Provides ceremonial and atmospheric interaction with the user
"""
from typing import Any
from ast_nodes.ritual_nodes import RealmType, OperationType

class MysticalIO:
    """Handles input/output with mystical flair and ceremony"""
    
    def __init__(self, mystical_mode: bool = True):
        """Initialize the mystical I/O handler"""
        self.mystical_mode = mystical_mode
        self.realm_descriptions = {
            RealmType.MORTAL: "numbers and symbols of the earthly plane",
            RealmType.SPIRIT: "ethereal essences that flow between dimensions",
            RealmType.SHADOW: "truths and falsehoods from the realm of duality",
            RealmType.VOID: "emptiness and the absence of being",
            RealmType.ASTRAL: "collections that drift through cosmic winds",
            RealmType.DIVINE: "sacred structures blessed by higher powers",
            RealmType.TEMPORAL: "moments captured in the flow of time"
        }
        
        self.operation_descriptions = {
            OperationType.UNION: "united in harmonious addition",
            OperationType.DIFFERENCE: "separated by mystical subtraction",
            OperationType.FUSION: "fused through multiplicative magic",
            OperationType.DIVISION: "divided by the ancient arts",
            OperationType.POWER: "raised to transcendent heights",
            OperationType.ESSENCE: "distilled to its purest form"
        }
    
    def announce_ritual_beginning(self) -> None:
        """Announce the beginning of a ritual"""
        if self.mystical_mode:
            print("\n" + "="*60)
            print("THE MYSTICAL RITUAL BEGINS")
            print("The ancient powers stir... Reality bends to your will...")
            print("="*60 + "\n")
    
    def announce_ritual_completion(self) -> None:
        """Announce successful completion of a ritual"""
        if self.mystical_mode:
            print("\n" + "="*60)
            print("THE RITUAL IS COMPLETE")
            print("The spell has been cast successfully!")
            print("The spirits return to their realms, their task fulfilled.")
            print("="*60 + "\n")
    
    def announce_ritual_failure(self, error: str) -> None:
        """Announce ritual failure with mystical flair"""
        if self.mystical_mode:
            print("\n" + "="*60)
            print("THE RITUAL HAS FAILED!")
            print(f"The mystical forces rebel: {error}")
            print("The spell dissipates into the ether...")
            print("="*60 + "\n")
    
    def get_invocation_prompt(self, spirit_name: str, realm: RealmType) -> str:
        """Get a mystical prompt for spirit invocation"""
        if self.mystical_mode:
            realm_desc = self.realm_descriptions.get(realm, "an unknown realm")
            return f"\nTo summon the spirit '{spirit_name}' from {realm_desc},\n   speak its essence into being: "
        else:
            return f"Enter value for {spirit_name} ({realm.value} realm): "
    
    def announce_spirit_summoned(self, spirit_name: str, realm: RealmType) -> None:
        """Announce successful spirit summoning"""
        if self.mystical_mode:
            print(f"The spirit '{spirit_name}' materializes from the {realm.value} realm!")
    
    def announce_essence_channeled(self, variable: str) -> None:
        """Announce essence channeling"""
        if self.mystical_mode:
            print(f"Channeling the mystical essence of '{variable}'...")
    
    def announce_force_woven(self, variable: str) -> None:
        """Announce force weaving"""
        if self.mystical_mode:
            print(f"Weaving the cosmic force of '{variable}' into the spell matrix...")
    
    def announce_manifestation(self, operation: OperationType, result_var: str, result: Any) -> None:
        """Announce the manifestation of an operation"""
        if self.mystical_mode:
            op_desc = self.operation_descriptions.get(operation, "transformed by unknown magic")
            print(f"The essences are {op_desc}!")
            print(f"The result manifests as '{result_var}': {result}")
    
    def speak_to_realm(self, variable: str, value: Any, target: str) -> None:
        """Speak the result to the specified realm"""
        if self.mystical_mode:
            target_desc = self._get_target_description(target)
            print(f"\nSpeaking to {target_desc}:")
            print(f"   {variable} reveals its essence: {value}")
        else:
            print(f"[{target}] {variable}: {value}")
    
    def _get_target_description(self, target: str) -> str:
        """Get mystical description for output targets"""
        target_map = {
            "the void": "the infinite void that echoes through eternity",
            "the mortal eyes": "those who walk the earthly plane", 
            "the sacred scroll": "the ancient parchments of knowledge"
        }
        return target_map.get(target, target)
    
    def display_debug_info(self, message: str) -> None:
        """Display debug information"""
        if not self.mystical_mode:
            print(f"[DEBUG] {message}")
    
    def get_realm_prompt(self, available_realms: list) -> str:
        """Get prompt for realm selection"""
        if self.mystical_mode:
            realm_list = "\n".join([f"  {realm.value} - {self.realm_descriptions[realm]}" 
                                   for realm in available_realms])
            return f"\nChoose the mystical realm:\n{realm_list}\nRealm: "
        else:
            realm_names = [realm.value for realm in available_realms]
            return f"Choose realm ({', '.join(realm_names)}): "