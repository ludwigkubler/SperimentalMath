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
    
    def mu(f, n):
        total = 0
        count = 0
        for _ in range(1000):  # Sample 1000 instances of X on the slice S_n
            X = [random.choice([-1, 1]) for _ in range(n*n)]
            if sum(X) == n:
                total += f(X)**2
                count += 1
        return total / count if count > 0 else 0
    
    def det(matrix, n):
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det_val += ((-1)**j) * matrix[0][j] * det(submatrix, n-1)
            return det_val
    
    def xi(f, n):
        perm_n = lambda X: sum(X[i*n:(i+1)*n] for i in range(n))
        return (mu(perm_n, n) - mu(f, n)) / (mu(perm_n, n) + mu(f, n))
    
    det_n = lambda X: det([X[i*n:(i+1)*n] for i in range(n)], n)
    
    if xi(det_n, 2) < 1 - 4**-2:
        return {
            "metric_name": "Slice-Fourier Variance Asymmetry",
            "metric_value": xi(det_n, 2),
            "instances_tested": 1000,
            "conjecture_holds": False,
            "counterexample": "n=2 failed"
        }
    
    results = []
    for n in range(3, 6):
        slice_size = (n*(n+1)) // 2
        if slice_size < 1000:
            continue
        for _ in range(30):  # Draw 30 random nonnegative B with entries i.i.d. Exp(1)
            B = [[random.expovariate(1) for _ in range(n*n)] for _ in range(n*n)]
            Y = [sum(B[i][j] * X[j*n:(j+1)*n] for j in range(n)) for i in range(n)]
            det_val = xi(lambda X: det([Y[i*n:(i+1)*n] for i in range(n)], n), n)
            results.append(det_val)
    
    if min(results) < 1 - 4**-5:
        return {
            "metric_name": "Slice-Fourier Variance Asymmetry",
            "metric_value": min(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"n=5 failed with minimum value {min(results)}"
        }
    
    return {
        "metric_name": "Slice-Fourier Variance Asymmetry",
        "metric_value": min(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 4, 5]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 1 - 4**-5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 1 - 4**-5 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n=5 failed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")