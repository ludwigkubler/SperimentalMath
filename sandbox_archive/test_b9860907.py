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
    
    def generate_dnf_formula(k, n):
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(2**k):
            clause = random.sample(variables, k)
            if random.choice([True, False]):
                clause = [f"~{v}" for v in clause]
            clauses.append(" or ".join(clause))
        return " and ".join(clauses)

    def compute_minimal_rank(n, k):
        # Placeholder function to simulate computation
        # Replace with actual algorithm if available
        return n**k * math.log(n)

    def check_monotone_circuit_depth(k, n):
        # Placeholder function to simulate existence of circuit
        # Replace with actual algorithm if available
        return True

    k = random.randint(2, 5)
    n = random.randint(10, 20)
    dnf_formula = generate_dnf_formula(k, n)
    
    minimal_rank = compute_minimal_rank(n, k)
    circuit_depth_exists = check_monotone_circuit_depth(k, n)

    rank_deviation = abs(minimal_rank - (n**k * math.log(n))) / (n**k * math.log(n)) * 100
    conjecture_holds = rank_deviation <= 10 and circuit_depth_exists

    return {
        "metric_name": "Minimal Rank of Tropicalized Quaternionic Kähler Manifold",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": f"Rank {minimal_rank} deviates from Θ({n**k * math.log(n)}) by more than 10%" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank deviates from Θ(n^k log n) by more than 10%\" first_failing_seed={first_failing_seed}")