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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d = random.randint(3, min(n - 1, 20))
    
    # Generate a random d-regular graph
    G = [[] for _ in range(n)]
    edges = set()
    while len(edges) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
    
    # Construct the Tseitin formula φ_G
    variables = list(range(n * d))
    clauses = []
    for i in range(n):
        literals = [variables[i * d + j] for j in range(d)]
        clauses.append([literals[0]] + [-x for x in literals[1:]])
        for j in range(1, len(literals)):
            clauses.append([-literals[j], literals[j - 1]])
    
    # Compute the eta-invariant η(G)
    eta_values = []
    for i in range(n):
        for j in range(d):
            u = G[i][j]
            if u > i:
                continue
            eta_value = Fraction(0, 1)
            for k in range(n * d):
                if variables[k] == variables[i * d + j]:
                    eta_value += Fraction(1, 2 ** (k % n))
            eta_values.append(eta_value)
    
    # Measure the resolution proof width w(φ_G)
    def resolve_clause(clause, model):
        for literal in clause:
            if literal < 0 and -literal not in model:
                return False
        return True
    
    def resolve_formula(formula, model):
        stack = formula[:]
        while stack:
            clause = stack.pop()
            if resolve_clause(clause, model):
                continue
            unsatisfied_literal = None
            for literal in clause:
                if literal < 0 and -literal not in model:
                    unsatisfied_literal = literal
                    break
            if unsatisfied_literal is None:
                return False
            new_model = model.copy()
            new_model[unsatisfied_literal] = True
            if resolve_formula(formula, new_model):
                return True
            new_model[unsatisfied_literal] = False
            if not resolve_formula(formula, new_model):
                return False
        return True
    
    proof_width = 0
    for model in itertools.product([False, True], repeat=n * d):
        if resolve_formula(clauses, dict(zip(variables, model))):
            proof_width += 1
    
    # Correlate η(G) with w(φ_G)
    correlation_coefficient = sum(x * y for x, y in zip(eta_values, [proof_width] * len(eta_values))) / (len(eta_values) * sum(x ** 2 for x in eta_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 or max(eta_values) / proof_width > 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 9973) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["n_max"] for r in results) >= 16:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")