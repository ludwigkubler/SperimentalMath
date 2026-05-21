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
    
    def perm_n(X):
        return sum(X[i][j] * X[j][i] for i in range(n) for j in range(n))
    
    def det_n(X):
        if n == 1:
            return X[0][0]
        else:
            det = 0
            sign = 1
            for j in range(n):
                submatrix = [[X[i][k] for k in range(n) if k != j] for i in range(1, n)]
                det += sign * X[0][j] * det_n(submatrix)
                sign *= -1
            return det
    
    def slice_evals(f, n):
        count = 0
        total = 0
        for _ in range(2 ** n):
            X = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
            if sum(sum(row) for row in X) == n:
                count += 1
                total += f(X)
        return total / count
    
    def mu(f):
        return slice_evals(f, n) ** 2
    
    def xi(f):
        perm_val = mu(perm_n)
        det_val = mu(det_n)
        if det_val == 0:
            return float('-inf')
        return (perm_val - det_val) / (perm_val + det_val)
    
    results = []
    for n in [2, 3, 4, 5]:
        perm_val = xi(perm_n)
        det_val = xi(det_n)
        if det_val < 1 - 4 ** (-n):
            return {
                "metric_name": "xi(det_n)",
                "metric_value": det_val,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"det_n failed at n={n}"
            }
        results.append(det_val)
    
    for n in range(2, 6):
        m_max = int(n ** (3 / 2))
        for m in range(1, m_max + 1):
            B = [[random.expovariate(1) for _ in range(n)] for _ in range(m)]
            Y = [[sum(B[i][k] * X[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
            det_val = slice_evals(lambda X: det_m(X), m)
            if det_val < 1 - n * 4 ** (-n):
                return {
                    "metric_name": f"xi(det_{m}(BX))",
                    "metric_value": det_val,
                    "instances_tested": 30,
                    "conjecture_holds": False,
                    "counterexample": f"det_{m}(BX) failed at (n,m)=({n},{m})"
                }
            results.append(det_val)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([x for x in results if x >= 1 - n * 4 ** (-n)]) / len(results)
    
    return {
        "metric_name": "xi(det_n)",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(x["metric_value"] for x in results) / len(results)
    std = math.sqrt(sum((x["metric_value"] - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")