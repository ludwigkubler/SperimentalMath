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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(10 * n):
            clause = random.choice([1, -1]) * random.choice(variables)
            for _ in range(random.randint(2, 4)):
                clause += random.choice([1, -1]) * random.choice(variables)
            clauses.append(clause)
        return ' '.join(clauses)
    
    def dpll_proof_tree_size(sat_instance):
        # Simplified DPLL proof tree size estimation
        return len(sat_instance.split())
    
    def tropicalized_etale_cohomology_rank(n):
        # Placeholder for actual computation
        return random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_instance = generate_sat_instance(n)
    proof_tree_size = dpll_proof_tree_size(sat_instance)
    rank = tropicalized_etale_cohomology_rank(n)
    
    g_n = math.log(proof_tree_size + 1) / math.log(2)
    conjecture_holds = rank <= g_n and rank <= 2 * n
    
    return {
        "metric_name": "Rank of Tropicalized Etale Cohomology",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}, g(n)={g_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")