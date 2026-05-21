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
    
    def mu(f, n):
        count = 0
        total = 0
        for _ in range(30):  # Sample 30 instances from the slice S_n
            X = [random.choice([-1, 1]) for _ in range(n*n)]
            if sum(X) == n:
                count += 1
                total += f(X)**2
        return total / count if count > 0 else 0
    
    def xi(f):
        det_val = mu(det_n, n)
        perm_val = mu(perm_n, n)
        return (det_val - perm_val) / (det_val + perm_val)
    
    def det_n(X):
        n = int(math.sqrt(len(X)))
        if n * n != len(X):
            raise ValueError("Invalid input size for determinant")
        return det(X, n)
    
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
    
    def perm_n(X):
        n = int(math.sqrt(len(X)))
        if n * n != len(X):
            raise ValueError("Invalid input size for permutation")
        return sum(X)
    
    n_values = [2, 3, 4, 5]
    results = []
    
    for n in n_values:
        det_val = xi(det_n)
        if det_val < 1 - 4**(-n):
            return {
                "metric_name": "Slice-Fourier Variance Asymmetry",
                "metric_value": det_val,
                "instances_tested": 30,
                "conjecture_holds": False,
                "counterexample": f"det_n failed at n={n}"
            }
        results.append(det_val)
    
    for n in n_values:
        for m in range(1, int(n**(3/2)) + 1):
            B = [[random.expovariate(1) for _ in range(n*n)] for _ in range(m*m)]
            Y = [sum(B[i][j] * X[j*n+k] for j in range(n)) for i in range(m) for k in range(n)]
            g_val = xi(lambda X: det_m(X))
            if g_val < 1 - n * 4**(-n):
                return {
                    "metric_name": "Slice-Fourier Variance Asymmetry",
                    "metric_value": g_val,
                    "instances_tested": 30,
                    "conjecture_holds": False,
                    "counterexample": f"g(X) failed at (n,m,B)"
                }
            results.append(g_val)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = 1.0
    
    return {
        "metric_name": "Slice-Fourier Variance Asymmetry",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 1 - n * 4**(-n)) / len(results)
    
    if all(r >= 1 - n * 4**(-n) for r, n in zip(results, [2, 3, 4, 5] * (len(results) // 4))):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 1 - n * 4**(-n) for r, n in zip(results, [2, 3, 4, 5] * (len(results) // 4))):
        first_failing_seed = seeds[results.index(min(r for r, n in zip(results, [2, 3, 4, 5] * (len(results) // 4)) if r < 1 - n * 4**(-n)))]
        print(f"RESULT: FALSIFIED counterexample=\"g(X) failed at (n,m,B)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")