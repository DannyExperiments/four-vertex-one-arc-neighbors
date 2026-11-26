from itertools import combinations, permutations

V=range(4)
D=frozenset({(0,1),(0,2),(0,3),(1,2)})
H=frozenset({(1,0),(2,0),(0,3)})
D2=frozenset({(1,0),(2,0),(0,3),(1,2)})

def acyclic(E):
    for order in permutations(V):
        if all(order.index(x)<order.index(y) for x,y in E):
            return True
    return False

def parents(E,S):
    A=set(S)
    while True:
        B=A|{x for x,y in E if y in A}
        if A==B: return A
        A=B

def connected(E,u,v,S):
    A=parents(E,S)
    inner=[x for x in V if x not in (u,v)]
    for k in range(len(inner)+1):
        for mid in permutations(inner,k):
            path=(u,*mid,v)
            if not all((a,b) in E or (b,a) in E for a,b in zip(path,path[1:])):
                continue
            if all((y in A) if (x,y) in E and (z,y) in E else (y not in S)
                   for x,y,z in zip(path,path[1:],path[2:])):
                return True
    return False

def sep(E):
    C=set()
    for u,v in combinations(V,2):
        rem=set(V)-{u,v}
        for k in range(len(rem)+1):
            for S in combinations(sorted(rem),k):
                if not connected(E,u,v,S):
                    C.add((u,v,S))
    return C

C=sep(D)
assert C=={(1,3,(0,)),(1,3,(0,2)),(2,3,(0,)),(2,3,(0,1))}
assert sep(H)^C=={(1,2,())}
assert sep(D2)==C and D2-{(1,2)}==H
expected={"add": [3,3,3,3], "delete":[2,3,3,8], "reverse":[0,0,0]}
groups={k:[] for k in expected}
for u,v in combinations(V,2):
    arcs={(u,v),(v,u)}
    old=D&arcs
    for new in (set(),{(u,v)},{(v,u)}):
        if new==old: continue
        T=(D-arcs)|new
        k=("add" if not old else "delete" if not new else "reverse")
        if not acyclic(T):
            print(k, u,v, "cyclic")
            continue
        dist=len(C^sep(T))
        groups[k].append(dist)
        print(k, old, "to", new, "d =", dist, "queries:", sorted(C^sep(T)))
assert {k:sorted(v) for k,v in groups.items()}==expected
positive=[x for v in groups.values() for x in v if x>0]
assert min(positive)==2
print("Exact certificate passed: global minimum 1, best positive one-edit distance 2.")
