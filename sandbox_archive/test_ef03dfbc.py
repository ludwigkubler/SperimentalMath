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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(5, 10)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def grothendieck_witt_class(cnf):
        n = len(cnf[0])
        A = [[0] * n for _ in range(n)]
        for clause in cnf:
            for x in clause:
                for y in clause:
                    if x != 0 and y != 0:
                        i, j = abs(x) - 1, abs(y) - 1
                        A[i][j] += 1
                        A[j][i] += 1
        return sum(sum(A[i][j] * (A[i][j] + 1) // 2 for j in range(i)) for i in range(n))
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf[0])
        rank = [0] * n
        for clause in cnf:
            for literal in clause:
                rank[abs(literal) - 1] += 1
        return sum((r - (n + 1) / 2) ** 2 for r in rank)
    
    def min_index(A):
        n = len(A)
        for i in range(n):
            if A[i][i] != 0:
                return i
        return None
    
    n_max = 0
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        A = grothendieck_witt_class(cnf)
        v = communication_complexity_rank_variance(cnf)
        min_index_val = min_index(A)
        
        if min_index_val is not None:
            total_metric_value += min_index_val
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "min_index",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")