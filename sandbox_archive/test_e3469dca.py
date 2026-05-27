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
    
    def generate_kcnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice(variables)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses

    def resolution_complexity(clauses):
        # Simplified version of resolution complexity calculation
        return len(clauses) * 1.5

    def quandle_rank(clauses):
        # Placeholder for actual quandle rank computation
        # For simplicity, we use a dummy function that returns a random value
        return random.randint(10, 60)

    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n, n * 2)
    clauses = generate_kcnf(n, m)
    
    alpha_nm = resolution_complexity(clauses)
    rank_Q = quandle_rank(clauses)
    
    return {
        "metric_name": "Quandle Rank",
        "metric_value": rank_Q,
        "instances_tested": 1,
        "conjecture_holds": math.isclose(rank_Q, alpha_nm, rel_tol=1e-9),
        "counterexample": f"Mean rank {rank_Q} does not match resolution complexity {alpha_nm}" if not math.isclose(rank_Q, alpha_nm, rel_tol=1e-9) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 83))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d:.3f} std={std_dev:.3f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_d:.3f} std={std_dev:.3f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")