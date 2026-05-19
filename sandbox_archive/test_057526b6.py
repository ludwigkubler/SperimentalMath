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
    
    def treewidth(G):
        # Implement a simple heuristic to estimate treewidth (e.g., BFS-based)
        n = len(G)
        if n == 0:
            return 0
        queue = [set([i]) for i in range(n)]
        while queue:
            current = queue.pop()
            neighbors = set.union(*[G[i] for i in current])
            if len(neighbors) > len(current):
                return len(current)
            queue.append(neighbors - current)
        return 0

    def tseitin_formula(G, root):
        # Generate Tseitin formula for a given tree decomposition
        n = len(G)
        formulas = {}
        variables = {i: f"x{i}" for i in range(n)}
        for node in G:
            if len(node) == 1:
                formulas[node[0]] = variables[node[0]]
            else:
                new_var = f"y{len(formulas)}"
                formulas[new_var] = f"{variables[node[0]]} ∨ {variables[node[1]]}"
                for i in range(2, len(node)):
                    formulas[new_var] += f" ∧ ¬{formulas[f'y{i-1}']}"
        return formulas[root]

    def resolution_length(formula):
        # Implement a simple resolution refutation length estimator
        clauses = formula.split(" ∧ ")
        new_clauses = set()
        while True:
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    c1 = clauses[i].split(" ∨ ")
                    c2 = clauses[j].split(" ∨ ")
                    for p in c1:
                        if f"¬{p}" in c2:
                            new_clause = [q for q in c1 if q != p] + [q for q in c2 if q != f"¬{p}"]
                            new_clauses.add(" ∨ ".join(new_clause))
                            found_resolvent = True
            if not found_resolvent:
                break
            clauses.extend(list(new_clauses))
            new_clauses.clear()
        return len(clauses)

    n = random.randint(5, 40)
    G = {i: set() for i in range(n)}
    root = random.choice(range(n))
    for _ in range(n - 1):
        u, v = random.sample(range(n), 2)
        if u not in G[v]:
            G[u].add(v)
            G[v].add(u)

    tw = treewidth(G)
    formula = tseitin_formula(G, root)
    length = resolution_length(formula)

    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (tw * 0.5),
        "counterexample": "" if length >= 2 ** (tw * 0.5) else f"Graph with treewidth {tw} has refutation length {length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")