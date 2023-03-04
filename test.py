from unification import *

constraints = """
[[short]] = ()->[[z]]
[[input]] = int
[[x]] = [[input]]
[[alloc x]] = ↑[[x]]
[[y]] = [[alloc x]]
[[y]] = ↑[[x]]
[[z]] = [[*y]]
[[z]] = ↑[[y]]
[[y]] = ↑[[*y]]
"""

expected_reuslt = """
[[short]] = ()->int
[[x]] = int
[[y]] = ↑int
[[z]] = int
"""

t_list = []
for line in constraints.split("\n"):
    if len(line) == 0:
        continue
    line = line.split(" = ")
    x1 = line[0]
    x2 = line[1]
    t_list.append(Term(x1))
    t_list.append(Term(x2))

u = Unificator(t_list)

u.run()

for term, parent in u.parents.items():
    print(term, parent.term)
# import code
# code.interact(local=locals())