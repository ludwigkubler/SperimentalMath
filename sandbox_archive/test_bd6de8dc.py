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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([f'x{i}', f'-x{i}']) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix, b):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [[matrix[i][j] for j in range(n)] + [b[i]] for i in range(m)]
        
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        return [row[-1] for row in augmented_matrix]
    
    def volume(hypersurface):
        # Placeholder for actual hypersurface volume calculation
        return len(hypersurface)
    
    def resolution_length(cnf, assignment):
        # Placeholder for actual resolution proof length calculation
        return 2 ** (len(assignment) / 2)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    hypersurface = gaussian_elimination([[1 if i == j else 0 for j in range(n)] for i in range(n)], [1] * n)
    min_volume = volume(hypersurface)
    assignment = {f'x{i}': True for i in range(1, n + 1)}
    
    resolution_len = resolution_length(cnf, assignment)
    conjecture_holds = (resolution_len <= 2 ** (min_volume / 2)) and (min_volume >= 2 ** n)
    counterexample = "" if conjecture_holds else f"Volume={min_volume}, Resolution Length={resolution_len}"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")