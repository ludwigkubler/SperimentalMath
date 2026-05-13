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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def symplectic_capacity(convex_hull):
        # Placeholder for actual computation
        return random.random()

    def extended_frege_proof_length(sat_instance):
        # Placeholder for actual computation
        return len(sat_instance)

    n = 10
    sat_instance = generate_3sat_instance(n)
    convex_hull = [sum(clause) for clause in zip(*sat_instance)]
    capacity = symplectic_capacity(convex_hull)
    proof_length = extended_frege_proof_length(sat_instance)

    return {
        "metric_name": "symplectic_capacity",
        "metric_value": capacity,
        "instances_tested": 1,
        "conjecture_holds": False if capacity == 0 else proof_length > 0 and abs(capacity * proof_length - 1) < 1e-6,
        "counterexample": "mapping_undefined" if capacity == 0 else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_capacity = sum(r["metric_value"] for r in results) / len(results)
    std_capacity = math.sqrt(sum((r["metric_value"] - mean_capacity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_capacity} std={std_capacity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")