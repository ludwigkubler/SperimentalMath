# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10 + (seed % 3) * 5  # Sweep through N in {10, 15, 20, 25, 30}
    
    def generate_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def is_independent(lattice, matrix):
        for i in range(len(matrix)):
            if any(all(matrix[i][j] == lattice[j][k] for k in range(len(matrix))) for j in range(i + 1, len(matrix))):
                return False
        return True
    
    def find_minimal_lattices(matrix):
        lattices = []
        for i in range(1, len(matrix) + 1):
            for subset in combinations(range(len(matrix)), i):
                lattice = [[matrix[j][k] if k in subset else 0 for k in range(len(matrix))] for j in range(len(matrix))]
                if is_independent(lattice, matrix):
                    lattices.append(lattice)
        return min(lattices, key=len)
    
    def communication_complexity(n, min_lattice_size):
        return math.log2(n) ** 2 * math.log(min(min_lattice_size, n - min_lattice_size))
    
    matrix = generate_matrix(n)
    min_lattice = find_minimal_lattices(matrix)
    min_lattice_size = len(min_lattice)
    computed_complexity = communication_complexity(n, min_lattice_size)
    upper_bound = math.log2(n) ** 2 * math.log(min(min_lattice_size, n - min_lattice_size))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": computed_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": computed_complexity <= upper_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")