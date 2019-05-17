import json
from collections import defaultdict


def tree():
    return defaultdict()


class cus_tree:
    """
    树节点
    """

    def __init__(self, _name, _children):
        self.name = _name
        self.children = _children


if __name__ == "__main__":
    category = []
    category.append(cus_tree("baidu.com", []))
    
    category[0].children.append(cus_tree("guoneixinwen",[]))
    category[0].children.append(cus_tree("guojixinwen",[]))
    category[0].children.append(cus_tree("shehuixinwen",[]))

    print(category[0].children)
