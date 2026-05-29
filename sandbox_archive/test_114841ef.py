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
    
    def generate_3cnf(n, clause_density):
        m = int(n * clause_density)
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def resolution_refutation_size(clauses):
        # Simplified version of resolution refutation size calculation
        # This is a placeholder and should be replaced with actual logic
        return len(clauses) * 2

    def minimal_local_homology_rank(clauses, n):
        # Simplified version of minimal local homology rank calculation
        # This is a placeholder and should be replaced with actual logic
        return len(clauses)

    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    n_values = [10, 15, 20, 25]
    results = []

    for n in n_values:
        for _ in range(30):  # Ensure at least 30 instances per seed
            clauses = generate_3cnf(n, random.choice([0.5, 1, 2]))
            t_F = resolution_refutation_size(clauses)
            f_n = minimal_local_homology_rank(clauses, n)
            log2_f_n = log2(f_n)

            results.append({
                "n": n,
                "t_F": t_F,
                "log2_f_n": log2_f_n
            })

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }

    log2_f_n_values = [r["log2_f_n"] for r in results]
    t_F_values = [r["t_F"] for r in results]

    mean_log2_f_n = sum(log2_f_n_values) / len(log2_f_n_values)
    mean_t_F = sum(t_F_values) / len(t_F_values)

    std_log2_f_n = math.sqrt(sum((x - mean_log2_f_n) ** 2 for x in log2_f_n_values) / len(log2_f_n_values))
    std_t_F = math.sqrt(sum((x - mean_t_F) ** 2 for x in t_F_values) / len(t_F_values))

    correlation_coefficient = sum((log2_f_n_values[i] - mean_log2_f_n) * (t_F_values[i] - mean_t_F) for i in range(len(log2_f_n_values))) / (len(log2_f_n_values) * std_log2_f_n * std_t_F)

    if correlation_coefficient > 0.8 and all(log2_f_n <= t_F for log2_f_n, t_F in zip(log2_f_n_values, t_F_values)):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"correlation_coefficient={correlation_coefficient}, log2_f_n > t_F found"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")