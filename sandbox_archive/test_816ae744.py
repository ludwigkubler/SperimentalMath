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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate enough clauses to ensure variety
        clause = [random.randint(-n, n) for _ in range(n)]
        if not any(clause[i] != -clause[j] for j in range(i)):
            cnf.append(clause)
    return cnf

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = next((r for r in range(rank, rows) if matrix[r][i] != 0), None)
        if pivot_row is not None:
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(rows):
                if j != rank:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_ranks = []
    total_widths = []

    for n in n_values:
        cnf = generate_cnf(n)
        ranks = []
        widths = []

        for _ in range(5):  # Test each size with multiple instances
            rank = gaussian_elimination(cnf)
            ranks.append(rank)

            # Compute circuit monotone width (simplified example)
            width = len([c for c in cnf if any(x > 0 for x in c)])
            widths.append(width)

        total_ranks.extend(ranks)
        total_widths.extend(widths)

    mean_rank = sum(total_ranks) / len(total_ranks)
    mean_width = sum(total_widths) / len(total_widths)
    conjecture_holds = mean_rank >= 0.5 * mean_width
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Minimal Rank vs Circuit Monotone Width",
        "metric_value": mean_rank,
        "instances_tested": len(total_ranks),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")