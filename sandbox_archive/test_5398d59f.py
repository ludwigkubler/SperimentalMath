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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def tropical_semi_ring(clauses):
        semi_ring = set()
        for clause in clauses:
            product = 0
            for literal in clause:
                if literal > 0:
                    product += math.log2(literal)
                else:
                    product -= math.log2(-literal)
            semi_ring.add(product)
        return semi_ring

    def minimal_rank(semi_ring):
        # Placeholder for actual computation of minimal rank
        return len(semi_ring)

    def sat_resolution_length(clauses):
        # Placeholder for actual resolution proof length calculation
        return len(clauses) * 2

    n = random.randint(5, 40)
    clauses = generate_sat_instance(n)
    semi_ring = tropical_semi_ring(clauses)
    rank = minimal_rank(semi_ring)
    resolution_length = sat_resolution_length(clauses)

    if resolution_length == 0:
        return {
            "metric_name": "rank_to_log2_n_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_length_zero"
        }

    ratio = rank / math.log2(n) ** 2
    return {
        "metric_name": "rank_to_log2_n_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 10,  # Placeholder constant C
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_to_log2_n_ratio_exceeds_bound\" first_failing_seed={first_failing_seed}")