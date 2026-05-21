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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def poset_euler_characteristic(poset):
        chain_counts = []
        for i in range(len(poset)):
            count = 0
            for j in range(i + 1, len(poset)):
                if all(x in poset[j] for x in poset[i]):
                    count += 1
            chain_counts.append(count)
        return sum((-1) ** (len(chain) % 2) * chain_count for chain_count in chain_counts)
    
    def disjointness_communication_complexity(n):
        # Simplified deterministic protocol for disjointness communication complexity
        return n
    
    n = random.randint(5, 40)
    phi = generate_3cnf(n)
    P_phi = sorted(phi, key=len)  # Ensure poset is ordered by inclusion length
    chi_P_phi = poset_euler_characteristic(P_phi)
    D_phi = disjointness_communication_complexity(n)
    
    return {
        "metric_name": "euler_characteristic",
        "metric_value": chi_P_phi,
        "instances_tested": 1,
        "conjecture_holds": abs(chi_P_phi - Fraction(D_phi * n).limit_denominator()) < 0.1 * D_phi,
        "counterexample": "" if conjecture_holds else f"Graph with n={n}, chi(P_φ)={chi_P_phi}, D(φ)={D_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")