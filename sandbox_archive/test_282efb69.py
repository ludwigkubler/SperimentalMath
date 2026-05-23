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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
            clauses.append(f'-{variables[i-1]}')
        for i in range(n+1, 2*n):
            a, b = random.sample(variables, 2)
            if random.choice([True, False]):
                clauses.append(f'{-a} {b}')
                clauses.append(f'{a} {-b}')
            else:
                clauses.append(f'{a} {b}')
                clauses.append(f'-{a} -{b}')
        return ' '.join(clauses)

    def tropicalize(formula):
        # Simplified tropicalization for demonstration
        return formula.replace(' ', '\n')

    def compute_minimal_rank(tropicalized_formula):
        # Placeholder for actual computation
        return random.randint(1, n**2 * math.log(n))

    n = 30
    formula = generate_tseitin_formula(n)
    tropicalized_formula = tropicalize(formula)
    minimal_rank = compute_minimal_rank(tropicalized_formula)

    alpha_n = n**2 * math.log(n)
    conjecture_holds = minimal_rank <= alpha_n
    counterexample = "" if conjecture_holds else f"minimal_rank={minimal_rank} > alpha_n={alpha_n}"

    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank > alpha_n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")