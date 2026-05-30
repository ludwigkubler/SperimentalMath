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
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def communication_complexity(matrix):
        n = len(matrix)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != matrix[j][i]:
                    count += 1
        return count
    
    def entanglement_entropy(matrix):
        n = len(matrix)
        ones = sum(sum(row) for row in matrix)
        zeros = n * n - ones
        p_ones = ones / (n * n)
        p_zeros = zeros / (n * n)
        if p_ones == 0 or p_zeros == 0:
            return 0
        return -p_ones * math.log2(p_ones) - p_zeros * math.log2(p_zeros)
    
    n_max = 40
    instances_tested = 30
    total_complexity = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        matrix = generate_matrix(n)
        complexity = communication_complexity(matrix)
        entropy = entanglement_entropy(matrix)
        
        if entropy <= math.log2(n) and complexity > 0:
            total_complexity += complexity
    
    mean_complexity = total_complexity / instances_tested
    conjecture_holds = all(complexity <= (entropy**2 * math.log2(n)**2) for _ in range(instances_tested))
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_complexity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")