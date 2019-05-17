import json
from collections import defaultdict


def tree():
    return defaultdict()


if __name__ == "__main__":
    category = {}
    category["guoneixinwen"] = ""
    category["guojixinwen"] = ""
    category["shehuixinwen"] = ""

    category["guoneixinwen"] = {"hunan": "", "jiangxi": ""}
    category["guojixinwen"] = {"meiguo": "", "jianada": "", "yinguo": ""}

    #print(category)

    cat = ["guoneixinwen", "guojixinwen", "shehuixinwen"]
    
    cat[0].append(["hunan", "jiangxi"])
    cat[1] = ["meiguo", "yingguo", "deguo"]

    print(cat)
