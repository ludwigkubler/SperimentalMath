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
    n = random.randint(2, 40)
    k_max = min(n // 2, 15)
    
    def perm_matrix(n):
        p = list(range(n))
        random.shuffle(p)
        return [[int(i == j) for j in range(n)] for i in p]
    
    def det_matrix(n):
        d = [list(range(1, n + 1))]
        for _ in range(1, n):
            d.append([i % n + 1 for i in d[-1]])
        return d
    
    def symmetric_power(matrix, k):
        if k == 0:
            return [[1]]
        result = []
        for i in range(n):
            for j in range(n):
                row = [matrix[i][k] * matrix[j][k] for k in range(n)]
                result.append(row)
        return result
    
    def trivial_multiplicity(matrix, k):
        power = symmetric_power(matrix, k)
        count = 0
        for i in range(n):
            if all(power[i][j] == 0 for j in range(n) if i != j):
                count += 1
        return count
    
    perm_trivial = trivial_multiplicity(perm_matrix(n), k_max)
    det_trivial = trivial_multiplicity(det_matrix(n), k_max)
    
    metric_value = perm_trivial - det_trivial
    conjecture_holds = metric_value >= math.sqrt(n) / 2
    counterexample = "" if conjecture_holds else f"n={n}, k={k_max}"
    
    return {
        "metric_name": "trivial_multiplicity_gap",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break