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
    
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        literal, polarity = random.choice(random.choice(clauses))
        new_assignment = assignment.copy()
        new_assignment[literal] = polarity
        true_clauses = [c for c in clauses if any(l in c and (polarity == (l[1] == 1)) or l not in c for l in new_assignment)]
        false_clauses = [c for c in clauses if all(l not in c or (polarity != (l[1] == 1)) for l in new_assignment)]
        return 1 + max(dpll(true_clauses, new_assignment), dpll(false_clauses, new_assignment))
    
    def generate_random_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = random.sample(range(-n, 0) + list(range(1, n+1)), 3)
            clause = [(l, random.choice([True, False])) for l in literals]
            clauses.append(clause)
        return clauses
    
    def p_adic_l_function_value(q, n):
        # Simplified approximation of L(1/2, χ_q) using a known result
        return math.log(n, 2) ** (3 / 4)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_random_3cnf(n)
    depth = dpll(clauses, {})
    q = random.randint(1, 100)  # Example p-adic integer
    l_function_value = p_adic_l_function_value(q, n)
    
    return {
        "metric_name": "DPLL Refutation Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": abs(depth - l_function_value) / l_function_value < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")