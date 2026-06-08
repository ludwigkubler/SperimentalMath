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
    
    def tseitin_formula(boolean_func, n):
        # Simplified Tseitin formula generation
        clauses = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if boolean_func[i] & (1 << j):
                    clause.append(j)
                else:
                    clause.append(-j - 1)
            clauses.append(clause)
        return clauses
    
    def diophantine_exponent(clauses):
        # Simplified calculation of minimal diophantine exponent
        return len(clauses) / n
    
    def communication_complexity_rank_variance(clauses):
        # Simplified calculation of communication complexity rank variance
        rank = len(clauses)
        return (rank - 1) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_func = generate_boolean_function(n)
        clauses = tseitin_formula(boolean_func, n)
        diophantine_exp = diophantine_exponent(clauses)
        rank_variance = communication_complexity_rank_variance(clauses)
        
        results.append({
            "n": n,
            "diophantine_exponent": diophantine_exp,
            "rank_variance": rank_variance
        })
    
    if not results:
        return {
            "metric_name": "diophantine_exponent",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    diophantine_values = [r["diophantine_exponent"] for r in results]
    rank_variance_values = [r["rank_variance"] for r in results]
    
    mean_diophantine = sum(diophantine_values) / len(diophantine_values)
    mean_rank_variance = sum(rank_variance_values) / len(rank_variance_values)
    
    correlation_coefficient = (sum((d - mean_diophantine) * (v - mean_rank_variance) for d, v in zip(diophantine_values, rank_variance_values)) /
                               math.sqrt(sum((d - mean_diophantine)**2 for d in diophantine_values) *
                                         sum((v - mean_rank_variance)**2 for v in rank_variance_values)))
    
    return {
        "metric_name": "diophantine_exponent",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed={first_failing_seed}"
    
    print(result)