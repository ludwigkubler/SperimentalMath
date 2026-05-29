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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def minterms(f):
        n = len(f)
        mints = []
        for i in range(2**n):
            if f[i] == 1:
                mint = [int(x) for x in format(i, f'0{n}b')]
                mints.append(mint)
        return mints
    
    def monomial_ideals(mints):
        ideals = set()
        for mint in mints:
            ideal = tuple(sorted(set(mint)))
            ideals.add(ideal)
        return ideals
    
    def coxeter_group_rank(n):
        if n == 1: return 1
        elif n == 2: return 2
        elif n == 3: return 3
        elif n == 4: return 6
        elif n == 5: return 8
        elif n == 6: return 10
        elif n == 7: return 12
        elif n == 8: return 14
        elif n == 9: return 16
        elif n == 10: return 18
        else: return None
    
    def dynkin_diagram_vertices(n):
        rank = coxeter_group_rank(n)
        if rank is None:
            return None
        return rank
    
    def spearman_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("Both lists must have the same length")
        
        sorted_x = sorted(zip(x, range(n)))
        sorted_y = sorted(zip(y, range(n)))
        
        x_rank = [sorted_y[i][1] for i in sorted_x]
        y_rank = [sorted_x[i][1] for i in sorted_y]
        
        n = len(x)
        sum_dif_sq = sum((x_rank[i] - y_rank[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_dif_sq) / (n * (n**2 - 1))

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        mints = minterms(f)
        ideals = monomial_ideals(mints)
        num_ideals = len(ideals)
        vertices = dynkin_diagram_vertices(n)
        
        if vertices is None:
            return {
                "metric_name": "Spearman Correlation",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((num_ideals, vertices))
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = spearman_correlation(x, y)
    
    return {
        "metric_name": "Spearman Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")