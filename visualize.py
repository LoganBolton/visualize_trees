import sys
from tree import *
import graphviz
from collections import deque
import math

def find_minmax_values(root):
    """Find the minimum and maximum values in the tree."""
    if not root:
        return 0, 0
    
    min_val = float('inf')
    max_val = float('-inf')
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        min_val = min(min_val, node.value)
        max_val = max(max_val, node.value)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return min_val, max_val

def scale_thickness(value, min_val, max_val, min_thickness=1, max_thickness=10):
    """Scale the node value to a thickness between min_thickness and max_thickness using logarithmic scaling."""
    if max_val == min_val or value <= 0:
        return min_thickness
    
    CONSTANT_SCALE = 1.5  # Reduced from 5.5 since log scaling gives larger values
    
    # Logarithmic scaling
    log_min = math.log1p(min_val) if min_val > 0 else 0
    log_max = math.log1p(max_val)
    log_val = math.log1p(value)
    
    scaled = ((log_val - log_min) / (log_max - log_min)) * (max_thickness - min_thickness) + min_thickness
    return scaled * CONSTANT_SCALE

def get_edge_color(value, min_val, max_val):
    """Get the color for an edge based on its value using logarithmic scaling."""
    if max_val == min_val or value <= 0:
        return "#000000"
    
    # Logarithmic scaling
    log_min = math.log1p(min_val) if min_val > 0 else 0
    log_max = math.log1p(max_val)
    log_val = math.log1p(value)
    
    # Scale from 0 to 255 for red component
    scale = (log_val - log_min) / (log_max - log_min)
    red = int(scale * 255)
    
    # Return color in hex format
    return f"#{red:02x}0000"

def visualize_tree(root, output_file='tree_visualization'):
    """Create a graphviz visualization of the tree with edge thickness based on node values."""
    dot = graphviz.Digraph(comment='Tree Visualization')
    dot.attr(rankdir='TB')  # Top to Bottom layout
    
    # Find min and max values for scaling
    min_val, max_val = find_minmax_values(root)
    
    # Queue for BFS traversal: (node, unique_id)
    queue = deque([(root, '0')])
    
    while queue:
        node, node_id = queue.popleft()
        
        # Add node to graph
        dot.node(node_id, str(node.value))
        
        # Process left child
        if node.left:
            left_id = f"{node_id}L"
            queue.append((node.left, left_id))
            thickness = scale_thickness(node.left.value, min_val, max_val)
            color = get_edge_color(node.left.value, min_val, max_val)
            dot.edge(
                node_id,
                left_id,
                penwidth=str(thickness),
                color=color,
                dir='none',
                tailport='s',  # exit from bottom center of the parent
                headport='n'   # enter the top center of the child
            )

        
        # Process right child
        if node.right:
            right_id = f"{node_id}R"
            queue.append((node.right, right_id))
            thickness = scale_thickness(node.right.value, min_val, max_val)
            color = get_edge_color(node.right.value, min_val, max_val)
            dot.edge(
                node_id,
                right_id,
                penwidth=str(thickness),
                color=color,
                dir='none',
                tailport='s',  # exit from bottom center of the parent
                headport='n'   # enter the top center of the child
            )
    
    # Save visualization
    try:
        dot.render(output_file, view=True, format='png')
        print(f"Visualization saved as {output_file}.png")
    except Exception as e:
        print(f"Error saving visualization: {e}")

def main():
    # Create and populate the tree
    root = Node()
    create_random_tree(root, 20)
    run_through_tree(root, 10000)
    
    # Generate visualization
    visualize_tree(root)

if __name__ == "__main__":
    main()