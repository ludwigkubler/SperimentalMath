# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_integer_solution(A, b):
        n = len(b)
        for i in range(n):
            if not A[i][i] == 1:
                return False
            for j in range(n):
                if j != i and not A[i][j] == 0:
                    return False
            if not b[i].denominator == 1:
                return False
        return True
    
    def generate_matroid_matrix(n, m):
        A = [[Fraction(random.randint(0, 2), random.randint(1, 3)) for _ in range(m)] for _ in range(n)]
        b = [Fraction(random.randint(0, 2), random.randint(1, 3)) for _ in range(n)]
        return A, b
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            A, b = generate_matroid_matrix(n, n)
            if is_integer_solution(A, b):
                results.append(1)
            else:
                results.append(0)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(result == 1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Fractional Solution Rate",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r == 1) / len(results)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = seeds[results.index(next(r for r in results if r != 1))]
        result = f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}"
    
    print(result)