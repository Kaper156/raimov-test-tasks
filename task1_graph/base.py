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
    # В проверке на None теперь нет необходимости,
    # предполагается что (под)дерево имеет значения по ключу data,
    # а в остальных ключах хранятся поддеревья
    print("\t" * depth + f"{name}:{tree['data']}")
    # for name, inner_tree in [(name, inner_tree) for name, inner_tree in tree.items() if name != 'data']:
    for name, inner_tree in tree.items():
        if name != 'data':
            look_inner(inner_tree, depth=depth + 1, name=name)


def main():
    tree = dict()
    build_tree(tree, 5)
    tree = test_tree
    # for depth, data in look_inner(tree):
    # eval('nanl21 / "d"')
    look_inner(tree)


if __name__ == '__main__':
    main()
