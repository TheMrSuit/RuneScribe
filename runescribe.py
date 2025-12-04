#!/usr/bin/env python3
"""
RuneScribe - A Ritualistic Programming Language
Main entry point for parsing and executing .spell files
"""

import sys
import argparse
from pathlib import Path
from parser.spell_parser import SpellParser

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="RuneScribe - Parse and execute ritualistic spell files"
    )
    parser.add_argument(
        "file", 
        nargs='?', 
        help="Path to .spell file to parse"
    )
    parser.add_argument(
        "-i", "--interactive", 
        action="store_true",
        help="Start interactive parsing mode"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true", 
        help="Enable verbose output"
    )
    parser.add_argument(
        "-e", "--execute",
        action="store_true",
        help="Execute the spell after parsing"
    )
    parser.add_argument(
        "--no-mystical",
        action="store_true",
        help="Disable mystical output mode (technical mode)"
    )
    
    args = parser.parse_args()
    
    # Initialize parser
    spell_parser = SpellParser()
    
    if args.interactive:
        # Interactive mode
        ast = spell_parser.parse_interactive()
        if ast:
            print(f"\nParsed AST: {ast}")
            
    elif args.file:
        # Parse file
        file_path = Path(args.file)
        
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
            
        if not args.file.endswith('.spell'):
            print(f"Warning: File '{args.file}' does not have .spell extension")
            
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            ast, type_info = spell_parser.parse_with_types(content, args.file)
            
            if args.verbose:
                print(f"Successfully parsed {args.file}")
                print(f"AST: {ast}")
                
                print("\nStatements:")
                for i, stmt in enumerate(ast.statements):
                    print(f"  {i+1}. {stmt}")
                    
                print("\nType Information:")
                for var, info in type_info.items():
                    print(f"  {var}: realm={info['realm'].value}, types={info['possible_types']}")
            else:
                print("Parse successful!")
            
            # Execute the spell if requested
            if args.execute:
                from interpreter.spell_interpreter import SpellInterpreter
                
                mystical_mode = not args.no_mystical
                interpreter = SpellInterpreter(mystical_mode=mystical_mode)
                
                if args.verbose and mystical_mode:
                    print("\n" + "="*50)
                    print("PREPARING TO EXECUTE SPELL...")
                    print("="*50)
                
                interpreter.execute_spell_program(ast)
                
                if args.verbose:
                    print("\n" + interpreter.get_spirit_realm_status())
                
        except Exception as e:
            print(f"Error parsing {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
            
    else:
        # No arguments - show help
        parser.print_help()

if __name__ == "__main__":
    main()