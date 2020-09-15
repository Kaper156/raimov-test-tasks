# Тестовое задание №1.
# Напишите алгоритм полного обхода дерева (связный граф, не содержащий циклы). Дерево представлено в виде словаря.

test_tree = {
    'data': 0,
    'left': {
        'data': 0
    },
    'right': {
        'data': 0
    }
}


def build_tree(tree, depth):
    data_generator = iter(range(0, 256))
    # while depth > 0:
    #     tree


def add_leafs(tree, data):
    pass


def look_inner(tree, depth=0, name='root'):
    print("\t" * depth + f"{name}:")
    depth += 1
    for name, inner in tree.items():
        if type(inner) is dict:
            look_inner(inner, depth=depth, name=name)
        else:
            print("\t" * depth + f"[DATA]{name}:{inner}")


def main():
    tree = dict()
    build_tree(tree, 5)
    tree = test_tree
    # for depth, data in look_inner(tree):
    # eval('nanl21 / "d"')
    look_inner(tree)


if __name__ == '__main__':
    main()
