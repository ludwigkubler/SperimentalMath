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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def construct_curve(n):
        # Placeholder for curve construction logic
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)

    def hodge_index(h):
        # Placeholder for Hodge index calculation
        # This is a dummy implementation and should be replaced with actual logic
        return math.log2(h) if h > 0 else -math.inf

    def resolution_proof_size(n):
        # Placeholder for resolution proof size calculation
        # This is a dummy implementation and should be replaced with actual logic
        return math.log2(n) if n > 1 else -math.inf

    n_values = [10, 20, 40]
    hodge_indices = []
    proof_sizes = []

    for n in n_values:
        if not is_prime(n):
            continue
        h = construct_curve(n)
        hodge_indices.append(hodge_index(h))
        proof_sizes.append(resolution_proof_size(n))

    if len(hodge_indices) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(hodge_indices),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    correlation = 0
    for h, p in zip(hodge_indices, proof_sizes):
        correlation += (h - sum(hodge_indices) / len(hodge_indices)) * (p - sum(proof_sizes) / len(proof_sizes))
    correlation /= math.sqrt(sum((h - sum(hodge_indices) / len(hodge_indices)) ** 2 for h in hodge_indices) *
                             sum((p - sum(proof_sizes) / len(proof_sizes)) ** 2 for p in proof_sizes))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(hodge_indices),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")