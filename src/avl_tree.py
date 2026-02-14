"""
AVL Tree implementation for Arabic roots.

Features:
- Self-balancing binary search tree
- Stores Arabic triliteral roots (3-letter roots)
- O(log n) search, dynamic insertion, delete
- In-order traversal for sorted display

Author: [Your Name]
Date: [Today's Date]
"""

from arabic_utils import ArabicUtils


class AVLNode:
    """Node in AVL Tree storing an Arabic root."""
    
    def __init__(self, root: str):
        """
        Initialize an AVL node.
        
        Args:
            root (str): Arabic root (3 letters, e.g., "كتب")
        """
        self.root = root  # The Arabic root
        self.derivatives = []  # List of validated derived words
        self.frequency = 1  # Usage frequency (optional feature)
        self.left = None    # Left child
        self.right = None   # Right child
        self.height = 1     # Height of node (for balancing)

    def add_derivative(self, word: str, pattern: str) -> None:
        """
        Add a validated derived word to this root.
        
        Args:
            word (str): The derived Arabic word
            pattern (str): Pattern used to generate it
        """
        # Check if this word already exists for this root
        for existing in self.derivatives:
            if existing['word'] == word and existing['pattern'] == pattern:
                existing['frequency'] += 1
                return
        
        # Add new derivative
        self.derivatives.append({
            'word': word,
            'pattern': pattern,
            'frequency': 1
        })

    def get_derivatives(self) -> list:
        """Get all derivatives for this root."""
        return self.derivatives
    
    def get_derivative_count(self) -> int:
        """Get number of derivatives for this root."""
        return len(self.derivatives)

    def remove_derivative(self, word: str, pattern: str = None) -> bool:
        """
        Remove a derivative from this root.
        
        Args:
            word (str): The derived word to remove
            pattern (str, optional): Specific pattern to remove. 
                                    If None, remove all occurrences of the word.
        
        Returns:
            bool: True if removed, False if not found
        """
        removed = False
        indices_to_remove = []
        
        for i, deriv in enumerate(self.derivatives):
            if deriv['word'] == word and (pattern is None or deriv['pattern'] == pattern):
                indices_to_remove.append(i)
                removed = True
        
        # Remove from highest index to lowest to avoid shifting issues
        for i in sorted(indices_to_remove, reverse=True):
            del self.derivatives[i]
        
        return removed
    
    def clear_derivatives(self) -> None:
        """Clear all derivatives for this root."""
        self.derivatives.clear()


class AVLTree:
    """Self-balancing AVL Tree for Arabic roots."""
    
    def __init__(self):
        """Initialize empty AVL tree."""
        self.root = None
    
    def insert(self, root: str) -> None:
        """
        Public method to insert a new Arabic root.
        
        Args:
            root (str): Arabic root to insert (3 letters)
        """

        # Normalize the root first (expand shadda)
        normalized_root = ArabicUtils.normalize_arabic(root, aggressive=False, expand_shadda=True)
        
        # Check if it's a valid root after normalization
        if not ArabicUtils.is_valid_root(normalized_root):
            print(f"❌ '{root}' is not a valid Arabic root after normalization")
            return
        
        self.root = self._insert(self.root, normalized_root)
    
    def _insert(self, node: AVLNode, root: str) -> AVLNode:
        """
        Recursively insert a root and balance the tree.
        
        Args:
            node (AVLNode): Current node
            root (str): Arabic root to insert
            
        Returns:
            AVLNode: Updated node after insertion and balancing
        """
        # Step 1: Perform normal BST insertion
        if node is None:
            return AVLNode(root)
        
        # Compare Arabic roots lexicographically
        if root < node.root:
            node.left = self._insert(node.left, root)
        elif root > node.root:
            node.right = self._insert(node.right, root)
        else:
            # Root already exists - update frequency or do nothing
            node.frequency += 1
            return node
        
        # Step 2: Update height of current node
        node.height = 1 + max(self._get_height(node.left), 
                             self._get_height(node.right))
        
        # Step 3: Get balance factor
        balance = self._get_balance(node)
        
        # Step 4: If unbalanced, handle 4 cases
        
        # Left Left Case
        if balance > 1 and root < node.left.root:
            return self._right_rotate(node)
        
        # Right Right Case
        if balance < -1 and root > node.right.root:
            return self._left_rotate(node)
        
        # Left Right Case
        if balance > 1 and root > node.left.root:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Left Case
        if balance < -1 and root < node.right.root:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node
    
    def search(self, root: str) -> AVLNode:
        """
        Search for an Arabic root in the tree.
        
        Args:
            root (str): Arabic root to search for
            
        Returns:
            AVLNode: Node containing the root, or None if not found
        """
        return self._search(self.root, root)
    
    def _search(self, node: AVLNode, root: str) -> AVLNode:
        """Recursive search helper."""
        if node is None or node.root == root:
            return node
        
        if root < node.root:
            return self._search(node.left, root)
        else:
            return self._search(node.right, root)
    
    def display_inorder(self) -> list:
        """
        Return all roots in sorted order (in-order traversal).
        
        Returns:
            list: Sorted list of Arabic roots
        """
        result = []
        self._inorder_traversal(self.root, result)
        return result
    
    def _inorder_traversal(self, node: AVLNode, result: list) -> None:
        """Recursive in-order traversal."""
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.root)
            self._inorder_traversal(node.right, result)
    
    # ========== AVL HELPER METHODS ==========
    
    def _get_height(self, node: AVLNode) -> int:
        """Get height of node (handle None case)."""
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node: AVLNode) -> int:
        """Get balance factor of node."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _right_rotate(self, y: AVLNode) -> AVLNode:
        r"""
        Right rotate subtree rooted with y.
        
            y                          x
           / \     Right Rotate       / \
          x   T3   ––––––––––––>     T1  y
         / \                            / \
        T1  T2                         T2  T3
        """
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), 
                          self._get_height(x.right))
        
        return x
    
    def _left_rotate(self, x: AVLNode) -> AVLNode:
        r"""
        Left rotate subtree rooted with x.
        
            x                          y
           / \     Left Rotate        / \
          T1  y    ––––––––––––>     x   T3
             / \                    / \
            T2  T3                 T1  T2
        """
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        x.height = 1 + max(self._get_height(x.left), 
                          self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), 
                          self._get_height(y.right))
        
        return y
    
    def get_tree_height(self) -> int:
        """Get height of the entire tree."""
        return self._get_height(self.root)
    
    def count_nodes(self) -> int:
        """Count total nodes in the tree."""
        return self._count_nodes(self.root)
    
    def _count_nodes(self, node: AVLNode) -> int:
        """Recursive node counter."""
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
    
    def get_all_nodes(self) -> list[AVLNode]:
        """
        Get all nodes in the tree.
        
        Returns:
            List[AVLNode]: List of all nodes
        """
        nodes = []
        self._collect_nodes(self.root, nodes)
        return nodes
    
    def _collect_nodes(self, node: AVLNode, nodes_list: list[AVLNode]) -> None:
        """Recursively collect all nodes."""
        if node:
            self._collect_nodes(node.left, nodes_list)
            nodes_list.append(node)
            self._collect_nodes(node.right, nodes_list)

    def remove_derivative(self, root: str, word: str, pattern: str = None) -> bool:
        """
        Remove a derivative from a specific root.
        
        Args:
            root (str): Arabic root
            word (str): Derived word to remove
            pattern (str, optional): Specific pattern
        
        Returns:
            bool: True if removed, False if not found
        """
        node = self.search(root)
        if node:
            return node.remove_derivative(word, pattern)
        return False

    #################################################################################################################
    ##################################### TREE VISUALIZATION (OPTIONAL) #############################################
    #################################################################################################################

    # Add to the AVLTree class in avl_tree.py
        
    def get_tree_structure(self) -> dict:
        """
        Get tree structure for visualization.
        
        Returns:
            dict: Tree structure with nodes and connections
        """
        return self._get_node_structure(self.root)
    
    def _get_node_structure(self, node: AVLNode) -> dict:
        """Recursively get node structure."""
        if node is None:
            return None
        
        return {
            'root': node.root,
            'height': node.height,
            'balance': self._get_balance(node),
            'derivative_count': node.get_derivative_count(),
            'frequency': node.frequency,
            'left': self._get_node_structure(node.left),
            'right': self._get_node_structure(node.right)
        }
    
    def display_tree_ascii(self) -> str:
        """
        Display tree in ASCII format (sideways, rotated 90°).
        
        Returns:
            str: ASCII representation of the tree
        """
        lines = []
        self._generate_ascii_tree(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _generate_ascii_tree(self, node: AVLNode, prefix: str, is_left: bool, lines: list) -> None:
        """
        Generate ASCII tree representation recursively.
        
        Args:
            node: Current node
            prefix: Prefix string for this line
            is_left: Whether this node is a left child
            lines: List to accumulate lines
        """
        if node is None:
            return
        
        # Add right subtree
        self._generate_ascii_tree(
            node.right, 
            prefix + ("│   " if is_left else "    "), 
            False, 
            lines
        )
        
        # Add current node
        line = prefix + ("└── " if is_left else "┌── ") + node.root
        line += f" (h={node.height}, bal={self._get_balance(node)})"
        if node.get_derivative_count() > 0:
            line += f" [Derivatives: {node.get_derivative_count()}]"
        lines.append(line)
        
        # Add left subtree
        self._generate_ascii_tree(
            node.left, 
            prefix + ("    " if is_left else "│   "), 
            True, 
            lines
        )
    
    def display_tree_horizontal(self) -> str:
        """
        Display tree in horizontal format (top-down).
        Good for smaller trees.
        
        Returns:
            str: Horizontal tree representation
        """
        if self.root is None:
            return "🌳 Empty tree"
        
        result = []
        current_level = [self.root]
        
        while any(node is not None for node in current_level):
            # Print current level
            level_str = ""
            next_level = []
            
            for node in current_level:
                if node is None:
                    level_str += "    "
                    next_level.extend([None, None])
                else:
                    level_str += f"{node.root}(h{node.height}) "
                    next_level.append(node.left)
                    next_level.append(node.right)
            
            result.append(level_str.center(100))
            current_level = next_level
        
        return "\n".join(result)
    

    