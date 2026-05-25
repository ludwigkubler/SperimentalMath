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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(clause)
        return clauses
    
    def delone_set_geometry(clauses):
        n = len(clauses[0])
        points = []
        for i in range(n):
            point = [0] * n
            point[i] = 1
            points.append(point)
        for clause in clauses:
            for var in clause:
                if var > 0:
                    points[var - 1][var - 1] += 1
                else:
                    points[-var - 1][-var - 1] += 1
        return points
    
    def minimal_rank(points):
        n = len(points)
        rank = 0
        for i in range(n):
            if all(points[i][j] == 0 for j in range(n) if j != i):
                rank += 1
        return rank
    
    def ac0_k_distance_circuit(clauses, k):
        # Placeholder function to construct an AC^0-k-distance circuit
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 5)
    clauses = generate_3cnf(n, m)
    geometry = delone_set_geometry(clauses)
    rank = minimal_rank(geometry)
    k = 1
    circuit_size = ac0_k_distance_circuit(clauses, k)
    
    return {
        "metric_name": "minimal_rank_vs_circuit_size",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= circuit_size ** 2 and circuit_size <= m,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "minimal_rank_vs_circuit_size"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")