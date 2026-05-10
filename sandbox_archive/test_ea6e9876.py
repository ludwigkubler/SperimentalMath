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
    n = 40
    p_values = [2, 3, int(math.log2(n)) + 1]
    
    # Generate a random DISJOINTNESS matrix
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = 0
    
    # Compute the Schatten p-norm ||M||_p
    def schatten_p_norm(M, p):
        if p == 2:
            return sum(sum(row[j]**2 for j in range(n))**0.5 for row in M)**0.5
        else:
            eigenvalues = []
            # Compute the matrix power and trace manually (simplified version)
            for _ in range(p):
                M = [[sum(M[i][k] * M[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
            trace = sum(M[i][i] for i in range(n))
            return trace**(1/p)
    
    ratios = [schatten_p_norm(M, p) / n**(0.5 - 1/p) for p in p_values]
    
    # Check if all ratios exceed the threshold
    conjecture_holds = all(ratio > 0.75 for ratio in ratios)
    counterexample = "" if conjecture_holds else "threshold_not_exceeded"
    
    return {
        "metric_name": "Schatten p-norm ratio",
        "metric_value": sum(ratios) / len(ratios),
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"threshold_not_exceeded\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")