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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_satisfying_assignments(f, n):
        count = 0
        for i in range(2**n):
            if sum(x * y for x, y in zip(bin(i)[2:].zfill(n), f)) == len([x for x in f if x == 1]):
                count += 1
        return count
    
    def shannon_entropy(probs):
        entropy = 0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    g_n = []
    E_f = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        g_n.append(count_satisfying_assignments(f, n))
        
        # Calculate probabilities of satisfying assignments
        total = sum(g_n[-1])
        probs = [Fraction(x, total) for x in g_n[-1]]
        E_f.append(shannon_entropy(probs))
    
    if not g_n or not E_f:
        return {
            "metric_name": "E(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Perform linear regression
    n_values = list(range(5, 41))
    A = [[n, 1] for n in n_values]
    b = E_f
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        AugmentedMatrix = [A[i] + [b[i]] for i in range(m)]
        
        # Forward elimination
        for k in range(n - 1):
            if AugmentedMatrix[k][k] == 0:
                return None  # No unique solution
            for i in range(k + 1, m):
                factor = AugmentedMatrix[i][k] / AugmentedMatrix[k][k]
                for j in range(k, n + 1):
                    AugmentedMatrix[i][j] -= factor * AugmentedMatrix[k][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (AugmentedMatrix[i][-1] - sum(AugmentedMatrix[i][j] * x[j] for j in range(i + 1, n))) / AugmentedMatrix[i][i]
        
        return x
    
    result = gaussian_elimination(A, b)
    
    if result is None:
        return {
            "metric_name": "E(f)",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    slope, intercept = result
    correlation_coefficient = (len(n_values) * sum(x*y for x, y in zip(n_values, E_f)) - sum(n_values)*sum(E_f)) / \
                              math.sqrt((len(n_values) * sum(x**2 for x in n_values) - sum(n_values)**2) * 
                                          (len(n_values) * sum(y**2 for y in E_f) - sum(E_f)**2))
    
    return {
        "metric_name": "E(f)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(v <= 4 for v in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")