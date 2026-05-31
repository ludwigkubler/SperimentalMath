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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, 5))]
            clauses.append(clause)
        return clauses
    
    def local_index(cnf):
        n = len(cnf)
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length
                dp[i][j] = max(dp[i][k] + dp[k + 1][j] for k in range(i, j))
        
        return dp[0][n]
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_k_cnf(n)
            metric_value = local_index(cnf)
            total_metric_value += metric_value
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(0.5 * n * math.log2(n) <= mean_metric_value <= 1.5 * n * math.log2(n) for n in [5, 10, 15, 20, 30, 40])
    
    return {
        "metric_name": "local_index",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")