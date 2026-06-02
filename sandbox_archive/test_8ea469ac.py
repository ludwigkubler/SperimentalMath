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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def solve(model):
            if not cnf:
                return model
            literal = next((l for l in range(1, n + 1) if l not in model and -l not in model), None)
            if literal is None:
                return None
            new_model = model.copy()
            new_model[literal] = True
            result = solve(new_model)
            if result is not None:
                return result
            new_model[literal] = False
            new_model[-literal] = True
            return solve(new_model)
        n = len(cnf[0])
        return solve({})

    def automorphic_representation(cnf):
        # Placeholder for actual implementation of automorphic representation
        return random.randint(1, 10)

    def tropicalize(rep):
        # Placeholder for actual implementation of tropicalization
        return rep

    def resolution_width(cnf):
        model = dpll(cnf)
        if model is None:
            return float('inf')
        width = 0
        for clause in cnf:
            if not any(lit in model and not model[lit] for lit in clause):
                width += 1
        return width

    results = []
    instances_tested = 0
    n_max = 0
    rank_sum = 0
    width_sum = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            instances_tested += 1
            n_max = max(n_max, n)
            rep = automorphic_representation(cnf)
            tau_rep = tropicalize(rep)
            rank = len(tau_rep)  # Placeholder for actual minimal rank calculation
            width = resolution_width(cnf)
            results.append((rank, width))
            rank_sum += rank
            width_sum += width

    if not results:
        return {
            "metric_name": "MinimalRank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }

    rank_mean = Fraction(rank_sum, instances_tested)
    width_mean = Fraction(width_sum, instances_tested)

    correlation = sum((r - rank_mean) * (w - width_mean) for r, w in results) / (instances_tested * math.sqrt(sum((r - rank_mean)**2 for r, _ in results)) * math.sqrt(sum((w - width_mean)**2 for _, w in results)))

    return {
        "metric_name": "MinimalRank",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) > 0.8 and all(abs(r - rank_mean) <= 3 for r, _ in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")