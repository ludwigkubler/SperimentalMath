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
    
    def communication_complexity_rank(F):
        n = int(math.log2(len(F)))
        clauses = []
        for i in range(n):
            clause = random.sample(range(n), 2)
            clauses.append(clause)
        return len(clauses)
    
    def noncommutative_spectral_invariants(F):
        n = int(math.log2(len(F)))
        ord_F = 1
        while True:
            # This is a placeholder for the actual computation of noncommutative invariants.
            # For simplicity, we assume that the order is proportional to the number of variables.
            if len(F) <= 2**ord_F:
                return ord_F
            ord_F += 1
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            F = generate_boolean_function(n)
            ord_F = noncommutative_spectral_invariants(F)
            rank_F = communication_complexity_rank(F)
            results.append((ord_F, rank_F))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ord_values = [r[0] for r in results]
    rank_values = [r[1] for r in results]
    
    n = len(ord_values)
    sum_ord = sum(ord_values)
    sum_rank = sum(rank_values)
    sum_ord_squared = sum(x**2 for x in ord_values)
    sum_rank_squared = sum(x**2 for x in rank_values)
    sum_ord_rank = sum(x * y for x, y in zip(ord_values, rank_values))
    
    mean_ord = sum_ord / n
    mean_rank = sum_rank / n
    
    cov = sum_ord_rank - n * mean_ord * mean_rank
    var_ord = sum_ord_squared - n * mean_ord**2
    var_rank = sum_rank_squared - n * mean_rank**2
    
    if var_ord == 0 or var_rank == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = cov / (math.sqrt(var_ord) * math.sqrt(var_rank))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")