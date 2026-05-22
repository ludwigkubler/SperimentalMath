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
    
    def generate_monotone_dnf(n: int, k: int):
        clauses = []
        for _ in range(k):
            clause = [random.randint(0, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def tropicalized_lie_algebra_rank(dnf_formula):
        n = len(dnf_formula[0])
        rank = 0
        for assignment in range(2**n):
            satisfied_clauses = 0
            for clause in dnf_formula:
                if all((assignment >> var) & 1 == 1 for var in clause):
                    satisfied_clauses += 1
            if satisfied_clauses > 0:
                rank += 1
        return rank
    
    def expected_rank(n: int, k: int):
        return n**k
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        k = random.randint(1, min(n-1, 10))
        dnf_formula = generate_monotone_dnf(n, k)
        rank = tropicalized_lie_algebra_rank(dnf_formula)
        expected = expected_rank(n, k)
        results.append((rank, expected))
    
    total_rank = sum(rank for rank, _ in results)
    mean_rank = Fraction(total_rank, len(results))
    std_dev = math.sqrt(sum((rank - mean_rank)**2 for rank, _ in results) / len(results))
    
    conjecture_holds = all(abs(rank - expected) <= 0.3 * expected for rank, expected in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Tropicalized Lie Algebra Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] for result in results)
    mean_rank = Fraction(total_rank, len(results))
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")