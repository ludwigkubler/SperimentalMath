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
    
    def matrix_representation(func, n):
        M = [[func(i ^ j) for j in range(2**n)] for i in range(2**n)]
        return M
    
    def isomorphism_count(M):
        n = len(M)
        count = 0
        for perm in itertools.permutations(range(n)):
            if all(M[i][j] == M[perm[i]][perm[j]] for i in range(n) for j in range(n)):
                count += 1
        return count
    
    def communication_rank(M):
        n = len(M)
        rank = 0
        for col in range(n):
            row_sums = [sum(M[row][col] for row in range(n)) for _ in range(2)]
            if any(row_sum == 0 or row_sum == n for row_sum in row_sums):
                rank += 1
        return rank
    
    def correlation_coefficient(ind, r):
        mean_ind = sum(ind) / len(ind)
        mean_r = sum(r) / len(r)
        numerator = sum((ind[i] - mean_ind) * (r[i] - mean_r) for i in range(len(ind)))
        denominator = math.sqrt(sum((ind[i] - mean_ind)**2 for i in range(len(ind))) * sum((r[i] - mean_r)**2 for i in range(len(r))))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_indeterminacy = []
    total_rank = []
    
    for n in n_values:
        instances_tested = 0
        ind_sum = 0
        r_sum = 0
        
        while instances_tested < 30:
            func = generate_boolean_function(n)
            M = matrix_representation(func, n)
            ind = isomorphism_count(M)
            r = communication_rank(M)
            
            if ind == 0 or r == 0:
                continue
            
            total_indeterminacy.append(ind)
            total_rank.append(r)
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "Correlation Coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": "Insufficient instances tested"
            }
    
    correlation_coefficient = (len(total_indeterminacy) * sum(ind * r for ind, r in zip(total_indeterminacy, total_rank)) -
                               sum(total_indeterminacy) * sum(total_rank)) / \
                              math.sqrt((len(total_indeterminacy) * sum(ind**2 for ind in total_indeterminacy) - sum(total_indeterminacy)**2) *
                                        (len(total_rank) * sum(r**2 for r in total_rank) - sum(total_rank)**2))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(total_indeterminacy),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Insufficient instances tested\" first_failing_seed={r['seed']}")
                break