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
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank_matrix = [[f[i ^ j] for i in range(2**n)] for j in range(2**n)]
        rank = 0
        for row in rank_matrix:
            if all(row[j] == 0 for j in range(1, len(row))):
                continue
            pivot_row = next(j for j in range(len(row)) if row[j] != 0)
            pivot = row[pivot_row]
            rank += 1
            for i in range(len(rank_matrix)):
                if i != pivot_row and rank_matrix[i][pivot_row] != 0:
                    factor = rank_matrix[i][pivot_row] / pivot
                    for j in range(n):
                        rank_matrix[i][j] -= factor * row[j]
        return rank
    
    def minimal_topological_degree(f):
        n = int(math.log2(len(f)))
        degree = 0
        for i in range(1, len(f)):
            if f[i] != f[0]:
                degree += 1
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_td = 0
        total_rc = 0
        
        while instances_tested < 100:
            f = generate_boolean_function(n)
            td = minimal_topological_degree(f)
            rc = communication_complexity_rank_variance(f)
            
            if td == 0 or rc == 0:
                continue
            
            total_td += td
            total_rc += rc
            instances_tested += 1
        
        if instances_tested < 100:
            return {
                "metric_name": "minimal_topological_degree",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        
        avg_td = total_td / instances_tested
        avg_rc = total_rc / instances_tested
        
        if avg_td < avg_rc:
            return {
                "metric_name": "minimal_topological_degree",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"td({avg_td}) < rc({avg_rc})"
            }
    
    return {
        "metric_name": "minimal_topological_degree",
        "metric_value": None,
        "instances_tested": 100 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean=None std=None support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean=None std=None support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"td < rc\" first_failing_seed={first_failing_seed}")