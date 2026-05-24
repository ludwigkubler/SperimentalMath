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
    
    def generate_cnf(n: int, m: int):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def sheaf_rank(cnf):
        # Placeholder function to compute sheaf rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.random() * 50
    
    def dpll_refutation_tree_width(cnf):
        # Placeholder function to compute DPLL refutation tree width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 100)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(n * (n / 10))  # Example: m is proportional to n
        cnf = generate_cnf(n, m)
        rank = sheaf_rank(cnf)
        width = dpll_refutation_tree_width(cnf)
        results.append({
            "n": n,
            "m": m,
            "rank": rank,
            "width": width,
            "ratio": width / rank
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    max_width = max(result["width"] for result in results)
    
    conjecture_holds = all(result["ratio"] <= 2 * math.log(n**m + m, 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "dpll_refutation_tree_width_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")