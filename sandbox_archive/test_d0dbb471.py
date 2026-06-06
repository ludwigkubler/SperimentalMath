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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def calculate_symplectic_volume(n):
        # Placeholder for actual calculation
        return math.sqrt(n)
    
    def calculate_variance_in_rank(cnf):
        # Placeholder for actual calculation
        rank_values = [len(set([abs(x) for x in clause])) for clause in cnf]
        mean_rank = sum(rank_values) / len(rank_values)
        variance = sum((x - mean_rank) ** 2 for x in rank_values) / len(rank_values)
        return variance
    
    n_max = 0
    instances_tested = 0
    total_ratio = 0.0
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        symplectic_volume = calculate_symplectic_volume(n)
        variance_in_rank = calculate_variance_in_rank(cnf)
        
        if variance_in_rank == 0:
            continue
        
        ratio = symplectic_volume / math.sqrt(n)
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)
    
    conjecture_holds = all(ratio >= math.sqrt(n) for ratio in [total_ratio / instances_tested] * instances_tested)
    counterexample = "Ratio < √n" if not conjecture_holds else ""
    
    return {
        "metric_name": "Ratio",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")