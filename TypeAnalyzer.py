import unification

source_code = """
    short() {
	var x, y, z;
	x = input;
	y = alloc x;
	*y = x;
	z = *y;
	return z;
}
"""
expected_reuslt = """
[[short]] = ()->int
[[x]] = int
[[y]] = ↑int
[[z]] = int
"""

class TypeAnalyzer:
    def __init__(self, target):
        self.target = target
        self.constraints = self.make_constraints(target)   
        self.analyzer = unification.Unificator(self.parsing_terms(self.constraints))
        self.result = ""

    def parsing_terms(self, constraints):
        t_list = []
        separator = " = "
        for line in constraints.split("\n"):
            if len(line) == 0:
                continue
            line = line.split(separator)
            x1 = line[0]
            x2 = line[1]
            t_list.append(unification.Term(x1))
            t_list.append(unification.Term(x2))
        return t_list

    def make_AST(self, target):
        pass

    def make_constraints(self, target):
        self.make_AST(target) # constraints는 AST를 탐색하여 만드는게 정석이다. 추후 개발 가능성을 고려하여 추가만 해놓음.
        constraints = """
[[short]] = ()->[[z]]
[[input]] = int
[[x]] = [[input]]
[[alloc x]] = ↑[[x]]
[[y]] = [[alloc x]]
[[y]] = ↑[[x]]
[[z]] = [[*y]]
[[y]] = ↑[[*y]]
"""
        return constraints

    def run(self):
        self.analyzer.run()
        for term, parent in self.analyzer.parents.items():
            self.result += term + ' ' + parent.term + '\n'

def main():
    ta = TypeAnalyzer(target = source_code)
    ta.run()
    print(ta.result)

if __name__ == "__main__":
    main()