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

def generate_3cnf(n):
    clauses = []
    for _ in range(n):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(3)]
        clause = tuple(sorted(literals))
        if clause not in clauses:
            clauses.append(clause)
    return clauses

def configuration_space_rank(clauses):
    n = len(clauses)
    matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            if any(l in clauses[i] and -l in clauses[j] for l in set(clauses[i]) & set(clauses[j])):
                matrix[i][j] += 1
                matrix[j][i] += 1
    
    rank = 0
    for row in range(n):
        pivot = next((col for col in range(row, n) if matrix[row][col]), None)
        if pivot is not None:
            rank += 1
            for col in range(n):
                matrix[row][col] /= matrix[pivot][pivot]
            for i in range(n):
                if i != row:
                    factor = matrix[i][pivot]
                    for j in range(n):
                        matrix[i][j] -= factor * matrix[row][j]
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        clauses = generate_3cnf(n)
        rank = configuration_space_rank(clauses)
        log_rank = math.log2(rank) if rank > 0 else -math.inf
        expected = n / 3
        results.append((n, log_rank, expected))
    
    mean_log_rank = sum(log_rank for _, log_rank, _ in results) / len(results)
    std_dev = math.sqrt(sum((log_rank - mean_log_rank) ** 2 for _, log_rank, _ in results) / len(results))
    support_fraction = sum(1 for _, log_rank, expected in results if abs(log_rank - expected) <= expected / 3) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "n/3 bound not met"
    
    return {
        "metric_name": "log2(rank)",
        "metric_value": mean_log_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    mean_log_rank = sum(trial_result["metric_value"] for trial_result in seeds) / len(seeds)
    std_dev = math.sqrt(sum((trial_result["metric_value"] - mean_log_rank) ** 2 for trial_result in seeds) / len(seeds))
    support_fraction = sum(1 for trial_result in seeds if trial_result["conjecture_holds"]) / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in seeds):
        first_failing_seed = next(seed for seed, result in enumerate(seeds) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n/3 bound not met\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")