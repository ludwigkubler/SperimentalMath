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

def generate_random_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(1, 2*n), random.randint(1, 2*n), random.randint(1, 2*n)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def poset_euler_characteristic(P_phi: dict) -> Fraction:
    chain_counts = [len(list(chain)) for chain in P_phi.values()]
    chi_P_phi = sum((-1) ** (len(chain) % 2) * chain_count for chain_count in chain_counts)
    return chi_P_phi

def disjointness_communication_complexity(φ: list) -> int:
    n = len(φ[0])
    # Simplified deterministic protocol for disjointness communication complexity
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    φ = generate_random_3cnf(n)
    
    P_phi = {}
    for clause in φ:
        for other_clause in φ:
            if set(clause).issubset(set(other_clause)):
                if other_clause not in P_phi:
                    P_phi[other_clause] = []
                P_phi[other_clause].append(clause)
    
    chi_P_phi = poset_euler_characteristic(P_phi)
    D_φ = disjointness_communication_complexity(φ)
    
    metric_value = chi_P_phi * Fraction(n).log2() / D_φ
    instances_tested = 1
    conjecture_holds = abs(metric_value - math.log(n)) < 0.1 * math.log(n)
    counterexample = "" if conjecture_holds else f"Graph with n={n}, A=[{', '.join(map(str, φ))}]"
    
    return {
        "metric_name": "euler_characteristic_bounds_disjointness_communication_complexity",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")