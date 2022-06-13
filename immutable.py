# editor: Wang Zhixiong
from typing import TypeVar, Generic, List, Iterator
from typing import Any
from typing import Union
from typing import Generator
from typing import Callable

K = Union[str, int, float]
D = Union[None, str, int, float]


class TreeNode:
    def __init__(self, k: K, v: D,
                 left: object = None,
                 right: object = None) -> None:
        self.key = k  # key
        self.val = v  # value
        self.leftChild = left  # left pointer
        self.rightChild = right  # right pointer

    def __iter__(self) -> Iterator[Any]:
        return iter(tolist(self))


def size(bst: Union[TreeNode, None]) -> Optional[TreeNode]:
    if bst is None:
        return 0
    else:
        return 1 + size(bst.leftChild) + size(bst.rightChild)


def insert(bst: Union[TreeNode, None], key: K,
           val: D) -> Optional[TreeNode]:
    if bst is None:
        bst = TreeNode(key, val)
    elif key is None or val is None:
        if bst.leftChild is None:
            bst.leftChild = TreeNode(key, val)
        else:
            if bst.rightChild is None:
                bst.rightChild = TreeNode(key, val)
        # raise AttributeError("The element is wrong.")
    elif bst.key is None:
        if bst.leftChild is None:
            bst.leftChild = TreeNode(key, val)
        else:
            if bst.rightChild is None:
                bst.rightChild = TreeNode(key, val)
    else:
        if isinstance(key, str):
            key_num = 0
            for i in range(len(key)):
                key_num = key_num + ord(key[i])
        else:
            key_num = key  # type: ignore
        if isinstance(bst.key, str):
            bstkey_num = 0
            for i in range(len(bst.key)):
                bstkey_num = bstkey_num + ord(bst.key[i])
        else:
            bstkey_num = bst.key  # type: ignore
        if key_num <= bstkey_num:
            if bst.leftChild is None:
                bst.leftChild = TreeNode(key, val)
            else:
                insert(bst.leftChild, key, val)
        else:
            if bst.rightChild is None:
                bst.rightChild = TreeNode(key, val)  # type: ignore
            else:
                insert(bst.rightChild, key, val)
    return bst


def get(bst: Union[TreeNode, None], key: K) -> Union[TreeNode, None]:
    if bst is None:
        return None
    if type(bst.key) != key:
        if get(bst.leftChild, key) is not None:
            return get(bst.leftChild, key)
        if get(bst.rightChild, key) is not None:
            return get(bst.rightChild, key)
    if key == bst.key:
        return bst


def find(bst: Union[TreeNode, None],
         key: K) -> Union[D, bool]:
    if get(bst, key) is None:
        return False
    else:
        return get(bst, key).val  # type: ignore


def parent(bst: Union[TreeNode, None],
           key: K) -> Union[TreeNode, None]:
    if bst is None or bst.key == key:
        return None
    elif key == bst.leftChild.key or key == bst.rightChild.key:
        return bst
    elif key < bst.key:
        return parent(bst.leftChild, key)
    else:
        return parent(bst.rightChild, key)


def is_member(bst: Union[TreeNode, None],
              k: K, v: D) -> bool:
    if find(bst, k) == v:
        return True
    else:
        return False


def delete(bst: Union[TreeNode, None],
           key: K) -> None:
    res = tolist(bst)
    res1 = res[0::2]
    index = None
    for i in range(0, len(res1)):
        if key == res1[i]:
            index = i
    res2 = res[1::2]
    if index is None:
        raise AttributeError("The element does not exist.")
    del res[index * 2 + 1]
    del res[index * 2]
    return fromlist(res)


def tolist(bst: Union[TreeNode, None]) -> List:
    res = []  # type: ignore

    def tolist_loop(bst, ans):
        if bst is not None:
            ans.append(bst.key)
            ans.append(bst.val)
            ans = tolist_loop(bst.leftChild, ans)
            ans = tolist_loop(bst.rightChild, ans)
        return ans

    return tolist_loop(bst, res)


def fromlist(lst: List) -> Union[TreeNode, None, bool]:
    bst = None
    if len(lst) == 0:
        return None
    elif len(lst) % 2 == 1:
        return False
    for i in range(0, len(lst)):
        for j in range(0, len(lst)):
            if lst[i] == lst[j] and i % 2 == 0 and j % 2 == 0:
                lst[i + 1] = lst[j + 1]
    else:
        for i in range(0, len(lst), 2):
            bst = insert(bst, lst[i], lst[i + 1])
        return bst


def map(bst: Union[TreeNode, None],
        f: Callable[[float], float]) -> TreeNode:
    if bst is not None and bst.key is not None:
        bst.val = f(bst.val)
        map(bst.leftChild, f)
        map(bst.rightChild, f)
    return bst


def func(bst: Union[TreeNode, None],
         f: Callable[[float], float]) -> int:
    ans = [0]

    def func_loop(bst, f, ans):
        if bst is not None:
            ans[0] = f(ans[0], bst.val)
            func_loop(bst.leftChild, f, ans)
            func_loop(bst.rightChild, f, ans)
        return ans

    return func_loop(bst, f, ans)[0]


def filter(tree: Union[TreeNode, None],
           rule: Generator[str, int, float]) -> Union[TreeNode, None]:
    bst = None

    def filter_loop(bst, current, rule):
        if current is not None:
            if rule(current.key) is False:
                bst = insert(bst, current.key, current.val)
            bst = filter_loop(bst, current.leftChild, rule)
            bst = filter_loop(bst, current.rightChild, rule)
        return bst

    return filter_loop(bst, tree, rule)


def mconcat(bst1: Union[TreeNode, None],
            bst2: Union[TreeNode, None]) -> Union[TreeNode, None, bool]:
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
        if cur >= len(lst) or lst == []:
            raise StopIteration
        tmp = lst[cur]
        cur = cur + 1
        it_lst[1] = it_lst[1] + 1
        return tmp

    return foo


def display(bst: Union[TreeNode, None]) -> dict:
    if bst is None:
        return {}
    else:
        a = tolist(bst)
        b = dict(zip(a[0::2], a[1::2]))
        return b
