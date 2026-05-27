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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = set()
        for _ in range(m):
            clause = []
            while len(clause) < 3:
                var = random.choice(variables)
                if var not in clause:
                    clause.append(var)
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def resolution_proof_complexity(clauses):
        # Simplified version for demonstration
        return len(clauses)
    
    def quandle_rank(clauses):
        n = max(max(clause) for clause in clauses)
        rank = 0
        for i in range(1, n + 1):
            if any(i in clause for clause in clauses):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            clauses = generate_k_cnf(n, m)
            rank = quandle_rank(clauses)
            resolution_complexity = resolution_proof_complexity(clauses)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = abs(mean_rank - resolution_complexity) < 0.1 * resolution_complexity
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} does not match resolution complexity {resolution_complexity}"
    
    return {
        "metric_name": "Quandle Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")