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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([i, -i]) for i in range(1, n + 1)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def configuration_space_rank(clauses):
        n = max(abs(c) for c in sum(clauses, []))
        rank = 0
        for clause in clauses:
            matrix = []
            for i in range(1, n + 1):
                row = [int(i in clause), int(-i in clause)]
                if any(row[j] == 1 and matrix[k][j] == 1 for k in range(len(matrix))):
                    continue
                matrix.append(row)
            rank = max(rank, len(matrix))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_3cnf(n)
            rank = configuration_space_rank(clauses)
            log_rank = math.log2(rank) if rank > 0 else -math.inf
            results.append((n, log_rank))
    
    total_instances = len(results)
    supported_count = sum(1 for n, log_rank in results if abs(log_rank - n / 3) <= 1 / 3)
    
    conjecture_holds = supported_count >= 0.8 * total_instances
    counterexample = "" if conjecture_holds else "n/3 ± 1/3 not satisfied"
    
    return {
        "metric_name": "log2(rank)",
        "metric_value": sum(log_rank for n, log_rank in results) / total_instances,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n/3 ± 1/3 not satisfied\" first_failing_seed={first_failing_seed}")