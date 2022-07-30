class Node:
    def __init__(self,key):
        self.val=key
        self.left=None
        self.right=None
        
def LevelOrder(root):
    if root==None:
        return
    queue=[]
    queue.append(root)
    while(len(queue)>0):
        print(queue[0].val)
        node = queue.pop(0)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
            
def LevelOrderAdv(root):
    if root==None:
        return
    queue=[]
    queue.append(root)
    queue.append(None)
    while (len(queue)>0):
        node = queue.pop(0)
        if node==None:
            print("\n")
            if len(queue)==0:
                break
            else:
                queue.append(None)
        else:
            print(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
            
    

root= Node(1)
root.left=Node(2)
root.right=Node(3)
root.left.left=Node(4)
root.left.right=Node(5)
root.right.right=Node(6)
print(LevelOrderAdv(root))