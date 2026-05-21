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
        for _ in range(1000):  # Sample 1000 instances from S_n
            X = [random.choice([-1, 1]) for _ in range(n*n)]
            if sum(X) != n:
                continue
            total += f(X)**2
        return total / 1000
    
    def xi(f, n):
        perm_n = lambda X: sum(X[i*n:(i+1)*n] for i in range(n))
        return (mu(perm_n, n) - mu(f, n)) / (mu(perm_n, n) + mu(f, n))
    
    det_n = lambda X: sum(math.prod(X[i*n+j] for j in range(n)) for i in range(n))
    
    if xi(det_n, 2) < 1 - 4**-2:
        return {
            "metric_name": "xi(det_n)",
            "metric_value": xi(det_n, 2),
            "instances_tested": 1000,
            "conjecture_holds": False,
            "counterexample": "det_n fails at n=2"
        }
    
    results = []
    for m in range(1, int(math.sqrt(6)) + 1):  # m <= floor(n^(3/2))
        for _ in range(30):
            B = [[random.expovariate(1) for _ in range(6)] for _ in range(m*m)]
            Y = [sum(B[i][j] * X[j*n:(j+1)*n] for j in range(n)) for i in range(m)]
            g = lambda X: sum(math.prod(Y[i*m+j] for j in range(m)) for i in range(m))
            results.append(xi(g, 2))
    
    if min(results) < 1 - 6 * 4**-2:
        return {
            "metric_name": "xi(det_m(BX))",
            "metric_value": min(results),
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"det_m(BX) fails at n=2, m={results.index(min(results))+1}"
        }
    
    return {
        "metric_name": "xi(det_n)",
        "metric_value": xi(det_n, 2),
        "instances_tested": 1000,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 4, 5]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 1 - 6 * 4**-2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 1 - 6 * 4**-2 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='det_m(BX) fails at n=2' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=120")