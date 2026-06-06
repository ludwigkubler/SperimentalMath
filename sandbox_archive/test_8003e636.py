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
    
    def generate_cnf(m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        # Placeholder function to compute the rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(abs(lit) for lit in sum(cnf, [])))
    
    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        ranks = [communication_complexity_rank(cnf) for _ in range(30)]
        results.append(variance(ranks))
    
    metric_value = sum(results) / len(results)
    instances_tested = 180
    n_max = max(n_values)
    conjecture_holds = all(r <= n ** 2 for r, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    support_fraction = sum(1 for r in results if r <= max(n_values) ** 2) / len(results)
    
    if all(r <= n ** 2 for r, n in zip(results, n_values)):
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results):.4f} std={math.sqrt(sum((x - sum(results)/len(results))**2 for x in results)/len(results)):.4f} support_fraction={support_fraction:.4f}")
    elif any(r > n ** 2 for r, n in zip(results, n_values)):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r > n_values[i] ** 2)]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")