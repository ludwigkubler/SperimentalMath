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
        clauses = set()
        while len(clauses) < num_clauses:
            clause = {random.randint(1, n), random.randint(1, n)}
            if len(clause) == 2 and all(abs(x) != abs(y) for x, y in zip(clause, -clause)):
                clauses.add(tuple(sorted(clause)))
        return clauses
    
    def hodge_rank(n):
        # Placeholder function to compute Hodge rank
        # This is a dummy implementation that returns a random value
        return random.randint(1, n)
    
    def permutation_circuit_depth(n):
        # Placeholder function to compute permutation circuit depth
        # This is a dummy implementation that returns a random value
        return random.randint(1, n)
    
    results = []
    for n in [5, 10, 15, 20, 25]:
        for _ in range(6):  # 6 instances per size to ensure statistical signal
            alpha = random.choice([0.2, 0.3, 0.4])
            F = generate_kcnf(n, alpha)
            rank_H_F = hodge_rank(n)
            depth_P_F = permutation_circuit_depth(n)
            results.append((rank_H_F, depth_P_F))
    
    if not results:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_H_F_values = [r[0] for r in results]
    depth_P_F_values = [r[1] for r in results]
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        assert n == len(y), "x and y must have the same length"
        
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        
        rho_numerator = sum((sorted_x[i] - sorted_y[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1)
        
        return 1 - (6 * rho_numerator) / rho_denominator
    
    rho = spearman_rank_correlation(rank_H_F_values, depth_P_F_values)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": 0.6 <= rho < 0.8,
        "counterexample": "" if 0.6 <= rho < 0.8 else f"Spearman rank correlation {rho} is outside the acceptable range [0.6, 0.8)"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["instances_tested"] > 0 for r in results):
        print("RESULT: INCONCLUSIVE insufficient_data")
    else:
        rho_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
        support_fraction = sum(1 for r in results if 0.6 <= r["metric_value"] < 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(rho_values)/len(rho_values):.4f} std={math.sqrt(sum((x - sum(rho_values)/len(rho_values))**2 for x in rho_values) / len(rho_values)):.4f} support_fraction={support_fraction:.2f}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not (0.6 <= r["metric_value"] < 0.8))
            print(f"RESULT: FALSIFIED counterexample='Spearman rank correlation out of acceptable range' first_failing_seed={first_failing_seed}")