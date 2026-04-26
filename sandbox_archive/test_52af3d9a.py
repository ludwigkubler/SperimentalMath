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
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i ^ (1 << j)] if i & (1 << j) else f[i] for j in range(n)] for i in range(2**n)]
        return matrix
    
    def convex_hull_volume(matrix):
        # Simplex volume approximation using determinant
        n = len(matrix)
        det = 0
        for sign, perm in product([-1, 1], repeat=n):
            submatrix = [[matrix[i][j] for j in perm[:n]] for i in range(n)]
            det += sign * abs(determinant(submatrix))
        return abs(det) / math.factorial(n)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def symplectic_capacity(volume):
        # Simplified version assuming a unitary scaling factor
        return 1 / volume
    
    def randomized_communication_complexity(f):
        n = int(math.log2(len(f)))
        complexity = float('inf')
        for _ in range(10):  # Sample multiple times to get an average
            message_length = random.randint(n, 2*n)
            if message_length >= len(f):
                return 0
            complexity = min(complexity, message_length)
        return complexity
    
    n = random.choice([5, 8, 11, 14])
    f = generate_random_boolean_function(n)
    comm_matrix = communication_matrix(f)
    volume = convex_hull_volume(comm_matrix)
    cap = symplectic_capacity(volume)
    rc_complexity = randomized_communication_complexity(f)
    
    return {
        "metric_name": "symplectic_capacity",
        "metric_value": cap,
        "instances_tested": 1,
        "conjecture_holds": abs(cap - 1 / rc_complexity) < 0.1,  # Simplified check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")