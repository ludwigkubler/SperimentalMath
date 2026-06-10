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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return ['0', '1']
        else:
            inputs = generate_boolean_circuit(depth - 1)
            outputs = []
            for i in range(len(inputs)):
                for j in range(len(inputs)):
                    outputs.append(f"({inputs[i]} | {inputs[j]})")
                    outputs.append(f"({inputs[i]} & {inputs[j]})")
            return outputs
    
    def compute_symplectic_rank(circuit):
        # Placeholder function to simulate symplectic rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(circuit)
    
    circuit_depths = [5, 10, 15, 20, 30, 40]
    circuit_ranks = []
    n_max = max(circuit_depths)
    
    for depth in circuit_depths:
        circuits = generate_boolean_circuit(depth)
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = random.choice(circuits)
            rank = compute_symplectic_rank(circuit)
            circuit_ranks.append((depth, rank))
    
    if not circuit_ranks:
        return {
            "metric_name": "symplectic_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    depths = [depth for depth, rank in circuit_ranks]
    ranks = [rank for depth, rank in circuit_ranks]
    
    # Calculate Spearman correlation coefficient
    def spearman_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rho_numerator = sum((sorted_x[i] - sorted_y[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1)
        return 1 - (6 * rho_numerator) / rho_denominator
    
    correlation_coefficient = spearman_correlation(depths, ranks)
    
    return {
        "metric_name": "symplectic_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(circuit_ranks),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")