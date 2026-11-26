#!/usr/bin/env python3
"""Finite census of the class-level edit variant through five vertices."""
from collections import defaultdict
from itertools import combinations, product


def topological_order(parents):
    unseen = set(range(len(parents)))
    ordered = []
    while unseen:
        ready = [i for i in unseen if parents[i].isdisjoint(unseen)]
        if not ready:
            return None
        ordered.extend(ready)
        unseen.difference_update(ready)
    return ordered


def queries(n):
    full = (1 << n) - 1
    for v, w in combinations(range(n), 2):
        allowed = full ^ (1 << v) ^ (1 << w)
        s = allowed
        while True:
            yield v, w, s
            if not s:
                break
            s = (s - 1) & allowed


def mask(indices):
    return sum(1 << i for i in indices)


def signature(parents, order, tests):
    n = len(parents)
    ancestor_masks = [0] * n
    for i in order:
        ancestor_masks[i] = 1 << i
        for p in parents[i]:
            ancestor_masks[i] |= ancestor_masks[p]
    ancestors = [0] * (1 << n)
    for sub in range(1, 1 << n):
        bit = sub & -sub
        ancestors[sub] = ancestors[sub ^ bit] | ancestor_masks[bit.bit_length() - 1]
    family = [mask(pa) | (1 << i) for i, pa in enumerate(parents)]
    clique_nodes = [tuple(pa | {i}) for i, pa in enumerate(parents)]
    cache = {}
    result = 0
    for k, (v, w, s) in enumerate(tests):
        vm, wm = 1 << v, 1 << w
        key = ancestors[s | vm | wm]
        if key not in cache:
            linked = [0] * n
            for i in range(n):
                if key & (1 << i):
                    for j in clique_nodes[i]:
                        linked[j] |= family[i] ^ (1 << j)
            cache[key] = linked
        graph = cache[key]
        seen = vm | s
        frontier = vm
        while frontier and not seen & wm:
            bit = frontier & -frontier
            new = graph[bit.bit_length() - 1] & ~seen
            seen |= new
            frontier = (frontier ^ bit) | new
        if not seen & wm:
            result |= 1 << k
    return result


def census(n):
    pairs = tuple(combinations(range(n), 2))
    tests = tuple(queries(n))
    coding = {}
    for edges in product(range(3), repeat=len(pairs)):
        pa = [set() for _ in range(n)]
        for (i, j), state in zip(pairs, edges):
            if state == 1:
                pa[j].add(i)
            if state == 2:
                pa[i].add(j)
        order = topological_order(pa)
        if order is not None:
            coding[edges] = signature(pa, order, tests)
    signatures = set(coding.values())
    by_class = defaultdict(lambda: len(tests) + 1)
    for edges, source in coding.items():
        if by_class[source] == 1:
            continue
        possible = [by_class[source]]
        for i, state in enumerate(edges):
            for other in range(3):
                if state == other:
                    continue
                neighbor = coding.get(edges[:i] + (other,) + edges[i+1:])
                if neighbor is not None and source != neighbor:
                    possible.append((source ^ neighbor).bit_count())
        by_class[source] = min(possible)
    global_min = {}
    for source, edit in by_class.items():
        least = 1 if edit == 1 else min((source ^ alt).bit_count() for alt in signatures if source != alt)
        assert edit == least, (n, source, edit, least)
        global_min[source] = least
    assert set(by_class) == signatures and len(tests) + 1 not in by_class.values()
    return len(coding), len(signatures), max(global_min.values())


def main():
    expected = [(3, 2), (25, 11), (543, 185), (29281, 8782)]
    for n, counts in enumerate(expected, start=2):
        dags, classes, radius = census(n)
        assert (dags, classes) == counts
        print(f"n={n}: {dags:,} DAGs; {classes:,} signatures; maximal nearest distance {radius}", flush=True)


if __name__ == "__main__":
    main()
