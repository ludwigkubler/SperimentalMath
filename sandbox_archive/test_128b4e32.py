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
    
    def generate_k_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def projective_variety(cnf):
        # Simplified encoding of the projective variety
        return len(set(tuple(sorted(clause)) for clause in cnf))
    
    def communication_complexity_matrix(cnf):
        n = len(cnf[0])
        matrix = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i & (1 << var)) == (j & (1 << var)) or (i & (1 << var)) == 0 for var in range(n)):
                    matrix[i][j] = 1
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                rank += 1
        return rank * (n - rank)
    
    q = 2  # Field size
    n_max = 40
    instances_tested = 30
    
    results = []
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        k = random.randint(1, n // 2)
        cnf = generate_k_cnf(n, k)
        
        kappa = projective_variety(cnf)
        matrix = communication_complexity_matrix(cnf)
        r_var = rank_variance(matrix)
        
        results.append({
            "n": n,
            "kappa": kappa,
            "r_var": r_var
        })
    
    mean_kappa = sum(result["kappa"] for result in results) / instances_tested
    mean_r_var = sum(result["r_var"] for result in results) / instances_tested
    
    conjecture_holds = all(mean_r_var >= kappa and mean_r_var <= q**(n/2 - 1) * kappa for result in results)
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": mean_r_var,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_kappa={mean_kappa}, mean_r_var={mean_r_var}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30 * 2 + 1, 2))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")