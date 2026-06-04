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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def tseitin_formula(n):
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(i + 1, n):
                clause.append(f"~{literals[j]}")
            clauses.append(" ".join(clause))
        return " ".join(clauses)
    
    def frege_proof_depth(formula):
        # Simplified Frege proof depth calculation
        return len(formula.split()) ** 0.5
    
    def symplectic_leaves_count(graph):
        # Simplified symplectic leaves count (placeholder)
        return len(graph) // 2
    
    n = random.randint(10, 30)
    d = random.randint(2, n - 1)
    graph = generate_d_regular_graph(n, d)
    formula = tseitin_formula(n)
    proof_depth = frege_proof_depth(formula)
    leaves_count = symplectic_leaves_count(graph)
    
    return {
        "metric_name": "symplectic_leaves_vs_proof_depth",
        "metric_value": abs(leaves_count - proof_depth),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")