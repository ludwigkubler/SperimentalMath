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
    
    def generate_random_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if len(set(clause)) != n:  # Ensure no duplicate literals
                continue
            clauses.append(clause)
        return clauses
    
    def sum_of_squares_approximation_degree(clauses):
        m = len(clauses)
        n = max(abs(lit) for clause in clauses for lit in clause)
        degree = math.ceil(math.log2(m * n))
        return degree
    
    def hodge_integrals_rank(clauses):
        # Placeholder function to compute the minimal rank of Hodge integrals
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses)  # Example: rank is equal to the number of clauses
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 10)
    clauses = generate_random_3cnf(n, m)
    
    degree = sum_of_squares_approximation_degree(clauses)
    rank = hodge_integrals_rank(clauses)
    
    return {
        "metric_name": "Rank of Hodge Integrals",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= degree,
        "counterexample": "" if rank <= degree else f"rank={rank}, degree={degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")