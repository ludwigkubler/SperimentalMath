# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations
from collections import defaultdict

def gaussian_elimination(A, b):
    n = len(b)
    augmented = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        if augmented[i][i] == 0:
            return None  # No unique solution
        
        for j in range(i+1, n):
            factor = Fraction(augmented[j][i], augmented[i][i])
            for k in range(n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(augmented[i][-1], augmented[i][i])
        for j in range(i-1, -1, -1):
            augmented[j][-1] -= augmented[j][i] * x[i]
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random communication protocol
    m = random.randint(5, 30)
    d = random.randint(2, 10)
    messages = [random.choice(range(d)) for _ in range(m)]
    
    # Construct the associated polyhedral complex (simplified example)
    A = [[0] * d for _ in range(m)]
    b = [0] * m
    for i in range(m):
        A[i][messages[i]] = 1
        b[i] = random.randint(1, 5)
    
    # Calculate the minimal tropical motivic rank (simplified example)
    solution = gaussian_elimination(A, b)
    if solution is None:
        return {
            "metric_name": "minimal_tropical_motivic_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    # Calculate the communication complexity rank variance (simplified example)
    rcv = sum((x - sum(solution) / len(solution)) ** 2 for x in solution) / len(solution)
    
    return {
        "metric_name": "minimal_tropical_motivic_rank",
        "metric_value": len([x for x in solution if x != 0]),
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")