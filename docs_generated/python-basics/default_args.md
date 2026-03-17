# Python 函数默认参数示例

下面展示 `default_args.py` 中的 `append_item` 函数，代码来自真实的 `.py` 文件，而不是写在 Markdown 里。

```python
def append_item(item, lst=None):
    """Append an item to a list, creating a new list by default.

    This示例用于说明为什么不推荐在函数定义里使用可变对象作为默认参数。
    """
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

你只需要维护 `python-demos/basics/default_args.py` 中的代码，这里的函数会在构建时自动同步。

