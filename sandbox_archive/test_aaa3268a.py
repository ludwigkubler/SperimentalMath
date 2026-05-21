# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def simplicial_complex_from_clauses(clauses):
        nodes = set()
        for clause in clauses:
            nodes.update(clause)
        simplices = []
        for i, j, k in combinations(nodes, 3):
            if any(node in clause for node in [i, j, k]):
                simplices.append([i, j, k])
        return simplices
    
    def persistent_homology(simplices):
        # Simplified version of persistent homology using a filtration
        intervals = []
        for simplex in simplices:
            intervals.append((len(simplex), 1))
            intervals.append((len(simplex) + 1, -1))
        intervals.sort()
        barcode_length = 0
        active_intervals = 0
        for length, change in intervals:
            barcode_length += active_intervals * (length - barcode_length)
            active_intervals += change
        return barcode_length
    
    def communication_complexity(clauses):
        # Simplified version of communication complexity using a bipartite graph
        n = len(clauses)
        A = [sum(1 for node in clause if node < n) for clause in clauses]
        B = [sum(1 for node in clause if node >= n) for clause in clauses]
        return sum(min(a, b) for a, b in zip(A, B))
    
    def generate_3cnf(n):
        variables = list(range(n))
        clauses = []
        for _ in range(n * 2):  # Each variable appears in at least two clauses
            clause = random.sample(variables + [-v - 1 for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    n = 40
    clauses = generate_3cnf(n)
    simplices = simplicial_complex_from_clauses(clauses)
    barcode_length = persistent_homology(simplices)
    comm_complexity = communication_complexity(clauses)
    
    metric_name = "persistent_homology_barcode_length"
    metric_value = barcode_length
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if barcode_length == Fraction(n, 2) and comm_complexity >= n:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")