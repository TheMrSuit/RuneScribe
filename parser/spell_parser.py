"""
Updated RuneScribe Parser with realm-based type inference
"""
import os
from pathlib import Path
from lark import Lark, LarkError
from .ast_transformer import SpellTransformer
from ast_nodes.ritual_nodes import SpellProgramNode, InvokeNode, RealmTypeInference

class SpellParser:
    """Main parser class for RuneScribe .spell files"""
    
    def __init__(self):
        """Initialize the Lark parser with grammar"""
        # Load grammar file
        grammar_path = Path(__file__).parent / "spell_grammar.lark"
        
        if not grammar_path.exists():
            raise FileNotFoundError(f"Grammar file not found: {grammar_path}")
            
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar = f.read()
            
        # Initialize Lark parser
        self.parser = Lark(
            grammar,
            start='start',
            parser='lalr',  # Fast LALR(1) parser
            lexer='contextual',  # Handle context-sensitive tokens
            transformer=SpellTransformer(),
            debug=True  # Enable for development
        )
    
    def parse_file(self, filepath: str) -> SpellProgramNode:
        """Parse a .spell file and return AST"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_text(content, filepath)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Spell file not found: {filepath}")
        except Exception as e:
            raise RuntimeError(f"Error reading spell file {filepath}: {e}")
    
    def parse_text(self, text: str, source_name: str = "<string>") -> SpellProgramNode:
        """Parse spell text and return AST"""
        try:
            # Parse with Lark and transform to AST
            ast = self.parser.parse(text)
            return ast
            
        except LarkError as e:
            # Convert Lark errors to more readable format
            # TODO: Add mystical error message option later
            raise SyntaxError(f"Parse error in {source_name}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error parsing {source_name}: {e}")
    
    def parse_with_types(self, text: str, source_name: str = "<string>") -> tuple:
        """Parse spell text and return AST with type information"""
        try:
            ast = self.parser.parse(text)
            
            # Perform type inference
            type_info = self._infer_types(ast)
            
            return ast, type_info
            
        except Exception as e:
            raise RuntimeError(f"Error parsing {source_name}: {e}")
    
    def _infer_types(self, ast: SpellProgramNode) -> dict:
        """Infer types for all variables based on realm context"""
        type_info = {}
        
        for statement in ast.statements:
            if isinstance(statement, InvokeNode):
                # Assign realm-based types to variables
                for var in statement.variables:
                    type_info[var] = {
                        'realm': statement.realm,
                        'possible_types': RealmTypeInference.get_realm_types(statement.realm),
                        'inferred_type': None  # Will be set when value is assigned
                    }
        
        return type_info
    
    def parse_interactive(self, prompt: str = "spell> ") -> SpellProgramNode:
        """Interactive parsing for REPL-style usage"""
        print("RuneScribe Interactive Parser")
        print("Enter your spell (Ctrl+C to exit):")
        
        try:
            lines = []
            while True:
                try:
                    line = input(prompt)
                    if line.strip() == "":
                        # Empty line - try to parse accumulated input
                        if lines:
                            text = "\n".join(lines)
                            return self.parse_text(text, "<interactive>")
                    else:
                        lines.append(line)
                        
                except EOFError:
                    if lines:
                        text = "\n".join(lines)
                        return self.parse_text(text, "<interactive>")
                    break
                    
        except KeyboardInterrupt:
            print("\nSpell casting interrupted.")
            return None

# Example usage function
def main():
    """Example usage showing the new syntax"""
    parser = SpellParser()
    
    # Your example spell
    example_spell = """
INVOKE spirits x AND y FROM the mortal realm
CHANNEL the essence OF x
WEAVE WITH the force OF y  
MANIFEST their union AS result
SPEAK FORTH result TO the void
"""
    
    try:
        ast, type_info = parser.parse_with_types(example_spell)
        print("Parse successful!")
        print(f"AST: {ast}")
        
        print("\nStatements:")
        for i, stmt in enumerate(ast.statements):
            print(f"  {i+1}. {stmt}")
            
        print("\nType Information:")
        for var, info in type_info.items():
            print(f"  {var}: realm={info['realm'].value}, types={info['possible_types']}")
            
    except Exception as e:
        print(f"Parse error: {e}")

if __name__ == "__main__":
    main()