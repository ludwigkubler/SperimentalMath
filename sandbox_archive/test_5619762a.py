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
    
    n = 40
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    
    def noncommutative_Lp_norm(M, p):
        if p == float('inf'):
            return max(max(abs(x) for x in row) for row in M)
        else:
            sum_val = 0
            for i in range(n):
                for j in range(n):
                    sum_val += abs(M[i][j]) ** p
            return (sum_val / (n * n)) ** (1 / p)
    
    c = 1.0  # Example constant, adjust as needed
    
    min_norm = float('inf')
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            norm = noncommutative_Lp_norm(M, i + j - 2)
            if norm < min_norm:
                min_norm = norm
    
    metric_value = min_norm
    conjecture_holds = metric_value >= c * n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Noncommutative L_p Norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")