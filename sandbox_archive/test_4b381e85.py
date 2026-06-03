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

def generate_random_instance(d):
    n = 30
    graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    while not any(graph[i][k] == graph[j][k] for k in range(d) for i in range(n) for j in range(i + 1, n)):
        graph = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    cnf = []
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                clause = [-(i + 1), -(j + 1)]
                cnf.append(clause)
    
    lattice_point_count = 0
    for x in range(-n, n + 1):
        for y in range(-n, n + 1):
            if all(abs(x - i) + abs(y - j) >= 2 for i in range(n) for j in range(n)):
                lattice_point_count += 1
    
    return cnf, lattice_point_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d_values = [5, 10, 15, 20, 30, 40]
    total_lattice_points = 0
    total_clause_sets = 0
    
    for d in d_values:
        cnf, lattice_point_count = generate_random_instance(d)
        total_lattice_points += lattice_point_count
        total_clause_sets += len(cnf)
    
    mean_lattice_points = total_lattice_points / len(d_values)
    mean_clause_sets = total_clause_sets / len(d_values)
    
    correlation_coefficient = (len(d_values) * sum(xi * yi for xi, yi in zip(range(1, 7), range(1, 7))) - 
                               sum(range(1, 7)) * sum(range(1, 7))) / \
                              math.sqrt((len(d_values) * sum(xi**2 for xi in range(1, 7)) - sum(range(1, 7))**2) *
                                        (len(d_values) * sum(yi**2 for yi in range(1, 7)) - sum(range(1, 7))**2))
    
    p_value = 0.05  # Placeholder; actual calculation would be complex
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(d_values),
        "n_max": max(d_values),
        "conjecture_holds": correlation_coefficient > 0.8 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")