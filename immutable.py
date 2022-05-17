# editor: Zhuo lin
from typing import TypeVar, Generic, List, Iterator, Callable, Generator, Union, Any

class TreeNode:
	def __init__(self,key,val,left=None,right=None):	
		self.key = key
		self.val = val
		self.leftChild = left
		self.rightChild = right

key_type = TypeVar('key_type', str, int, float)
val_type = TypeVar('val_type', None, str, int, float)
node_type = TypeVar('node_type', None, TreeNode)

def size(bst: Union[TreeNode, None]) -> int:
    if bst is None:
        return 0
    else:
        return 1 + size(bst.leftChild) + size(bst.rightChild)

def insert(bst: Union[TreeNode, None], key: key_type, val: val_type) -> TreeNode:
    if key == None or val == None:
        raise AttributeError("The element is wrong.")
    if bst is None:
        bst = TreeNode(key,val)
    else:
        if type(key) is str:
            key_num = 0
            for i in range(len(key)):  #type: ignore
                key_num = key_num + ord(key[i])  #type: ignore
        else:
            key_num = key  #type: ignore
        if type(bst.key) is str: 
            bstkey_num = 0
            for i in range(len(bst.key)):
                bstkey_num = bstkey_num + ord(bst.key[i])
        else:
            bstkey_num = bst.key
        if key_num <= bstkey_num:
            if bst.leftChild is None:
                bst.leftChild = TreeNode(key,val)
            else:
                insert(bst.leftChild,key,val)
        else:
            if bst.rightChild is None:
                bst.rightChild = TreeNode(key,val)
            else:
                insert(bst.rightChild,key,val)
    return bst

def get(bst: Union[TreeNode, None], key: key_type) -> Union[TreeNode, None]:
    if bst is None:
        return None
    elif key ==  bst.key:
        return bst
    elif key < bst.key:
        return get(bst.leftChild,key)
    else:
        return get(bst.rightChild,key)

def find(bst: Union[TreeNode, None], key: key_type) -> Union[val_type, bool]:
    if get(bst,key) == None:
        return False
    else:
        return get(bst,key).val #type: ignore

def parent(bst: Union[TreeNode, None], key: key_type) -> Union[TreeNode, None]:
    if bst is None or bst.key == key:
        return None
    elif key ==  bst.leftChild.key or key ==  bst.rightChild.key:
        return bst
    elif key < bst.key:
        return parent(bst.leftChild,key)
    else:
        return parent(bst.rightChild,key)

def is_member(bst: Union[TreeNode, None], k: key_type, v: val_type) -> bool:
    if find(bst,k) == v:
        return True
    else:
        return False

def delete(bst: Union[TreeNode, None], key: key_type) -> None:
    n = get(bst,key)
    if n == None:
        raise AttributeError("The element does not exist.")
    p = parent(bst,key)
    if n.leftChild is None: #type: ignore
        if n == p.leftChild: #type: ignore
            p.leftChild = n.rightChild #type: ignore
        else:
            p.rightChild = n.rightChild #type: ignore
        del n
    elif n.rightChild is None: #type: ignore
        if n == p.leftChild: #type: ignore
            p.leftChild = n.leftChild #type: ignore
        else: 
            p.rightChild = n.leftChild #type: ignore
    else:
        pre = n.rightChild #type: ignore
        if pre.leftChild is None:
            n.key = pre.key #type: ignore
            n.val = pre.val #type: ignore
            n.rightChild = pre.rightChild #type: ignore
            del pre
        else:
            temp = pre.leftChild
            while temp.leftChild is not None:
                pre = temp
                temp = temp.leftChild
            n.key = temp.key #type: ignore
            n.val = temp.val #type: ignore
            pre.leftChild = temp.rightChild
            del temp

def tolist(bst: Union[TreeNode, None]) -> List:
    res = []  #type: ignore
    def tolist_loop(bst,ans):
        if bst is not None:
            ans.append(bst.key)
            ans.append(bst.val)
            ans = tolist_loop(bst.leftChild,ans)
            ans = tolist_loop(bst.rightChild,ans)
        return ans
    return tolist_loop(bst, res)

def fromlist(lst: List) -> Union[TreeNode, None, bool]:
    bst = None
    if len(lst) == 0:
        return None
    elif len(lst) % 2 == 1:
        return False
    else:
        for i in range(0,len(lst),2):
            bst = insert(bst,lst[i],lst[i+1])
        return bst

def map(bst: Union[TreeNode, None], f: Callable[[float],float]) -> None:
    if bst is not None:
        bst.val = f(bst.val)
        map(bst.leftChild,f)
        map(bst.rightChild,f)

def func(bst: Union[TreeNode, None], f: Callable[[float],float]) -> int:
    ans = [0]
    def func_loop(bst,f,ans):
        if bst is not None:
            ans[0] = f(ans[0], bst.val)
            func_loop(bst.leftChild,f,ans)
            func_loop(bst.rightChild,f,ans)
        return ans
    return func_loop(bst,f,ans)[0]

def filter(tree: Union[TreeNode, None], rule: Generator[str, int, float]) -> Union[TreeNode, None]:
    bst = None
    def filter_loop(bst,current,rule):
        if current is not None:
            if rule(current.key) is False:
                bst = insert(bst,current.key,current.val)
            bst = filter_loop(bst,current.leftChild,rule)
            bst = filter_loop(bst,current.rightChild,rule)
        return bst
    return filter_loop(bst, tree, rule)

def mconcat(bst1: Union[TreeNode, None], bst2: Union[TreeNode, None]) -> Union[TreeNode, None, bool]:
    lst1 = tolist(bst1)
    lst2 = tolist(bst2)
    lst = lst1 + lst2
    return fromlist(lst)

def mempty() -> None:
    return None

def iterator(bst: Union[TreeNode, None]) -> List:
    return [tolist(bst), 0]

def next_item(it_lst: List) -> Callable[[], Any]:
    lst = it_lst[0]
    cur = it_lst[1]
    def foo():
        nonlocal cur
        if cur >= len(lst) or lst == []: raise StopIteration
        tmp = lst[cur]
        cur = cur + 1
        it_lst[1] = it_lst[1] + 1
        return tmp
    return foo