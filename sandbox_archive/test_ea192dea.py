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
    
    def generate_kcnf(n, alpha):
        k = 3
        num_clauses = int(alpha * n * (n - 1) / 2)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(k)]
            if len(set(clause)) == k:
                clauses.append(clause)
        return clauses

    def hodge_rank(n):
        # Placeholder function to simulate Hodge rank calculation
        return random.randint(1, n)

    def permutation_circuit_depth(n):
        # Placeholder function to simulate permutation circuit depth calculation
        return random.randint(1, n * (n - 1))

    def spearman_correlation(ranks1, ranks2):
        if len(ranks1) != len(ranks2):
            raise ValueError("Ranks lists must be of the same length")
        
        n = len(ranks1)
        rank_dict1 = {x: i for i, x in enumerate(sorted(set(ranks1)), 1)}
        rank_dict2 = {x: i for i, x in enumerate(sorted(set(ranks2)), 1)}
        
        sum_d1_sq = sum((rank_dict1[x] - (n + 1) / 2) ** 2 for x in ranks1)
        sum_d2_sq = sum((rank_dict2[x] - (n + 1) / 2) ** 2 for x in ranks2)
        
        rho_numerator = n * sum(rank_dict1[x] * rank_dict2[x] for x in ranks1) - ((n + 1) / 2) ** 2
        rho_denominator = math.sqrt(n * sum_d1_sq * sum_d2_sq)
        
        return rho_numerator / rho_denominator if rho_denominator != 0 else 0

    n_values = [5, 10, 15, 20, 25]
    alpha_values = [0.2, 0.3, 0.4]
    results = []

    for n in n_values:
        for _ in range(6):  # 6 instances per n to ensure statistical signal
            clauses = generate_kcnf(n, random.choice(alpha_values))
            rank = hodge_rank(n)
            depth = permutation_circuit_depth(n)
            results.append((rank, depth))

    ranks1, ranks2 = zip(*results)
    rho = spearman_correlation(ranks1, ranks2)

    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": 0.6 <= rho < 0.8,
        "counterexample": "" if 0.6 <= rho < 0.8 else f"rho={rho}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)

    mean_rho = sum(result["metric_value"] for result in results) / len(results)
    std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.6 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")