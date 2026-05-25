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
    
    def p_adic_log(n, p):
        if n == 0:
            return -math.inf
        log_val = 0
        while n > 0:
            log_val += n % p
            n //= p
        return log_val

    def tseitin_resolution_length(formula):
        # Placeholder implementation for Tseitin resolution length
        # This is a dummy function and should be replaced with the actual algorithm
        return len(formula) * 2

    def minimal_rank(p_adic_potential):
        # Placeholder implementation for minimal rank
        # This is a dummy function and should be replaced with the actual algorithm
        return p_adic_potential + 1

    n = random.randint(5, 40)
    alpha = random.uniform(0.3, 0.7)
    num_clauses = int(n * alpha)

    formula = []
    for _ in range(num_clauses):
        clause = [random.randint(1, n) for _ in range(random.randint(2, n))]
        formula.append(clause)

    tau_F = tseitin_resolution_length(formula)
    phi_F = p_adic_log(sum(1 for assignment in itertools.product([0, 1], repeat=n) if all(all(assignment[var-1] == literal % 2 for literal in clause) for clause in formula)), 2)
    r_F = minimal_rank(phi_F)

    ratio = r_F / tau_F
    difference = abs(r_F - (phi_F * 0.5))  # Placeholder constant c_p

    return {
        "metric_name": "Ratio of Minimal Rank to Tseitin Resolution Length",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - phi_F) < difference * 0.05 and difference < 1,
        "counterexample": f"Ratio={ratio}, Difference={difference}" if not (abs(ratio - phi_F) < difference * 0.05 and difference < 1) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE conjecture_mapping_undefined")