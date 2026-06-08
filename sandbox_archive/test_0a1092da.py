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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def dpll(cnf):
        def search(assignments):
            if not cnf:
                return True
            literal = next((l for l in range(1, n+1) if l not in assignments and -l not in assignments), None)
            if literal is None:
                return False
            for value in [True, False]:
                new_assignments = assignments.copy()
                new_assignments[literal] = value
                if search(new_assignments):
                    return True
            return False
        
        n = max(abs(l) for clause in cnf for l in clause)
        return len(cnf), search({})

    def quandle_rank(cnf):
        # Simplified mapping of CNF to a quandle rank (placeholder)
        return len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            rank = quandle_rank(cnf)
            proof_length, _ = dpll(cnf)
            results.append((rank, proof_length))

    if not results:
        return {
            "metric_name": "quandle_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }

    ranks = [r for r, _ in results]
    proof_lengths = [l for _, l in results]

    mean_rank = sum(ranks) / len(ranks)
    mean_length = sum(proof_lengths) / len(proof_lengths)

    covariance = sum((r - mean_rank) * (l - mean_length) for r, l in results)
    variance_ranks = sum((r - mean_rank)**2 for r in ranks)
    variance_lengths = sum((l - mean_length)**2 for l in proof_lengths)

    if variance_ranks == 0 or variance_lengths == 0:
        return {
            "metric_name": "quandle_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }

    correlation_coefficient = covariance / (math.sqrt(variance_ranks) * math.sqrt(variance_lengths))

    return {
        "metric_name": "quandle_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")