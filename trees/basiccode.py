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
        
def height(root):
    if root ==None:
        return 0
    lefty= height(root.left)
    righty= height(root.right)
    return max(lefty,righty)+1

def total(root):
    if root==None:
        return 0
    lefty = total(root.left)
    righty = total(root.right)
    return lefty+righty+1

def sum (root):
    if root==None:
        return 0
    lefty=sum(root.left)
    righty=sum(root.right)
    return lefty+righty+root.val

def diameter(root):
    if root==None:
        return 0
    lefty = diameter(root.left)
    righty = diameter(root.right)
    dia = height(root.left)+height(root.right)+1
    return max(dia , max(lefty,righty))


        
root= Node(1)
root.left=Node(2)
root.right=Node(3)  
root.left.left=Node(4)
root.left.right=Node(5)
root.right.right=Node(6)
#print(Inorder(root))
print (diameter(root))