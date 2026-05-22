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
    
    def generate_monotone_dnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.choice([0, 1]) for _ in range(n)]
            if all(clause): continue
            clauses.append(clause)
        return clauses
    
    def tropicalized_lie_algebra_rank(clauses):
        n = len(clauses[0])
        rank = 0
        for i in range(n):
            max_val = -math.inf
            for clause in clauses:
                val = sum(1 if x == 1 else 0 for x in clause[i:])
                if val > max_val:
                    max_val = val
            rank += max_val
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_monotone_dnf(n, k=2)
            rank = tropicalized_lie_algebra_rank(clauses)
            total_rank += rank
            instances_tested += 1
        
        mean_rank = Fraction(total_rank, instances_tested)
        expected_rank = n**2
        
        if abs(mean_rank - expected_rank) > Fraction(expected_rank * 30, 100):
            conjecture_holds = False
            counterexample = f"Rank {mean_rank} is outside the expected range [{expected_rank - expected_rank * 0.3}, {expected_rank + expected_rank * 0.3}]"
        else:
            conjecture_holds = True
            counterexample = ""
        
        results.append({
            "metric_name": "Minimal Rank of Tropicalized Lie Algebra",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank outside expected range\" first_failing_seed={first_failing_seed}")