# editor: Wang Zhixiong

import unittest
from hypothesis import given
import hypothesis.strategies as st
from immutable import *


class TestImmutableList(unittest.TestCase):
    def test_api(self) -> None:
        empty = None
        l1 = TreeNode(None, "c", TreeNode(2, "b", TreeNode("a", 1)))
        l2 = TreeNode("a", 1, TreeNode(None, "c", TreeNode(2, "b")))
        self.assertEqual(size(empty), 0)
        self.assertTrue(
            display(l1) in [
                {'a': 1, 2: 'b', None: 'c'}, {'a': 1, None: 'c', 2: 'b'},
                {2: 'b', 'a': 1, None: 'c'}, {2: 'b', None: 'c', 'a': 1},
                {None: 'c', 2: 'b', 'a': 1}, {None: 'c', 'a': 1, 2: 'b'}
            ])
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(display(l1), display(l2))
        self.assertEqual(size(empty), 0)
        self.assertEqual(size(l1), 3)
        self.assertEqual(size(l2), 3)

        self.assertTrue(display(delete(l1, None)) in [
            {2: 'b', 'a': 1}, {'a': 1, 2: 'b'}])
        self.assertTrue(display(delete(l1, 'a')) in [
            {2: 'b', None: 'c'}, {None: 'c', 2: 'b'}])
        self.assertFalse(is_member(empty, None, None))
        self.assertTrue(is_member(l1, None, "c"))
        self.assertTrue(is_member(l1, 'a', 1))
        self.assertTrue(is_member(l1, 2, "b"))
        self.assertFalse(is_member(l1, 3, None))
        self.assertTrue(tolist(l1), iterator(l1)[0])
        self.assertEqual(display(l1),
                         display(fromlist([None, 'c', 'a', 1, 2, 'b'])))
        self.assertEqual(display(mconcat(l1, l2)),
                         display(fromlist([None, 'c',
                                           2, 'B', 'a', 1, 2, 'b'])))
        buf = []
        for e in l1:
            buf.append(e)
        self.assertIn(str(buf), str(iterator(l1)[0]))

        def f(x):
            return x

        lst = tolist(map(l1, f)) + tolist(map(l2, f))
        for e in l1:
            lst.remove(e)
        for e in l2:
            lst.remove(e)
        self.assertEqual(lst, [])

    def test_size(self) -> None:
        self.assertEqual(size(None), 0)
        self.assertEqual(size(TreeNode(3, 'a')), 1)
        self.assertEqual(size(TreeNode(3, 'a', TreeNode(2, 'b'))), 2)
        self.assertEqual(
            size(
                TreeNode(
                    3, 'a', TreeNode(
                        2, 'b'), TreeNode(
                        5, 'c'))), 3)
        tmp = TreeNode(3, 'a', TreeNode("sadf", 'b'), TreeNode(5, 'c'))
        tmp = insert(tmp, "g", "g")
        self.assertEqual(size(tmp), 4)

    def test_insert(self) -> None:
        self.assertEqual(insert(None, 3, 'a').key, 3)
        self.assertEqual(insert(None, 3, 'a').val, 'a')
        self.assertEqual(insert(TreeNode(3, 'a'), 2, 'b').key, 3)
        self.assertEqual(insert(TreeNode(3, 'a'), 2, 'b').val, 'a')
        try:
            insert(TreeNode(3, 'a'), None, 'b')
        except AttributeError as e:
            self.assertEqual(e.args[0], "The element is wrong.")
        try:
            insert(TreeNode(3, 'a'), 2, None)
        except AttributeError as e:
            self.assertEqual(e.args[0], "The element is wrong.")
        self.assertEqual(insert(TreeNode(3, 'a'), 2, 'b').leftChild.key, 2)
        self.assertEqual(insert(TreeNode(3, 'a'), 2, 'b').leftChild.val, 'b')
        self.assertEqual(insert(TreeNode(3, 'a'), 5, 'c').key, 3)
        self.assertEqual(insert(TreeNode(3, 'a'), 5, 'c').val, 'a')
        self.assertEqual(insert(TreeNode(3, 'a'), 5, 'c').rightChild.key, 5)
        self.assertEqual(insert(TreeNode(3, 'a'), 5, 'c').rightChild.val, 'c')

    def test_find(self) -> None:
        T = TreeNode(3, 'a', TreeNode(2, 'b'), TreeNode(5, 'c'))
        self.assertEqual(find(T, 3), 'a')
        self.assertEqual(find(T, 2), 'b')
        self.assertEqual(find(T, 5), 'c')
        self.assertEqual(find(T, 6), False)

    def test_member(self) -> None:
        T = TreeNode(3, 'a', TreeNode(2, 'b'), TreeNode(5, 'c'))
        self.assertEqual(is_member(T, 2, 'b'), True)

    def test_delete(self) -> None:
        T = TreeNode(3, 'a', TreeNode(2, 'b'), TreeNode(5, 'c'))
        self.assertEqual(is_member(T, 2, 'b'), True)
        self.assertEqual(is_member(delete(T, 2), 2, 'b'), False)
        try:
            delete(T, 4)
        except AttributeError as e:
            self.assertEqual(e.args[0], "The element does not exist.")

    def test_tolist(self) -> None:
        T = TreeNode(3, 'a', TreeNode(2, 'b'), TreeNode(5, 'c'))
        self.assertEqual(tolist(T), [3, 'a', 2, 'b', 5, 'c'])

    def test_fromlist(self) -> None:
        lst = [3, 'a', 2, 'b', 5, 'c']
        T = fromlist(lst)
        self.assertEqual(T.val, 'a')
        self.assertEqual(T.leftChild.val, 'b')
        self.assertEqual(T.rightChild.val, 'c')
        lst2 = []
        self.assertEqual(fromlist(lst2), None)
        lst3 = [3, 'a', 2, 'b', 5]
        self.assertEqual(fromlist(lst3), False)

    def test_map(self) -> None:
        T = TreeNode(3, 4, TreeNode(2, 6), TreeNode(5, 7))

        def f(x):
            return x * 2

        map(T, f)
        self.assertEqual(T.key, 3)
        self.assertEqual(T.val, 8)
        lc = T.leftChild
        rc = T.rightChild
        self.assertEqual(lc.key, 2)
        self.assertEqual(lc.val, 12)
        self.assertEqual(rc.key, 5)
        self.assertEqual(rc.val, 14)

    def test_func(self) -> None:
        T = TreeNode(3, 4, TreeNode(2, 6), TreeNode(5, 7))

        def fsum(x, s):
            return s + x

        self.assertEqual(func(T, fsum), 17)

    def test_filter(self) -> None:
        T = TreeNode(3, 4, TreeNode(2, 6), TreeNode(5, 7))

        def r(key):
            return key % 2 == 0

        T_filter = filter(T, r)
        self.assertEqual(T_filter.key, 3)
        self.assertEqual(T_filter.val, 4)
        self.assertEqual(T_filter.leftChild, None)
        self.assertEqual(T.leftChild.key, 2)
        self.assertEqual(T.leftChild.val, 6)
        self.assertEqual(T_filter.rightChild.key, 5)
        self.assertEqual(T_filter.rightChild.val, 7)

    def test_mconcat(self) -> None:
        T1 = TreeNode(3, 4, TreeNode(2, 6), TreeNode(5, 7))
        T2 = TreeNode(1, 8)
        T = mconcat(T1, T2)
        self.assertEqual(tolist(T), [3, 4, 2, 6, 1, 8, 5, 7])

    element = st.one_of(st.integers(), st.text(min_size=1))

    element = st.one_of(st.integers(), st.text(min_size=1))

    @given(st.lists(element))
    def test_from_list_to_list_equality(self, a) -> None:
        if len(a) % 2 == 1:
            self.assertEqual(fromlist(a), False)
        else:
            for i in range(0, len(a), 2):
                for j in range(i + 2, len(a), 2):
                    if type(a[i]) is str:
                        ai_num = 0
                        for k in range(len(a[i])):
                            ai_num = ai_num + ord(a[i][k])
                    else:
                        ai_num = a[i]
                    if type(a[j]) is str:
                        aj_num = 0
                        for k in range(len(a[j])):
                            aj_num = aj_num + ord(a[j][k])
                    else:
                        aj_num = a[j]
                    if ai_num > aj_num:
                        a[i], a[j] = a[j], a[i]
                        a[i + 1], a[j + 1] = a[j + 1], a[i + 1]
            self.assertEqual(tolist(fromlist(a)), a)

    element = st.one_of(st.integers(), st.text(min_size=1))

    @given(st.lists(element))
    def test_monoid_identity(self, lst) -> None:
        if len(lst) % 2 == 1:
            self.assertEqual(fromlist(lst), False)
        else:
            for i in range(0, len(lst), 2):
                for j in range(i + 2, len(lst), 2):
                    if type(lst[i]) is str:
                        lsti_num = 0
                        for k in range(len(lst[i])):
                            lsti_num = lsti_num + ord(lst[i][k])
                    else:
                        lsti_num = lst[i]
                    if type(lst[j]) is str:
                        lstj_num = 0
                        for k in range(len(lst[j])):
                            lstj_num = lstj_num + ord(lst[j][k])
                    else:
                        lstj_num = lst[j]
                    if lsti_num > lstj_num:
                        lst[i], lst[j] = lst[j], lst[i]
                        lst[i + 1], lst[j + 1] = lst[j + 1], lst[i + 1]
            a = fromlist(lst)
            self.assertEqual(tolist(mconcat(mempty(), a)), lst)
            self.assertEqual(tolist(mconcat(a, mempty())), lst)

    element = st.one_of(st.integers(), st.text(min_size=1))

    @given(st.lists(element), st.lists(element), st.lists(element))
    def test_monoid_associativity(self, lst1, lst2, lst3) -> None:
        if len(lst1) % 2 == 1:
            self.assertEqual(fromlist(lst1), False)
        elif len(lst2) % 2 == 1:
            self.assertEqual(fromlist(lst2), False)
        elif len(lst3) % 2 == 1:
            self.assertEqual(fromlist(lst3), False)
        else:
            t1 = fromlist(lst1)
            t2 = fromlist(lst2)
            t3 = fromlist(lst3)
            self.assertEqual(tolist(mconcat(mconcat(t1, t2), t3)),
                             tolist(mconcat(t1, mconcat(t2, t3))))

    def test_iter(self) -> None:
        lst = [3, 'a', 2, 'b', 5, 'c']
        T = fromlist(lst)
        tmp = []
        try:
            it = iterator(T)
            get_next = next_item(it)
            while True:
                tmp.append(get_next())
                tmp.append(get_next())
        except StopIteration:
            pass
        self.assertEqual(lst, tmp)
        self.assertEqual(tolist(T), tmp)
        it = iterator(None)
        get_next = next_item(it)
        self.assertRaises(StopIteration, lambda: get_next())
        i1 = iterator(T)
        i2 = iterator(T)
        self.assertEqual(next_item(i1)(), 3)
        self.assertEqual(next_item(i1)(), 'a')
        self.assertEqual(next_item(i2)(), 3)
        self.assertEqual(next_item(i2)(), 'a')
        self.assertEqual(next_item(i1)(), 2)


if __name__ == '__main__':
    unittest.main()
