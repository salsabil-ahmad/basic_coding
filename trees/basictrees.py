class Node:
    def __init__(self,key):
        self.val=key
        self.left=None
        self.right=None
        
def Inorder(root):
    if root:
        Inorder(root.left)
        print(root.val)
        Inorder(root.right)
def Postorder(root):
    if root:
        Postorder(root.left)
        Postorder(root.right) 
        print(root.val)  
def Preorder(root):
    if root:
        print(root.val) 
        Preorder(root.left)
        Preorder(root.right) 

root= Node(1)
root.left=Node(2)
root.right=Node(3)
root.left.left=Node(4)
root.left.right=Node(5)
print(Inorder(root))
