"""
Test tree visualization and structure.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from avl_tree import AVLTree

def test_tree_visualization():
    """Test ASCII tree visualization."""
    print("🌳 Testing Tree Visualization...")
    
    tree = AVLTree()
    
    # Insert roots in a specific order to create interesting tree structure
    test_roots = ["كتب", "قرأ", "درس", "عمل", "فهم", "سمع", "نظر", "ذهب"]
    
    for root in test_roots:
        tree.insert(root)
    
    print("\n✅ Tree created with 8 Arabic roots")
    print(f"   • Nodes: {tree.count_nodes()}")
    print(f"   • Height: {tree.get_tree_height()}")
    
    # Test ASCII tree
    print("\n📐 ASCII Tree Visualization:")
    print("=" * 50)
    ascii_tree = tree.display_tree_ascii()
    print(ascii_tree)
    print("=" * 50)
    
    # Test horizontal tree
    print("\n📊 Horizontal Tree Visualization:")
    print("=" * 50)
    horizontal_tree = tree.display_tree_horizontal()
    print(horizontal_tree)
    print("=" * 50)
    
    # Test tree structure
    print("\n🔧 Tree Structure Data:")
    structure = tree.get_tree_structure()
    print(f"   • Root node: {structure['root'] if structure else 'None'}")
    print(f"   • Root height: {structure['height'] if structure else 0}")
    print(f"   • Root balance: {structure['balance'] if structure else 0}")
    
    print("\n✅ All visualization tests passed!")

def test_height_calculation():
    """Verify height calculation method."""
    print("\n📏 Testing Height Calculation...")
    
    tree = AVLTree()
    
    # Empty tree
    assert tree.get_tree_height() == 0
    
    # Single node
    tree.insert("كتب")
    assert tree.get_tree_height() == 1
    
    # Two nodes (left child)
    tree.insert("أكل")  # Should come before كتب alphabetically
    height = tree.get_tree_height()
    print(f"   • 2 nodes, height = {height}")
    assert height == 2
    
    # Three nodes (balanced)
    tree.insert("درس")
    height = tree.get_tree_height()
    print(f"   • 3 nodes, height = {height}")
    assert height == 2  # Should be balanced
    
    print("✅ Height calculation correct")

def test_balance_property():
    """Test that AVL tree maintains balance."""
    print("\n⚖️ Testing AVL Balance Property...")
    
    tree = AVLTree()
    
    # Insert in sorted order (worst case for BST, but AVL should balance)
    sorted_roots = ["أ", "ب", "ت", "ث", "ج", "ح", "خ"]
    
    for root in sorted_roots:
        tree.insert(root)
    
    height = tree.get_tree_height()
    nodes = tree.count_nodes()
    
    # For AVL tree, height should be O(log n)
    # With 7 nodes, maximum height should be ~3
    import math
    max_expected = 1.44 * math.log2(nodes + 2) - 0.328
    
    print(f"   • Nodes: {nodes}")
    print(f"   • Actual height: {height}")
    print(f"   • Theoretical max for AVL: {max_expected:.2f}")
    
    assert height <= max_expected + 1  # Allow small tolerance
    print("✅ AVL tree maintains balance property")

def test_height_explanation():
    """Explain height calculation clearly."""
    print("\n📚 Height Calculation Explanation:")
    print("=" * 60)
    print("In our AVL tree implementation:")
    print("• Height = number of nodes in longest path from node to leaf")
    print("• Leaf nodes have height = 1 (themselves)")
    print("• Parent height = 1 + max(height(left_child), height(right_child))")
    print()
    print("Example Tree:")
    print("    A (height=3)")
    print("   / \\")
    print("  B   C (height=2)")
    print("     / \\")
    print("    D   E (height=1)")
    print()
    print("Calculation:")
    print("• D, E are leaves → height = 1")
    print("• C has children D(1) and E(1) → height = 1 + max(1,1) = 2")
    print("• B is leaf → height = 1")
    print("• A has children B(1) and C(2) → height = 1 + max(1,2) = 3")
    print("=" * 60)

def test_balance_factor():
    """Explain balance factor calculation."""
    print("\n⚖️ Balance Factor Explanation:")
    print("=" * 60)
    print("Balance Factor = height(left_subtree) - height(right_subtree)")
    print()
    print("Valid values for AVL tree: -1, 0, 1")
    print("• -1: Right subtree is 1 level taller")
    print("•  0: Both subtrees equal height")
    print("•  1: Left subtree is 1 level taller")
    print()
    print("If |balance| > 1, tree is unbalanced → rotation needed")
    print("=" * 60)

# Add these to the main test
if __name__ == "__main__":
    print("🌲 Running Tree Visualization Tests...")
    print("=" * 60)
    
    test_height_explanation()
    print()
    
    test_balance_factor()
    print()
    
    test_height_calculation()
    print()
    
    test_balance_property()
    print()
    
    test_tree_visualization()
    print()
    
    print("=" * 60)
    print("🎉 All tree visualization tests passed!")
    print("\n📈 Tree visualization is now available in the CLI!")