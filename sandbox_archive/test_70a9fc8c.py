# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n: int, m: int):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice(variables), random.choice(variables)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def hypergraph_max_matching_size(clauses):
        n = len(clauses)
        graph = [[] for _ in range(n + 1)]
        for i, clause in enumerate(clauses, start=1):
            for var in clause:
                graph[var].append(i)
        
        matching = []
        visited_edges = set()
        for i in range(1, n + 1):
            for j in range(len(graph[i])):
                edge = (i, graph[i][j])
                if edge not in visited_edges and (graph[i][j], i) not in visited_edges:
                    matching.append(edge)
                    visited_edges.add(edge)
        return len(matching)
    
    def is_polynomial_circuit_size(n: int):
        # Placeholder for ACC^0 circuit size check
        return True
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    clauses = generate_3cnf(n, m)
    max_matching_size = hypergraph_max_matching_size(clauses)
    conjecture_holds = is_polynomial_circuit_size(n) and (max_matching_size == int(n ** 0.5))
    
    return {
        "metric_name": "max_matching_size",
        "metric_value": max_matching_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")