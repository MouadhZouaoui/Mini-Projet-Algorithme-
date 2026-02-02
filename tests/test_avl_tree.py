"""
Test file for AVL Tree implementation.
Run with: python -m pytest tests/test_avl.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from avl_tree import AVLTree

def test_insert_and_search():
    """Test basic insertion and search."""
    tree = AVLTree()
    
    # Insert some Arabic roots
    roots = ["كتب", "قرأ", "درس", "عمل", "فهم", "سمع", "نظر", "ذهب"]
    
    for root in roots:
        tree.insert(root)
    
    # Test search - should find all
    for root in roots:
        node = tree.search(root)
        assert node is not None, f"Root {root} not found"
        assert node.root == root, f"Found wrong root: {node.root}"
    
    # Test search for non-existent root
    assert tree.search("XXXX") is None, "Non-existent root should return None"
    
    print("✅ test_insert_and_search passed")

def test_balancing():
    """Test that tree remains balanced."""
    tree = AVLTree()
    
    # Insert in sorted order (worst case for BST)
    roots = ["أكل", "بدء", "جلس", "دخل", "ذهب", "ذهب", "وقف"]
    
    for root in roots:
        tree.insert(root)
    
    # Check tree height
    height = tree.get_tree_height()
    node_count = tree.count_nodes()
    
    # For AVL tree, height should be O(log n)
    # With 6 nodes, max height should be ~3
    assert height <= 3, f"Tree height {height} is too large for {node_count} nodes"
    
    print(f"✅ Tree has {node_count} nodes, height {height} (balanced)")
    print("✅ test_balancing passed")

def test_inorder_traversal():
    """Test that roots are returned in sorted order."""
    tree = AVLTree()
    
    # Insert in random order
    roots = ["كتب", "قرأ", "درس", "عمل", "فهم"]
    
    for root in roots:
        tree.insert(root)
    
    # Get sorted list
    sorted_roots = tree.display_inorder()
    
    # Should be sorted alphabetically
    expected = sorted(roots)
    assert sorted_roots == expected, f"Expected {expected}, got {sorted_roots}"
    
    print(f"✅ Sorted roots: {sorted_roots}")
    print("✅ test_inorder_traversal passed")

def test_duplicate_roots():
    """Test handling duplicate roots."""
    tree = AVLTree()
    
    # Insert same root multiple times
    tree.insert("كتب")
    tree.insert("كتب")
    tree.insert("كتب")
    
    # Should only have one node
    assert tree.count_nodes() == 1, "Duplicate roots should not create new nodes"
    
    # Frequency should be updated
    node = tree.search("كتب")
    assert node.frequency == 3, f"Frequency should be 3, got {node.frequency}"
    
    print("✅ test_duplicate_roots passed")

def test_empty_tree():
    """Test operations on empty tree."""
    tree = AVLTree()
    
    assert tree.search("كتب") is None
    assert tree.display_inorder() == []
    assert tree.count_nodes() == 0
    assert tree.get_tree_height() == 0
    
    print("✅ test_empty_tree passed")

if __name__ == "__main__":
    print("🚀 Running AVL Tree Tests...\n")
    
    test_empty_tree()
    print()
    
    test_insert_and_search()
    print()
    
    test_balancing()
    print()
    
    test_inorder_traversal()
    print()
    
    test_duplicate_roots()
    print()
    
    print("🎉 All tests passed! AVL Tree is working correctly.")