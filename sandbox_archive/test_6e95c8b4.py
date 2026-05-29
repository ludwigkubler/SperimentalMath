# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import math
import random
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gamma(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def hypergeometric_moment(n, k):
        if k > n:
            return 0
        return math.comb(n, k) / gamma(2 + n / 2)
    
    def resolution_proof_length(n):
        # Placeholder function for actual proof length calculation
        return n * (n + 1) // 2
    
    def spearman_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        
        n = len(x)
        rank_x = {v: i for i, v in enumerate(sorted(set(x)), start=1)}
        rank_y = {v: i for i, v in enumerate(sorted(set(y)), start=1)}
        
        dx = [rank_x[x[i]] - rank_y[y[i]] for i in range(n)]
        dxx = sum(xi * xi for xi in dx)
        dxy = sum(dx[i] * dx[j] for i in range(n) for j in range(i + 1, n))
        
        return (n * dxx - dxy**2) / ((n * n - 1) * dxx)

    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def cnf_to_clause_distribution(cnf):
        distribution = {}
        for clause in cnf:
            length = len(clause)
            if length not in distribution:
                distribution[length] = 0
            distribution[length] += 1
        return distribution

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        clause_distribution = cnf_to_clause_distribution(cnf)
        
        moments = [hypergeometric_moment(n, k) for k in range(n + 1)]
        proof_length = resolution_proof_length(n)
        
        results.append((moments, proof_length))
    
    if not results:
        return {
            "metric_name": "Spearman correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    log_moments = [math.log(m) for m in results[0][0]]
    proof_lengths = [r[1] for r in results]
    
    correlation = spearman_correlation(log_moments, proof_lengths)
    
    return {
        "metric_name": "Spearman correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation > 0.99,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")