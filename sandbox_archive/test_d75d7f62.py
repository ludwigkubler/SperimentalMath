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
    
    def generate_quantum_circuit(n):
        # Simple random unitary matrix for demonstration purposes
        U = [[random.random() + 1j * random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    U[i][j] = abs(U[i][j])
                else:
                    U[i][j] /= math.sqrt(2)
        return U
    
    def trace(matrix):
        n = len(matrix)
        det = 0
        indices = list(range(n))
        for p in itertools.permutations(indices):
            prod = 1
            for i in range(n):
                sign = -1 if (p[i] % 2) else 1
                prod *= matrix[p[i]][i]
            det += sign * prod
        return det
    
    def frobenius_schur_indicator(U, n):
        return abs(trace(U.conjugate().transpose()) / math.factorial(n))
    
    def entropy(D):
        D = [x for x in D if x > 0]  # Filter out zero probabilities
        return -sum(p * math.log2(p) for p in D)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    n_max = 0
    
    for n in n_values:
        U = generate_quantum_circuit(n)
        instances_tested = 1
        metric_value = frobenius_schur_indicator(U, n)
        entropy_D = entropy([random.random() for _ in range(2**n)])
        
        results.append({
            "metric_name": "Frobenius-Schur Indicator",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": metric_value <= entropy_D,
            "counterexample": ""
        })
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["mean_metric"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["support_fraction"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")