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
    
    def generate_clause_set(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def lp_norm(p, clauses):
        n = len(clauses[0])
        total = 0
        for clause in clauses:
            polarity = sum(clause)
            total += abs(polarity) ** p
        return (1 / len(clauses)) ** (1 / p) * total
    
    def dpll_disjointness(n, m):
        # Simplified DPLL algorithm to check disjointness
        clauses = generate_clause_set(n, m)
        for i in range(2**n):
            assignment = [((i >> j) & 1) * 2 - 1 for j in range(n)]
            if all(any(lit * assign != 0 for lit in clause) for clause in clauses):
                return True
        return False
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n + 1) // 2)
        clauses = generate_clause_set(n, m)
        lp_norm_value = lp_norm(2, clauses)
        cc_disjointness = dpll_disjointness(n, m)
        
        results.append({
            "metric_name": "communication_complexity",
            "metric_value": cc_disjointness,
            "instances_tested": 1,
            "conjecture_holds": lp_norm_value <= 1 if cc_disjointness else False,
            "counterexample": f"n={n}, m={m}, lp_norm={lp_norm_value}, cc_disjointness={cc_disjointness}"
        })
    
    return {
        "seed": seed,
        **results[0],
        "mean_metric_value": sum(result["metric_value"] for result in results) / len(results),
        "support_fraction": sum(1 for result in results if result["conjecture_holds"]) / len(results)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["mean_metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")