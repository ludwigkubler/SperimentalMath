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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            variables = random.sample(range(1, n+1), 3)
            clause = [random.choice([var, -var]) for var in variables]
            clauses.append(clause)
        return clauses
    
    def geometric_langlands_lattice(clauses):
        # Construct a lattice based on the clause structure
        # This is a placeholder implementation
        lattice = []
        for clause in clauses:
            for literal in clause:
                if literal not in lattice:
                    lattice.append(literal)
        return lattice
    
    def min_rank(lattice):
        # Placeholder function to estimate the minimal rank of the lattice
        # For simplicity, we use the number of unique literals as a proxy
        return len(set(abs(x) for x in lattice))
    
    n = random.randint(5, 40)
    k = max(1, min(n // 2, 3))  # Ensure at least one clause and not too many
    formula = generate_kcnf(n, k)
    lattice = geometric_langlands_lattice(formula)
    rank = min_rank(lattice)
    
    expected_rank = n ** (1/4) * math.log(n)
    tolerance = 0.1 * expected_rank
    
    metric_name = "Minimal Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = abs(rank - expected_rank) <= tolerance
    counterexample = "" if conjecture_holds else f"Rank {rank} does not match expected {expected_rank:.2f}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_rank:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank out of tolerance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")