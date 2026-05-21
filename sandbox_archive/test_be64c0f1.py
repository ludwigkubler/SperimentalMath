# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def lex_order_complex(edges, n):
        vertices = list(range(n))
        complex = []
        for subset in powerset(vertices):
            if all((u, v) in edges or (v, u) in edges for u, v in combinations(subset, 2)):
                complex.append(sorted(subset))
        return complex
    
    def powerset(s):
        result = [[]]
        for x in s:
            result += [subset + [x] for subset in result]
        return result
    
    def combinations(lst, k):
        if k == 0:
            return [[]]
        if not lst:
            return []
        first, *rest = lst
        return [[first, *tail] for tail in combinations(rest, k - 1)] + combinations(rest, k)
    
    def resolution_length(formula):
        stack = [formula]
        while stack:
            clause = stack.pop()
            if not clause:
                continue
            literal = clause[0]
            new_clauses = []
            for other_clause in stack:
                if literal in other_clause:
                    new_clauses.append([x for x in other_clause if x != literal])
                elif -literal in other_clause:
                    new_clauses.append([x for x in other_clause if x != -literal])
            stack.extend(new_clauses)
        return len(stack)
    
    def tseitin_formula(edges, n):
        literals = {i: (2 * i + 1) for i in range(n)}
        neg_literals = {i: (2 * i + 2) for i in range(n)}
        formula = []
        for u, v in edges:
            formula.append([neg_literals[u], -literals[v]])
            formula.append([-neg_literals[u], literals[v]])
            formula.append([neg_literals[v], -literals[u]])
            formula.append([-neg_literals[v], literals[u]])
        return formula
    
    n = random.randint(5, 40)
    while True:
        graph_edges = generate_random_graph(n)
        if len(graph_edges) >= n * (n - 1) / 2 / 2 and len(graph_edges) <= n * (n - 1) / 2:
            break
    
    complex = lex_order_complex(graph_edges, n)
    ν_G = len(complex)
    
    formula = tseitin_formula(graph_edges, n)
    length = resolution_length(formula)
    
    c = 0.3
    if length >= 2**(c * ν_G):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Graph with {n} vertices and {ν_G} facets, resolution length {length}"
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length:.2f} std={std_length:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")