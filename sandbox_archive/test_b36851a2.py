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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(['x' + str(i), 'y' + str(i)], 2) + ['z' + str(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def tseitin_graph(clauses):
        # Construct Tseitin graph here
        pass

    def adjacency_matrix(graph):
        # Compute adjacency matrix here
        pass

    def smallest_eigenvalue(matrix):
        # Compute smallest eigenvalue here
        pass

    n_values = [20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(10):  # Test each size with 10 instances
            phi = generate_3cnf(n)
            G_phi = tseitin_graph(phi)
            A_phi = adjacency_matrix(G_phi)
            lambda_min = smallest_eigenvalue(A_phi)
            results.append(abs(lambda_min - 0.5) / (n / 10))
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(x <= 0.5 for x in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "spectral_gap",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r <= 0.5) / len(results)
    
    if all(r <= 0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 0.5 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")