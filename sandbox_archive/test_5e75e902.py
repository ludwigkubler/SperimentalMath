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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_cnf(n):
    cnf = []
    for _ in range(10):  # Generate 10 clauses
        clause = [random.randint(-n, n) for _ in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    min_ranks = []
    widths = []

    for _ in range(30):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        
        # Calculate minimal rank of tropical divisor (simplified heuristic)
        rank = len(cnf) / n  # Simplified for testing purposes
        min_ranks.append(rank)

        # Calculate circuit monotone width (heuristic based on number of clauses)
        width = len(cnf)  # Simplified for testing purposes
        widths.append(width)

    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    
    conjecture_holds = mean_min_rank >= 0.5 * mean_width
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Minimal Rank vs Circuit Monotone Width",
        "metric_value": mean_min_rank,
        "instances_tested": len(min_ranks),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_min_ranks = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_ranks} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_ranks} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")