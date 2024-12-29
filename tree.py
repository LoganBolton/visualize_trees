import random
from collections import deque
class Node:
    def __init__ (self):
        self.value = 0
        self.left = None
        self.right = None
    def add_children(self):
        self.left = Node()
        self.right = Node()
    
root = Node()

def create_balanced_tree(root, max_level):
    queue = deque([root])
    levels = 0
    while levels < max_level:
        for _ in range(len(queue)):
            curr = queue.popleft()
            curr.add_children()
            queue.append(curr.left)
            queue.append(curr.right)
        levels += 1

def create_random_tree(root, max_level):
    queue = deque([root])
    REPRODUCTION_RATE = 0.6
    levels = 0
    while levels < max_level:
        for _ in range(len(queue)):
            curr = queue.popleft()
            if random.random() < REPRODUCTION_RATE:
                curr.left = Node()
                queue.append(curr.left)
            if random.random() < REPRODUCTION_RATE:
                curr.right = Node()
                queue.append(curr.right)
                
        levels += 1

def print_tree(root):
    level = 0
    queue = deque([root])
    while len(queue) > 0:
        print("Level: ", level)
        for _ in range(len(queue)):
            curr = queue.popleft()
            print(curr.value)
            if curr.left is not None:
                queue.append(curr.left)
            if curr.right is not None:
                queue.append(curr.right)
        level += 1
        
def run_through_tree(root, runs):
    for _ in range(runs):
        curr = root
        while curr is not None:
            curr.value += 1
            if random.randint(0,1) == 0:
                curr = curr.left
            else:
                curr = curr.right

# create_balanced_tree(root, 3) 
# run_through_tree(root, 100)
# print_tree(root)