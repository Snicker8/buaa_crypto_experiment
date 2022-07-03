from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

# 先import对应程序的main()函数
# ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
# from ex#/c#.py import main

if __name__ == '__main__':
    graphviz = GraphvizOutput()
    graphviz.output_file = 'ex#/c#' + '.png'
    with PyCallGraph(output=graphviz):
        # 直接运行main()
        # ↓ ↓ ↓
        # main()
