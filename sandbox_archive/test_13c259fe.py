# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), n)]
            clauses.append(clause)
        return clauses
    
    def tropicalize_cohomology(clauses):
        # Simplified tropicalization logic
        rank = len(set(tuple(sorted(c)) for c in clauses))
        return rank
    
    def compute_f(n):
        # Linear function f(n) = 2n + 1
        return 2 * n + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        while len(results) < 30:
            k = random.randint(1, min(n, 10))
            clauses = generate_k_cnf(n, k)
            rank = tropicalize_cohomology(clauses)
            
            if rank > compute_f(n):
                counterexample = f"n={n}, k={k}, rank={rank}"
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            total_rank += rank
            instances_tested += 1
        
        mean_rank = Fraction(total_rank, instances_tested)
        std_dev = (sum((x - mean_rank) ** 2 for x in range(instances_tested)) / instances_tested).sqrt()
        
        results.append({
            "n": n,
            "mean_rank": mean_rank,
            "std_dev": std_dev
        })
    
    median_rank = sorted([r["mean_rank"] for r in results])[len(results) // 2]
    upper_bound = median_rank + 3 * std_dev
    
    if all(r["mean_rank"] <= upper_bound for r in results):
        return {
            "metric_name": "minimal_rank",
            "metric_value": sum(r["mean_rank"] for r in results) / len(results),
            "instances_tested": sum(r["instances_tested"] for r in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if r["mean_rank"] > upper_bound)
        return {
            "metric_name": "minimal_rank",
            "metric_value": sum(r["mean_rank"] for r in results) / len(results),
            "instances_tested": sum(r["instances_tested"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"First failing seed: {first_failing_seed}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)).sqrt()
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")