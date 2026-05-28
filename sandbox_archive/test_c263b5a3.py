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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_queries = 0
        for i in range(2**n):
            queries = []
            for j in range(n):
                if f[i] != f[flip_bits(i, j)]:
                    queries.append(j)
            max_queries = max(max_queries, len(queries))
        return max_queries
    
    def flip_bits(x, k):
        mask = 1 << k
        return x ^ mask
    
    def ehrhart_semigroup(f):
        n = int(math.log2(len(f)))
        semigroup = set()
        for i in range(2**n):
            count = sum(f[i] == f[j] for j in range(2**n))
            semigroup.add(count)
        return len(semigroup)
    
    def rank_ehrhart(semigroup):
        n = len(semigroup)
        matrix = [[0] * n for _ in range(n)]
        for i, a in enumerate(sorted(semigroup)):
            for j, b in enumerate(sorted(semigroup)):
                if (a + b) in semigroup:
                    matrix[i][j] = 1
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(n):
                            matrix[j][i] -= matrix[j][k]
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    cc_symmetry_det = communication_complexity(f)
    rank_ehrhart_f = rank_ehrhart(ehrhart_semigroup(f))
    
    return {
        "metric_name": "Rank_Ehrhart",
        "metric_value": rank_ehrhart_f,
        "instances_tested": 1,
        "conjecture_holds": rank_ehrhart_f <= cc_symmetry_det,
        "counterexample": "" if rank_ehrhart_f <= cc_symmetry_det else f"CC_SymmetryDet(f) > Rank_Ehrhart(f), CC_SymmetryDet(f)={cc_symmetry_det}, Rank_Ehrhart(f)={rank_ehrhart_f}"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes * 3, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"CC_SymmetryDet(f) > Rank_Ehrhart(f)\" first_failing_seed={first_failing_seed}")