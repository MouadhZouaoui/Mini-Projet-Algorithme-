#!/usr/bin/env python3
"""
Arabic Morphological Engine - Complete CLI Application

This application demonstrates:
1. AVL Tree for Arabic roots storage
2. Hash Table for morphological patterns
3. Morphological engine for word generation/validation
4. Complete CLI interface with rich formatting

Author: [Zouaoui Mouadh]
"""

import json
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.prompt import Prompt, Confirm
from rich import print as rprint

# Import our modules
from avl_tree import AVLTree
from hash_table import HashTable
from arabic_utils import ArabicUtils
from morphology import MorphologicalEngine

console = Console()

class ArabicMorphologyCLI:
    """Command Line Interface for Arabic Morphological Engine."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.engine = MorphologicalEngine()
        self.running = True
        
    def load_data_files(self) -> bool:
        """Load data from files (roots.txt and patterns.json)."""
        try:
            # Load roots
            with open("../data/roots.txt", "r", encoding="utf-8") as f:
                roots = [line.strip() for line in f if line.strip()]
                self.engine.load_roots(roots)
            
            # Load patterns
            with open("../data/patterns.json", "r", encoding="utf-8") as f:
                patterns = json.load(f)
                self.engine.load_patterns(patterns)
            
            return True
            
        except FileNotFoundError as e:
            console.print(f"[red]Error: {e}[/red]")
            console.print("[yellow]Please ensure data/roots.txt and data/patterns.json exist.[/yellow]")
            return False
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing JSON: {e}[/red]")
            return False
    
    def display_welcome(self):
        """Display welcome banner."""
        welcome_text = """
        [bold cyan]🌙 Arabic Morphological Engine 🌙[/bold cyan]
        
        [bold]Features:[/bold]
        • AVL Tree for Arabic roots (O(log n) search)
        • Hash Table for morphological patterns (O(1) access)
        • Word generation from roots and patterns
        • Word validation and pattern recognition
        • Professional CLI with rich formatting
        
        [bold]Academic Project:[/bold] Zouaoui Mouadh - Algorithmique 2026
        """
        
        console.print(Panel.fit(
            welcome_text,
            title="Welcome",
            border_style="cyan",
            padding=(1, 2)
        ))
    
    def display_menu(self):
        """Display main menu."""
        menu_options = [
            ("1", "📥 Load/Reload Data", "Load roots and patterns from files"),
            ("2", "🔍 Search Root", "Check if a root exists in AVL tree"),
            ("3", "🏗️ Generate Word", "Generate word from root and pattern"),
            ("4", "🎭 Generate All", "Generate all words for a root"),
            ("5", "✅ Validate Word", "Check if word belongs to a root"),
            ("6", "🗑️ Manage Derivatives", "Add/Remove derivatives menu"),
            ("7", "📊 Display Statistics", "Show engine statistics"),
            ("8", "🌳 Tree Operations", "AVL tree operations menu"),
            ("9", "📁 Hash Table Info", "Hash table operations menu"),
            ("10", "💾 Export Results", "Export generated words"),
            ("0", "🚪 Exit", "Exit the application")
        ]
        
        console.print("\n[bold cyan]Main Menu[/bold cyan]")
        console.print("=" * 60)
        
        table = Table(show_header=False, box=None)
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Action", style="green")
        table.add_column("Description", style="yellow")
        
        for opt, action, desc in menu_options:
            table.add_row(f"[bold]{opt}[/bold]", action, desc)
        
        console.print(table)
        console.print("=" * 60)
    
    def handle_choice(self, choice: str):
        """Handle user menu choice."""
        if choice == "1":
            self.load_data()
        elif choice == "2":
            self.search_root()
        elif choice == "3":
            self.generate_word()
        elif choice == "4":
            self.generate_all_words()
        elif choice == "5":
            self.validate_word()
        elif choice == "6":
            self.manage_derivatives()
        elif choice == "7":
            self.display_statistics()
        elif choice == "8":
            self.tree_operations()
        elif choice == "9":
            self.hash_table_info()
        elif choice == "10":
            self.export_results()
        elif choice == "0":
            self.exit_application()
        else:
            console.print("[red]Invalid choice! Please try again.[/red]")
    
    def manage_derivatives(self):
        """Manage derivatives menu."""
        console.print(Panel.fit(
            "[bold magenta]Manage Derivatives[/bold magenta]",
            border_style="magenta"
        ))
        
        while True:
            console.print("\n[bold]Derivatives Management:[/bold]")
            console.print("1. View derivatives for a root")
            console.print("2. Remove specific derivative")
            console.print("3. Clear all derivatives for a root")
            console.print("4. Back to main menu")
            
            choice = Prompt.ask("Choose operation", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                self.view_derivatives()
            elif choice == "2":
                self.remove_derivative()
            elif choice == "3":
                self.clear_derivatives()
            elif choice == "4":
                break

    
    def view_derivatives(self):
        """View derivatives for a specific root."""
        root = Prompt.ask("Enter Arabic root to view derivatives", default="كتب")
        
        if not ArabicUtils.is_valid_root(root):
            console.print(f"[red]❌ '{root}' is not a valid Arabic root (must be 3 letters).[/red]")
            return
        
        node = self.engine.roots_tree.search(root)
        
        if node:
            derivatives = node.get_derivatives()
            
            if derivatives:
                console.print(f"\n📚 Derivatives for root '{root}':")
                
                table = Table(title=f"Validated Derivatives for {root}")
                table.add_column("#", style="cyan")
                table.add_column("Word", style="green")
                table.add_column("Pattern", style="yellow")
                table.add_column("Frequency", style="magenta")
                
                for i, deriv in enumerate(derivatives, 1):
                    table.add_row(
                        str(i),
                        deriv['word'],
                        deriv['pattern'],
                        str(deriv['frequency'])
                    )
                
                console.print(table)
                console.print(f"Total: {len(derivatives)} derivatives")
            else:
                console.print(f"\n📝 No derivatives validated yet for root '{root}'.")
        else:
            console.print(f"[yellow]Root '{root}' not found.[/yellow]")


    def remove_derivative(self):
        """Remove a specific derivative."""
        root = Prompt.ask("Enter Arabic root", default="كتب")
        
        if not ArabicUtils.is_valid_root(root):
            console.print(f"[red]❌ Invalid root: {root}[/red]")
            return
        
        # Show current derivatives
        node = self.engine.roots_tree.search(root)
        if not node:
            console.print(f"[yellow]Root '{root}' not found.[/yellow]")
            return
        
        derivatives = node.get_derivatives()
        if not derivatives:
            console.print(f"[yellow]No derivatives for root '{root}' to remove.[/yellow]")
            return
        
        console.print(f"\n📚 Current derivatives for '{root}':")
        for i, deriv in enumerate(derivatives, 1):
            console.print(f"  {i}. {deriv['word']} (Pattern: {deriv['pattern']}, Freq: {deriv['frequency']})")
        
        # Get removal choice
        console.print("\n[bold]Removal Options:[/bold]")
        console.print("1. Remove by index")
        console.print("2. Remove by word and pattern")
        
        removal_choice = Prompt.ask("Choose removal method", choices=["1", "2"])
        
        if removal_choice == "1":
            try:
                index = int(Prompt.ask("Enter derivative number to remove", 
                                    choices=[str(i) for i in range(1, len(derivatives) + 1)]))
                
                if 1 <= index <= len(derivatives):
                    derivative = derivatives[index - 1]
                    word = derivative['word']
                    pattern = derivative['pattern']
                    
                    if self.engine.remove_derivative(root, word, pattern):
                        console.print(f"[green]✅ Removed '{word}' (pattern: {pattern}) from root '{root}'[/green]")
                    else:
                        console.print(f"[red]❌ Failed to remove derivative.[/red]")
                else:
                    console.print("[red]❌ Invalid index.[/red]")
            except ValueError:
                console.print("[red]❌ Invalid input.[/red]")
        
        elif removal_choice == "2":
            word = Prompt.ask("Enter word to remove")
            pattern = Prompt.ask("Enter pattern name (leave empty to remove all matches)", default="")
            
            if pattern == "":
                pattern = None
                confirm = Confirm.ask(f"Remove ALL occurrences of '{word}' from root '{root}'?")
            else:
                confirm = Confirm.ask(f"Remove '{word}' with pattern '{pattern}' from root '{root}'?")
            
            if confirm:
                if self.engine.remove_derivative(root, word, pattern):
                    if pattern:
                        console.print(f"[green]✅ Removed '{word}' (pattern: {pattern}) from root '{root}'[/green]")
                    else:
                        console.print(f"[green]✅ Removed all occurrences of '{word}' from root '{root}'[/green]")
                else:
                    console.print(f"[red]❌ Derivative not found.[/red]")
    
    def clear_derivatives(self):
        """Clear all derivatives for a root."""
        root = Prompt.ask("Enter Arabic root to clear derivatives", default="كتب")
        
        if not ArabicUtils.is_valid_root(root):
            console.print(f"[red]❌ Invalid root: {root}[/red]")
            return
        
        node = self.engine.roots_tree.search(root)
        if not node:
            console.print(f"[yellow]Root '{root}' not found.[/yellow]")
            return
        
        derivatives_count = node.get_derivative_count()
        
        if derivatives_count == 0:
            console.print(f"[yellow]No derivatives to clear for root '{root}'.[/yellow]")
            return
        
        confirm = Confirm.ask(f"Clear ALL {derivatives_count} derivatives for root '{root}'?")
        
        if confirm:
            if self.engine.clear_root_derivatives(root):
                console.print(f"[green]✅ Cleared {derivatives_count} derivatives from root '{root}'[/green]")
            else:
                console.print(f"[red]❌ Failed to clear derivatives.[/red]")


    def load_data(self):
        """Load data from files."""
        console.print(Panel.fit(
            "[bold blue]Loading Data[/bold blue]",
            border_style="blue"
        ))
        
        if self.load_data_files():
            console.print("[green]✅ Data loaded successfully![/green]")
            
            # Display summary
            stats = self.engine.get_engine_statistics()
            console.print(f"\n📊 Loaded: {stats['roots_count']} roots, {stats['patterns_count']} patterns")
        else:
            console.print("[red]❌ Failed to load data.[/red]")
    
    def search_root(self):
        """Search for a root in AVL tree."""
        console.print(Panel.fit(
            "[bold blue]Search Root in AVL Tree[/bold blue]",
            border_style="blue"
        ))
        
        root = Prompt.ask("Enter Arabic root to search", default="كتب")
        
        if not ArabicUtils.is_valid_root(root):
            console.print(f"[red]❌ '{root}' is not a valid Arabic root (must be 3 letters).[/red]")
            return
        
        # Search in AVL tree
        root_node = self.engine.roots_tree.search(root)
        
        if root_node:
            console.print(f"[green]✅ Root '{root}' found in AVL tree![/green]")
            
            # Display root info
            table = Table(title=f"Root Information: {root}")
            table.add_column("Attribute", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Root", root_node.root)
            table.add_row("Frequency", str(root_node.frequency))
            table.add_row("Derivatives Count", str(root_node.get_derivative_count()))
            table.add_row("Height in Tree", str(root_node.height))
            
            console.print(table)

            derivatives = root_node.get_derivatives()
 
            if derivatives:
                console.print(f"\n📚 Validated Derivatives ({len(derivatives)}):")
                deriv_table = Table()
                deriv_table.add_column("Word", style="cyan")
                deriv_table.add_column("Pattern", style="green")
                deriv_table.add_column("Frequency", style="yellow")
            
                for deriv in derivatives:
                    deriv_table.add_row(
                        deriv['word'],
                        deriv['pattern'],
                        str(deriv['frequency'])
                    )
            
                console.print(deriv_table)
            else:
                console.print("\n📝 No derivatives validated yet for this root.")

            
        else:
            console.print(f"[yellow]Root '{root}' not found in AVL tree.[/yellow]")
            
            # Offer to add it
            if Confirm.ask(f"Would you like to add '{root}' to the tree?"):
                self.engine.roots_tree.insert(root)
                console.print(f"[green]✅ Root '{root}' added to AVL tree.[/green]")
    
    def generate_word(self):
        """Generate word from root and pattern."""
        console.print(Panel.fit(
            "[bold blue]Generate Arabic Word[/bold blue]",
            border_style="blue"
        ))
        
        root = Prompt.ask("Enter Arabic root", default="كتب")
        
        if not ArabicUtils.is_valid_root(root):
            console.print(f"[red]❌ Invalid root: {root}[/red]")
            return
        
        # Show available patterns
        all_patterns = self.engine.patterns_table.get_all_patterns()
        if not all_patterns:
            console.print("[yellow]No patterns loaded. Please load data first.[/yellow]")
            return
        
        console.print("\n[bold]Available Patterns:[/bold]")
        for i, (pattern_name, pattern_data) in enumerate(all_patterns, 1):
            desc = pattern_data.get('description', '')
            console.print(f"  {i}. {pattern_name} - {desc}")
        
        pattern_choice = Prompt.ask(
            "\nEnter pattern name or number",
            choices=[str(i) for i in range(1, len(all_patterns) + 1)] + [p[0] for p in all_patterns]
        )
        
        # Get pattern name
        if pattern_choice.isdigit():
            idx = int(pattern_choice) - 1
            if 0 <= idx < len(all_patterns):
                pattern_name = all_patterns[idx][0]
            else:
                console.print("[red]❌ Invalid pattern number.[/red]")
                return
        else:
            pattern_name = pattern_choice
        
        # Generate the word
        with console.status(f"Generating word from '{root}' with pattern '{pattern_name}'..."):
            result = self.engine.generate_word(root, pattern_name)
        
        if result:
            console.print("\n[green]✅ Word generated successfully![/green]")
            
            # Display results in a nice table
            table = Table(title="Generation Results", box=None)
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Root", result['root'])
            table.add_row("Pattern", result['pattern'])
            table.add_row("Generated Word", f"[bold]{result['generated_word']}[/bold]")
            table.add_row("Valid", "✓" if result['is_valid'] else "✗")
            table.add_row("Template", result['template'])
            table.add_row("Description", result.get('description', 'N/A'))
            table.add_row("Example", result.get('example', 'N/A'))
            
            console.print(table)
        else:
            console.print("[red]❌ Failed to generate word.[/red]")
    
    def generate_all_words(self):
        """Generate all words for a root."""
        console.print(Panel.fit(
            "[bold blue]Generate All Words for Root[/bold blue]",
            border_style="blue"
        ))
        
        root = Prompt.ask("Enter Arabic root", default="كتب")
        
        if not ArabicUtils.is_valid_root(root):
            console.print(f"[red]❌ Invalid root: {root}[/red]")
            return
        
        # Generate all words
        with Progress() as progress:
            task = progress.add_task(f"Generating words for '{root}'...", total=None)
            results = self.engine.generate_all_for_root(root)
            progress.update(task, completed=100)
        
        if results:
            console.print(f"\n[green]✅ Generated {len(results)} words for root '{root}':[/green]")
            
            # Display results
            console.print(self.engine.display_generation_results(results))
            
            # Show statistics
            root_stats = self.engine.get_root_statistics(root)
            console.print(f"\n📊 Root Statistics:")
            console.print(f"  • Frequency: {root_stats['frequency']}")
            console.print(f"  • Derivatives: {root_stats['derivative_count']}")
        else:
            console.print(f"[yellow]⚠️ No words generated for root '{root}'.[/yellow]")
    
    def validate_word(self):
        """Validate if a word belongs to a root."""
        console.print(Panel.fit(
            "[bold blue]Validate Arabic Word[/bold blue]",
            border_style="blue"
        ))
        
        word = Prompt.ask("Enter Arabic word to validate", default="كاتب")
        
        # Ask if user wants to check against specific root
        check_specific = Confirm.ask("Check against specific root? (No to search all)")
        
        if check_specific:
            root = Prompt.ask("Enter root to check against", default="كتب")
            validation = self.engine.validate_word(word, root)
        else:
            validation = self.engine.validate_word(word)
        
        # Display results
        console.print("\n[bold]Validation Results:[/bold]")
        
        table = Table(box=None)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Word", validation['word'])
        table.add_row("Valid", "[green]✓ Yes[/green]" if validation['is_valid'] else "[red]✗ No[/red]")
        table.add_row("Message", validation['message'])
        
        if validation['is_valid']:
            if 'matches' in validation:
                table.add_row("Matches Found", str(len(validation['matches'])))
                # Show first few matches
                for i, match in enumerate(validation['matches'][:3], 1):
                    table.add_row(f"Match {i}", f"Root: {match['root']}, Pattern: {match['pattern']}")
            else:
                table.add_row("Root", validation.get('root', 'N/A'))
                table.add_row("Pattern", validation.get('pattern', 'N/A'))
        else:
            if 'possible_roots' in validation:
                table.add_row("Possible Roots", ', '.join(validation['possible_roots']))
        
        console.print(table)
    
    def display_statistics(self):
        """Display engine statistics."""
        console.print(Panel.fit(
            "[bold blue]Engine Statistics[/bold blue]",
            border_style="blue"
        ))
        
        stats = self.engine.get_engine_statistics()
        
        table = Table(title="Morphological Engine Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Description", style="yellow")
        
        table.add_row("Roots Count", str(stats['roots_count']), "Arabic roots in AVL tree")
        table.add_row("Patterns Count", str(stats['patterns_count']), "Morphological patterns in hash table")
        table.add_row("Generated Words", str(stats['generated_words_count']), "Total words generated")
        table.add_row("Unique Roots", str(stats['unique_roots_with_generated']), "Roots with generated words")
        table.add_row("AVL Tree Height", str(stats['avl_tree_height']), "Height of the AVL tree (O(log n))")
        table.add_row("Hash Table Load", f"{stats['hash_table_load_factor']:.2f}", "Load factor (optimal < 0.75)")
        
        console.print(table)
        
        # AVL tree info
        console.print("\n[bold]AVL Tree Information:[/bold]")
        console.print(f"  • Search complexity: O(log n) - Efficient!")
        console.print(f"  • Self-balancing: Yes - Maintains height balance")
        console.print(f"  • Operations: Insert, Search, Delete in O(log n)")
        
        # Hash table info
        console.print("\n[bold]Hash Table Information:[/bold]")
        console.print(f"  • Average search: O(1) - Constant time!")
        console.print(f"  • Collision resolution: Separate chaining")
        console.print(f"  • Dynamic resizing: When load factor > 0.75")


    # Update the tree_operations method in main.py

    def tree_operations(self):
        """AVL tree operations submenu."""
        console.print(Panel.fit(
            "[bold green]AVL Tree Operations[/bold green]",
            border_style="green"
        ))
        
        while True:
            console.print("\n[bold]Tree Operations:[/bold]")
            console.print("1. Display all roots (inorder traversal)")
            console.print("2. Count nodes in tree")
            console.print("3. Get tree height and balance info")
            console.print("4. Display tree structure (ASCII)")
            console.print("5. Display tree structure (Horizontal)")
            console.print("6. Display tree statistics")
            console.print("7. Back to main menu")
            
            choice = Prompt.ask("Choose operation", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                roots = self.engine.roots_tree.display_inorder()
                console.print(f"\n🌳 Roots in AVL tree (inorder traversal):")
                if roots:
                    console.print(", ".join(roots))
                    console.print(f"Total: {len(roots)} roots")
                else:
                    console.print("[yellow]Tree is empty.[/yellow]")
            
            elif choice == "2":
                count = self.engine.roots_tree.count_nodes()
                console.print(f"\n📊 Nodes in AVL tree: {count}")
                
                # Calculate theoretical max height for balanced tree
                if count > 0:
                    import math
                    min_height = math.floor(math.log2(count + 1))
                    max_height = 1.44 * math.log2(count + 2) - 0.328  # Theoretical for AVL
                    console.print(f"📏 Theoretical height range for {count} nodes:")
                    console.print(f"   • Minimum possible: {min_height}")
                    console.print(f"   • AVL max (worst-case): ~{max_height:.1f}")
                    console.print(f"   • Our tree height: {self.engine.roots_tree.get_tree_height()}")
            
            elif choice == "3":
                height = self.engine.roots_tree.get_tree_height()
                count = self.engine.roots_tree.count_nodes()
                
                console.print(f"\n📏 AVL Tree Height Analysis:")
                console.print(f"   • Actual height: {height}")
                console.print(f"   • Number of nodes: {count}")
                
                if count > 0:
                    # Calculate balance metrics
                    import math
                    optimal_min = math.floor(math.log2(count))
                    optimal_max = 1.44 * math.log2(count + 2) - 0.328
                    
                    if height <= optimal_max:
                        console.print("   ⚖️  Tree is well-balanced ✓")
                    else:
                        console.print("   ⚠️  Tree might need rebalancing")
                    
                    console.print(f"\n📈 Complexity analysis:")
                    console.print(f"   • Search time: O(log n) = O(log {count}) ≈ {math.log2(count):.1f} operations")
                    console.print(f"   • Space: O(n) = {count} nodes")
                    console.print(f"   • Insert/Delete: O(log n) with rotations")
            
            elif choice == "4":
                console.print("\n🌳 AVL Tree Structure (ASCII - Rotated 90°):")
                console.print("[dim]Right is up, Left is down[/dim]")
                console.print("=" * 60)
                
                tree_ascii = self.engine.roots_tree.display_tree_ascii()
                if tree_ascii:
                    console.print(tree_ascii)
                    console.print("\n[dim]Legend: h=height, bal=balance factor[/dim]")
                else:
                    console.print("[yellow]Tree is empty.[/yellow]")
                
                console.print("=" * 60)
            
            elif choice == "5":
                console.print("\n🌳 AVL Tree Structure (Horizontal - Top Down):")
                console.print("[dim]Root at top, children below[/dim]")
                console.print("=" * 60)
                
                tree_horizontal = self.engine.roots_tree.display_tree_horizontal()
                console.print(tree_horizontal)
                
                console.print("\n[dim]Legend: (hX) = height X[/dim]")
                console.print("=" * 60)
            
            elif choice == "6":
                console.print("\n📊 AVL Tree Detailed Statistics:")
                
                count = self.engine.roots_tree.count_nodes()
                height = self.engine.roots_tree.get_tree_height()
                
                table = Table(title="Tree Statistics", box=None)
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")
                table.add_column("Analysis", style="yellow")
                
                table.add_row("Total Nodes", str(count), "n = number of Arabic roots")
                
                if count > 0:
                    import math
                    min_possible = math.floor(math.log2(count + 1))
                    avl_max = 1.44 * math.log2(count + 2) - 0.328
                    
                    table.add_row(
                        "Tree Height", 
                        str(height),
                        f"Optimal: {min_possible} ≤ h ≤ {avl_max:.1f}"
                    )
                    
                    balance_status = "Balanced" if height <= avl_max else "Needs attention"
                    table.add_row(
                        "Balance Status",
                        balance_status,
                        "AVL maintains |balance| ≤ 1"
                    )
                    
                    efficiency = height / math.log2(count) if count > 1 else 1
                    table.add_row(
                        "Efficiency Ratio",
                        f"{efficiency:.2f}",
                        "Closer to 1 is better"
                    )
                    
                    # Get all nodes to calculate average derivatives
                    all_nodes = self.engine.roots_tree.get_all_nodes()
                    total_derivatives = sum(node.get_derivative_count() for node in all_nodes)
                    avg_derivatives = total_derivatives / count if count > 0 else 0
                    
                    table.add_row(
                        "Avg Derivatives/Node",
                        f"{avg_derivatives:.1f}",
                        "Average validated words per root"
                    )
                    
                    # Count leaves
                    leaves = sum(1 for node in all_nodes if node.left is None and node.right is None)
                    table.add_row(
                        "Leaf Nodes",
                        str(leaves),
                        f"{leaves/count*100:.1f}% of total"
                    )
                
                console.print(table)
                
                # Show tree properties
                console.print("\n[bold]AVL Tree Properties:[/bold]")
                console.print("• Self-balancing binary search tree")
                console.print(f"• Height: {height}, ensures O(log n) operations")
                console.print("• For n nodes, maximum height ≈ 1.44×log₂(n+2)")
                console.print("• Balance factor = height(left) - height(right) ∈ {-1, 0, 1}")
            
            elif choice == "7":
                break
    
    # def tree_operations(self):
    #     """AVL tree operations submenu."""
    #     console.print(Panel.fit(
    #         "[bold green]AVL Tree Operations[/bold green]",
    #         border_style="green"
    #     ))
        
    #     while True:
    #         console.print("\n[bold]Tree Operations:[/bold]")
    #         console.print("1. Display all roots (inorder traversal)")
    #         console.print("2. Count nodes in tree")
    #         console.print("3. Get tree height")
    #         console.print("4. Back to main menu")
            
    #         choice = Prompt.ask("Choose operation", choices=["1", "2", "3", "4"])
            
    #         if choice == "1":
    #             roots = self.engine.roots_tree.display_inorder()
    #             console.print(f"\n🌳 Roots in AVL tree ({len(roots)}):")
    #             console.print(", ".join(roots) if roots else "[yellow]Tree is empty.[/yellow]")
            
    #         elif choice == "2":
    #             count = self.engine.roots_tree.count_nodes()
    #             console.print(f"\n📊 Nodes in AVL tree: {count}")
            
    #         elif choice == "3":
    #             height = self.engine.roots_tree.get_tree_height()
    #             console.print(f"\n📏 AVL tree height: {height}")
    #             console.print(f"   For {self.engine.roots_tree.count_nodes()} nodes, optimal height is O(log n)")
            
    #         elif choice == "4":
    #             break
    
    def hash_table_info(self):
        """Hash table information submenu."""
        console.print(Panel.fit(
            "[bold magenta]Hash Table Information[/bold magenta]",
            border_style="magenta"
        ))
        
        if len(self.engine.patterns_table) == 0:
            console.print("[yellow]No patterns loaded in hash table.[/yellow]")
            return
        
        stats = self.engine.patterns_table.display_stats()
        
        console.print("\n[bold]Hash Table Statistics:[/bold]")
        table = Table(box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in stats.items():
            if isinstance(value, float):
                table.add_row(key.replace('_', ' ').title(), f"{value:.2f}")
            else:
                table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(table)
        
        # Show all patterns
        if Confirm.ask("\nShow all patterns in hash table?"):
            patterns = self.engine.patterns_table.get_all_patterns()
            
            pattern_table = Table(title="Morphological Patterns")
            pattern_table.add_column("Pattern", style="cyan")
            pattern_table.add_column("Template", style="green")
            pattern_table.add_column("Description", style="yellow")
            
            for pattern_name, pattern_data in sorted(patterns, key=lambda x: x[0]):
                pattern_table.add_row(
                    pattern_name,
                    pattern_data.get('template', 'N/A'),
                    pattern_data.get('description', '')[:30] + ('...' if len(pattern_data.get('description', '')) > 30 else '')
                )
            
            console.print(pattern_table)
    
    def export_results(self):
        """Export generated words."""
        console.print(Panel.fit(
            "[bold blue]Export Results[/bold blue]",
            border_style="blue"
        ))
        
        # Check if any roots have derivatives
        all_nodes = self.engine.roots_tree.get_all_nodes()
        has_derivatives = any(node.get_derivative_count() > 0 for node in all_nodes)

        if not has_derivatives:
            console.print("[yellow]No generated words to export.[/yellow]")
            return
        
        console.print("\n[bold]Export Formats:[/bold]")
        console.print("1. Text (readable in terminal)")
        console.print("2. CSV (for Excel/Google Sheets)")
        console.print("3. JSON (for programming)")
        
        choice = Prompt.ask("Choose format", choices=["1", "2", "3"])
        
        format_map = {"1": "text", "2": "csv", "3": "json"}
        export_format = format_map[choice]
        
        # Export
        export_data = self.engine.export_results(export_format)
        
        # Save to file
        filename = f"exported_words.{export_format}"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(export_data)
        
        console.print(f"\n[green]✅ Exported to '{filename}'[/green]")
        
        # Show preview
        if Confirm.ask(f"Show preview of exported data?"):
            console.print(f"\n[bold]Preview (first 10 lines):[/bold]")
            lines = export_data.split('\n')[:10]
            for line in lines:
                console.print(f"  {line}")
    
    def exit_application(self):
        """Exit the application."""
        console.print(Panel.fit(
            "[bold]Thank you for using the Arabic Morphological Engine![/bold]\n"
            "Project completed successfully! 🎉",
            title="Goodbye",
            border_style="cyan"
        ))
        self.running = False
    
    def run(self):
        """Main application loop."""
        self.display_welcome()
        
        # Load initial data
        if Confirm.ask("Load data from files?"):
            self.load_data_files()
        
        # Main loop
        while self.running:
            try:
                self.display_menu()
                choice = Prompt.ask("Enter your choice", default="0")
                console.print()
                self.handle_choice(choice)
                console.print()
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user.[/yellow]")
                if Confirm.ask("Exit application?"):
                    self.exit_application()
                    break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                console.print("[yellow]Returning to main menu...[/yellow]")

def main():
    """Entry point of the application."""
    try:
        cli = ArabicMorphologyCLI()
        cli.run()
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())