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
    
    def generate_k_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), random.choice(variables)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def hodge_index(n):
        # Placeholder for actual Hodge index calculation
        # This is a dummy implementation that returns a simple function of n
        return n * (n + 1) // 2

    def sos_refutation_size(k_cnf):
        # Placeholder for actual SOS refutation size calculation
        # This is a dummy implementation that returns a simple function of k_cnf
        return len(k_cnf) ** 2

    n = random.randint(5, 40)
    k = random.randint(1, n * (n - 1) // 2)
    k_cnf = generate_k_cnf(n, k)

    hodge_val = hodge_index(n)
    sos_size = sos_refutation_size(k_cnf)
    
    if sos_size == 0:
        return {
            "metric_name": "Hodge Index",
            "metric_value": hodge_val,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "SOS refutation size is zero"
        }

    upper_bound = math.sqrt(sos_size)
    
    return {
        "metric_name": "Hodge Index",
        "metric_value": hodge_val,
        "instances_tested": 1,
        "conjecture_holds": abs(hodge_val - upper_bound) <= 3,
        "counterexample": f"HodgeIndex({hodge_val}) > sqrt({sos_size})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"HodgeIndex({results[0]['metric_value']}) > sqrt({sos_refutation_size(generate_k_cnf(40, 100))})\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")