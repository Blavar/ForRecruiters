functions = ['D', 'sin', 'cos', 'ln']
operators = ['^', '*', '/', '+', '-']
special_symbols = '()[]:,^*/+-'


class Node:
    def __init__(self):
        self.type     = None
        self.val      = None
        self.parent   = None
        self.children = []

    def add_child( self, node ):
        self.children.append( node )
        node.parent = self

    def __repr__(self):
        res = ''
        if self.type == 'func':
            res += self.val + '('
            for child in self.children:
                res += str(child) + ','
            res = res[:-1] + ')'

        elif self.type == 'operator':
            if self.children:
                res += '(' + str(self.children[0]) + ' ' + str(self.val) + ' ' + str(self.children[1]) + ')'
            else:
                res += str(self.val)

        else:
            res += str(self.val)


        return res