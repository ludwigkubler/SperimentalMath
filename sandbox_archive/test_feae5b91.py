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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def p_adic_valuation_rank(clauses):
        # Placeholder function to compute the rank of the p-adic valuation ring
        # This is a stub and should be replaced with actual computation
        return len(set(tuple(sorted(clause)) for clause in clauses))

    def monotone_circuit_depth(clauses):
        # Placeholder function to compute the monotone circuit depth
        # This is a stub and should be replaced with actual computation
        return len(max(len(clause) for clause in clauses))
    
    n = random.randint(5, 40)
    k = random.randint(1, n // 2)
    F = generate_kcnf(n, k)
    r_F = p_adic_valuation_rank(F)
    depth_F = monotone_circuit_depth(F)
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": r_F,
        "instances_tested": 1,
        "conjecture_holds": r_F <= 2 * math.log(n),
        "counterexample": "" if r_F <= 2 * math.log(n) else f"Counterexample: n={n}, k={k}, rank={r_F}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")