# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if any(abs(c) == abs(d) for c, d in zip(clause, clause[1:])):
                continue
            clauses.append(clause)
        return clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(abs(x) == abs(y) and x != y for x in stack[i] for y in stack[j]):
                        new_clause = [x for x in stack[i] if x not in stack[j]] + [y for y in stack[j] if y not in stack[i]]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
    
    def hypergeometric_moments(clauses, n):
        moments = []
        for k in range(1, int(n**(1/3)) + 2):
            moment = Fraction(0)
            for clause in clauses:
                moment += sum(abs(x) for x in clause)**k
            moments.append(moment / len(clauses))
        return moments
    
    def spearman_rank_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        rank_x = {v: i + 1 for i, v in enumerate(sorted(set(x)))}
        rank_y = {v: i + 1 for i, v in enumerate(sorted(set(y)))}
        n = len(x)
        sum_dif_ranks_squared = sum((rank_x[x[i]] - rank_y[y[i]])**2 for i in range(n))
        return (n * sum_dif_ranks_squared - n*(n+1)**2/4) / math.sqrt(6 * n * (n-1) * (2*n+5))

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clauses = generate_cnf(n)
        proof_length = resolution_length(clauses)
        moments = hypergeometric_moments(clauses, n)
        log_moments = [math.log(m) for m in moments]
        results.append({"n": n, "proof_length": proof_length, "log_moments": log_moments})
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    log_moments = [item["log_moments"] for item in results]
    proof_lengths = [item["proof_length"] for item in results]
    corr_coeff = spearman_rank_correlation(log_moments, proof_lengths)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "conjecture_holds": corr_coeff > 0.99,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in result or result["metric_value"] is None for result in results):
        print("RESULT: INCONCLUSIVE no_data")
    else:
        avg_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={avg_corr_coeff} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation below threshold\" first_failing_seed={first_failing_seed}")