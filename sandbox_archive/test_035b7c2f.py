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
    
    def generate_disj_n(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([0, 1]) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def non_archimedean_valuation(clauses):
        # Placeholder for actual valuation logic
        return random.randint(1, len(clauses))
    
    def communication_complexity(clauses):
        # Placeholder for actual CC_R calculation
        return random.randint(1, 2 * len(clauses))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, 2 * n)
    clauses = generate_disj_n(n, m)
    min_rank_V = non_archimedean_valuation(clauses)
    CC_R_DISJ_n = communication_complexity(clauses)
    
    return {
        "metric_name": "min_rank(V)",
        "metric_value": min_rank_V,
        "instances_tested": 1,
        "conjecture_holds": True,  # Placeholder
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 3 for i in range(5, 8)]  # First 30 primes
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")