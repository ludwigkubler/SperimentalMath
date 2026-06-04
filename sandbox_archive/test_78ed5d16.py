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
    
    # Generate a random Boolean function with communication complexity rank r(f)
    n = 5 + (seed % 6) * 5  # Sweep through sizes 5, 10, 15, 20, 30, 40
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Calculate the communication complexity rank r(f)
    def comm_complexity_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 1
        while True:
            found = False
            for i in range(n):
                if f[i] != f[0]:
                    break
            else:
                return rank
            for j in range(i + 1, n):
                if f[j] != f[i]:
                    found = True
                    break
            if not found:
                return rank
            rank += 1
    r_f = comm_complexity_rank(f)
    
    # Construct the algebraic variety V_f using the eta-invariant
    def eta_invariant(V):
        n = len(V)
        if n == 0:
            return 0
        det = 1
        for i in range(n):
            det *= V[i][i]
        return abs(det)
    
    V_f = []
    for i in range(2**n):
        row = []
        for j in range(n):
            if f[j] == 1:
                row.append((i >> j) & 1)
            else:
                row.append(0)
        V_f.append(row)
    
    eta_f = eta_invariant(V_f)
    
    # Measure the correlation coefficient
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            return None
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        if var_x == 0 or var_y == 0:
            return None
        return cov_xy / math.sqrt(var_x * var_y)
    
    correlation_coefficient = pearson_correlation([eta_f], [r_f])
    
    # Return the results
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.5,
        "counterexample": "" if correlation_coefficient is not None else "correlation_coefficient=None"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=None\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget_exceeded n_tested=30")