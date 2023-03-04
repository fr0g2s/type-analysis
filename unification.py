
import re

class Term:
    typeVar_pattern = r"\[\[([^\[\]]*)\]\]"   # [[..]] 
    proper_pattern = {"int" : "int", "pointer":"↑", "function": r"\(.*?\) ->"} 
        
    def __init__(self, term: str):
        self.term: str = term
        self.subterms, self.type = self.parse_term(term)
        self.isTypeVar = self.__isTypeVar(term)
        self.isProperType = self.__isProperType(term)
        
    def strToTerm(self, t: str):
        return Term(t)
    
    def parse_term(self, t: str):
        t_subterms = ""
        t_type = ""
        for type, pattern in self.proper_pattern.items():
            match = re.match(pattern, t)
            if match:
                if type == "pointer":
                    t_subterms = t[t.find(pattern) + len(pattern):]
                else:
                    t_subterms = None
                t_type = type
                break
        if t_subterms == "":
            return None, None
        else:
            return t_subterms, t_type
    
    def __isTypeVar(self, t):
        return self.type is None

    def __isProperType(self, t):
        return self.type is not None

class Unificator:
    def __init__(self, terms: list):
        self.parents = {}
        for t in terms:
            self.Makeset(t)
        self.term_list = [t.term for t in terms]

    def Makeset(self, x: Term):
        self.parents[x.term] = x

    def Find(self, x: Term) -> Term:
        parent = self.parents[x.term]
        if parent.term != x.term:
            self.parents[x.term] = self.Find(parent) # 부모를 탐색하면서 동시에 중간 노드들의 부모를 정식 대표자로 지정한다.
        return self.parents[x.term]

    def Union(self, x: Term, y: Term):
        x_r = self.Find(x)
        y_r = self.Find(y)
        if x_r.term != y_r.term:
            self.parents[x_r.term] = y_r

    def isSameConstructor(self, x: Term, y: Term):
        return x.type == y.type

    def isBothTypeVar(self, x: Term, y: Term):
        return x.isTypeVar and y.isTypeVar

    def isBothProper(self, x: Term, y: Term):
        return not self.isBothTypeVar(x, y)

    def __unify(self, x: Term, y: Term):
        x_r = self.Find(x)
        y_r = self.Find(y)
        if x_r != y_r:
            if self.isBothTypeVar(x_r, y_r):
                self.Union(x_r, y_r)
            elif x_r.isTypeVar and y_r.isProperType:
                self.Union(x_r, y_r)
            elif x_r.isProperType and y_r.isTypeVar:
                self.Union(y_r, x_r)
            elif self.isBothProper(x_r, y_r) and self.isSameConstructor(x_r, y_r):
                self.Union(x_r, y_r)
                x_subterms = x_r.subterms
                y_subterms = y_r.subterms
                for i in range(0, len(x_subterms), 1): # x_r과 y_r의 sub-term 개수가 같음. Same Constructor이기 때문.
                    x_subterm = x_r.strToTerm(x_subterms)
                    y_subterm = y_r.strToTerm(y_subterms)
                    self.__unify(x_subterm, y_subterm)
            else:
                raise Exception("not typable")

    def run(self):
        if len(self.parents) == 0:
            print('[*] no exist node')
        else:
            for i in range(0, len(self.term_list), 2):
                x1 = self.parents[self.term_list[i]]
                x2 = self.parents[self.term_list[i+1]]
                self.__unify(x1, x2)


