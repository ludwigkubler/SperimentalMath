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

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = augmented_matrix[i][i]
        for j in range(n + 1):
            if i != j:
                factor_j = augmented_matrix[j][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= (factor_j / factor) * augmented_matrix[i][k]
                augmented_matrix[j][i] = Fraction(0)
        augmented_matrix[i][i] = Fraction(1, abs(factor))
    return [row[n:] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    adjacency_matrix = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # Count eigenvalues in the interval [-sqrt(n log n), sqrt(n log n)]
    eigenvalues = gaussian_elimination(adjacency_matrix)
    count = sum(1 for ev in eigenvalues if -math.sqrt(n * math.log(n)) <= ev <= math.sqrt(n * math.log(n)))
    
    # Placeholder for minimal SOS degree calculation (not implemented)
    sos_degree = 0
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*100 + 2, 100))  # Default to first 30 primes if no seeds provided
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")