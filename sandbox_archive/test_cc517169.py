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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0', '1']
        else:
            subcircuits = [generate_boolean_circuit(n-1) for _ in range(2)]
            return ['(' + a + b + ')' for a in subcircuits[0] for b in subcircuits[1]]
    
    def frege_proof_depth(circuit):
        if '0' not in circuit and '1' not in circuit:
            return 0
        else:
            return max(frege_proof_depth(subcircuit) for subcircuit in circuit.split('()')) + 1
    
    def hodge_bundle_metric_order(n):
        # Simplified model: order is proportional to the number of variables
        return n
    
    def compute_hodge_bundle_metric(circuit):
        n = len(circuit)
        return hodge_bundle_metric_order(n)
    
    trials = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_boolean_circuit(n)
        order = compute_hodge_bundle_metric(circuit)
        depth = frege_proof_depth(circuit)
        trials.append((order, depth))
    
    if not trials:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_trials"
        }
    
    n = len(trials)
    sum_order = sum(order for order, _ in trials)
    sum_depth = sum(depth for _, depth in trials)
    sum_order_depth = sum(order * depth for order, depth in trials)
    sum_order_squared = sum(order ** 2 for order, _ in trials)
    sum_depth_squared = sum(depth ** 2 for _, depth in trials)
    
    mean_order = Fraction(sum_order, n)
    mean_depth = Fraction(sum_depth, n)
    numerator = n * sum_order_depth - sum_order * sum_depth
    denominator = (n * sum_order_squared - sum_order ** 2) * (n * sum_depth_squared - sum_depth ** 2)
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n for _, n in trials),
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    r = numerator / denominator ** Fraction(1, 2)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float(r),
        "instances_tested": n,
        "n_max": max(n for _, n in trials),
        "conjecture_holds": abs(float(r)) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        mean_r = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / sum(1 for result in results if result["metric_value"] is not None)
        std_r = (sum((result["metric_value"] - mean_r) ** 2 for result in results if result["metric_value"] is not None) / sum(1 for result in results if result["metric_value"] is not None)) ** Fraction(1, 2)
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")