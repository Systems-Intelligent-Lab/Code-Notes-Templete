def append_item(item, lst=None):
    """Append an item to a list, creating a new list by default.

    This示例用于说明为什么不推荐在函数定义里使用可变对象作为默认参数。
    """
    if lst is None:
        lst = []
    lst.append(item)
    return lst


if __name__ == "__main__":
    print(append_item(1))       # [1]
    print(append_item(2))       # [2] - 不会和上一次共用列表

