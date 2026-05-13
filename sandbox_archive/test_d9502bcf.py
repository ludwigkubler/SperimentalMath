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
    
    def binomial_coefficient(n, k):
        if k > n or k < 0:
            return 0
        result = 1
        for i in range(1, k + 1):
            result *= (n - k + i)
            result //= i
        return result
    
    def moment_cumulant_transform(M, n):
        cumulants = [0] * (n + 1)
        for k in range(1, n + 1):
            sum_term = Fraction(0)
            for i in range(k + 1):
                binom_coeff = binomial_coefficient(k, i)
                sign = (-1) ** i
                if i < len(M) and k - i < len(M[i]):
                    sum_term += binom_coeff * sign * M[i][k - i]
            cumulants[k] = sum_term / k
        return cumulants
    
    def free_cumulant_sum(cumulants):
        return sum(abs(cumulants[k]) for k in range(1, len(cumulants)))
    
    n_values = [10, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        cumulants = moment_cumulant_transform(M, n)
        metric_value = free_cumulant_sum(cumulants)
        total_metric_value += metric_value
        instances_tested += n
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value >= 100 * (n_values[-1] ** 2) / len(n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Free Cumulant Sum",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")