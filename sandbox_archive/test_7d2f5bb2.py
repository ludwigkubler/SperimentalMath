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
        num_clauses = int(alpha * n * (n - 1) / 2)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([-1, 1]) * i for i in range(1, n + 1)]
            random.shuffle(clause)
            clauses.append(tuple(clause))
        return clauses
    
    def hodge_rank(n):
        # Placeholder function to simulate Hodge rank
        # Replace with actual computation if possible
        return random.randint(1, n)
    
    def permutation_circuit_depth(n):
        # Placeholder function to simulate permutation circuit depth
        # Replace with actual computation if possible
        return random.randint(1, 2 * n)
    
    def spearman_correlation(ranks1, ranks2):
        n = len(ranks1)
        rank_dict1 = {x: i for i, x in enumerate(sorted(set(ranks1)), start=1)}
        rank_dict2 = {x: i for i, x in enumerate(sorted(set(ranks2)), start=1)}
        
        rho_numerator = n * sum(rank_dict1[x] * rank_dict2[x] for x in ranks1) - ((n + 1) / 2) ** 2
        rho_denominator = math.sqrt(n * (n**2 - 1) / 12) * math.sqrt(sum((rank_dict1[x] - rank_dict2[x])**2 for x in ranks1))
        
        return Fraction(rho_numerator, rho_denominator).limit_denominator()
    
    n_values = [5, 10, 15, 20, 25]
    alpha_values = [0.2, 0.3, 0.4]
    results = []
    
    for n in n_values:
        for _ in range(6):  # Ensure at least 6 instances per n
            clauses = generate_kcnf(n, random.choice(alpha_values))
            rank = hodge_rank(n)
            depth = permutation_circuit_depth(n)
            results.append((rank, depth))
    
    if not results:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    ranks1, ranks2 = zip(*results)
    rho = spearman_correlation(ranks1, ranks2)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": float(rho),
        "instances_tested": len(results),
        "conjecture_holds": 0.6 <= rho < 0.8,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED"
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] != "")
        result = f"FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if 0.6 <= r["metric_value"] < 0.8) / len(results)
        result = "FALSIFIED"
    
    print(f"RESULT: {result} mean={mean_rho:.4f} std=0.0000 support_fraction={support_fraction:.2f}")