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
    
    def communication_complexity(f):
        n = len(f)
        kappa_f = 0
        for x in range(1 << (n-1)):
            y = f[x] ^ f[x + (1 << (n-1))]
            if y != f[x]:
                kappa_f += 1
        return kappa_f
    
    def symplectic_area(density_matrix):
        n = len(density_matrix)
        det = 1.0
        for i in range(n):
            det *= density_matrix[i][i]
        return -2 * math.log(det) if det > 0 else float('inf')
    
    def random_density_matrix(n):
        matrix = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                matrix[i][j] += matrix[j][i]
                if i == j:
                    matrix[i][j] /= 2
                else:
                    matrix[i][j] *= math.sqrt(2)
        return matrix
    
    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(1 << n)]
    
    instances_tested = 0
    total_area = 0.0
    total_kappa_f = 0.0
    
    for n in [5, 10, 15, 20, 30, 40]:
        kappa_f = communication_complexity(random_boolean_function(n))
        density_matrix = random_density_matrix(n)
        area = symplectic_area(density_matrix)
        
        if area == float('inf'):
            continue
        
        total_area += area
        total_kappa_f += kappa_f
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "symplectic_area",
            "metric_value": -1,
            "instances_tested": instances_tested,
            "n_max": max([5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_area = total_area / instances_tested
    mean_kappa_f = total_kappa_f / instances_tested
    
    return {
        "metric_name": "symplectic_area",
        "metric_value": mean_area,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(supported_count, len(results))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")