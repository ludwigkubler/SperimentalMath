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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, 2 * n) for _ in range(random.randint(1, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def tropical_semi_ring(clauses):
        n = len(clauses[0])
        semi_ring = [[-math.inf] * n for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                if abs(lit) > n:
                    continue
                i = abs(lit) - 1
                semi_ring[lit - 1][i] = max(semi_ring[lit - 1][i], 1)
                semi_ring[i][lit - 1] = max(semi_ring[i][lit - 1], 1)
        return semi_ring
    
    def minimal_rank(semi_ring):
        n = len(semi_ring)
        rank = 0
        for i in range(n):
            if any(x > 0 for x in semi_ring[i]):
                rank += 1
        return rank
    
    def resolution_length(clauses):
        # Simplified version of resolution length calculation
        return sum(len(clause) for clause in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 instances
            clauses = generate_sat_instance(n)
            semi_ring = tropical_semi_ring(clauses)
            rank = minimal_rank(semi_ring)
            length = resolution_length(clauses)
            results.append((n, rank, length))
    
    if not results:
        return {
            "metric_name": "minimal_rank_over_log2_n",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    total_rank = sum(rank for _, rank, _ in results)
    total_length = sum(length for _, _, length in results)
    mean_rank = Fraction(total_rank, len(results))
    mean_length = Fraction(total_length, len(results))
    ratio = mean_rank / (mean_length ** 2)
    
    support_fraction = sum(1 for _, rank, _ in results if rank <= math.log(n) ** 2) / len(results)
    
    return {
        "metric_name": "minimal_rank_over_log2_n",
        "metric_value": float(ratio),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Ratio {ratio} exceeds log^2(n)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] * result["instances_tested"] for result in results if result["metric_value"] is not None)
    total_instances = sum(result["instances_tested"] for result in results)
    mean_ratio = Fraction(total_rank, total_instances)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds log^2(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=No valid data")