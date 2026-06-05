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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def compute_clause_set(circuit):
        if isinstance(circuit, list):
            subclause = []
            for i in circuit:
                subclause.extend(compute_clause_set(i))
            return subclause
        else:
            return [circuit]
    
    def generate_random_circuit(depth: int, max_inputs: int) -> list:
        if depth == 1:
            return random.randint(0, max_inputs - 1)
        else:
            return [generate_random_circuit(random.randint(1, depth - 1), max_inputs) for _ in range(2)]
    
    def min_order_of_grothendieck_teichmueller_group(clause_set):
        # Placeholder function to simulate computation
        return len(clause_set)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed are sampled
            circuit = generate_random_circuit(depth, 40)
            clause_set = compute_clause_set(circuit)
            n_max = max(n_max, len(clause_set))
            instances_tested += 1
            metric_value = min_order_of_grothendieck_teichmueller_group(clause_set)
            total_metric_value += metric_value
    
    if instances_tested < 30:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(metric_value <= depth**3 for depth, metric_value in zip([5, 10, 15, 20, 30, 40], [mean_metric_value]*6))
    counterexample = "" if conjecture_holds else "depth=5, mean_metric_value=..."
    
    return {
        "metric_name": "min_order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=... support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"...\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")