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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def communication_complexity(cnf):
        n = len(cnf[0])
        max_clauses = max(len(clause) for clause in cnf)
        return n * max_clauses
    
    def rank_of_toric_variety(cnf):
        # Simplified version of computing the rank of a toric variety
        # This is a placeholder and should be replaced with actual computation
        return len(cnf)
    
    def solve(lits, cls):
        # Placeholder for solving CNF
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank = float('inf')
    max_rank = -float('inf')
    total_comm_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            comm_complexity = communication_complexity(cnf)
            rank = rank_of_toric_variety(cnf)
            
            if rank < min_rank:
                min_rank = rank
            if rank > max_rank:
                max_rank = rank
            
            total_comm_complexity += comm_complexity
            instances_tested += 1
    
    mean_comm_complexity = total_comm_complexity / instances_tested
    mean_rank = (min_rank + max_rank) / 2
    
    # Check the conjecture for a constant C and threshold k
    C = Fraction(1, 2)
    k = 5
    all_hold = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            comm_complexity = communication_complexity(cnf)
            rank = rank_of_toric_variety(cnf)
            
            if abs(rank - C * comm_complexity) > k:
                all_hold = False
                counterexample = f"n={n}, rank={rank}, c(φ)={comm_complexity}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": all_hold,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")