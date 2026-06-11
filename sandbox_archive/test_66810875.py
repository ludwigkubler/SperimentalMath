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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0', '1']
        else:
            subcircuits = [generate_boolean_circuit(n // 2) for _ in range(2)]
            return ['(' + a + b + ')' for a in subcircuits[0] for b in subcircuits[1]]
    
    def frege_proof_depth(circuit):
        if circuit == '0' or circuit == '1':
            return 1
        else:
            return 1 + max(frege_proof_depth(a) for a in circuit.split('(')[1].split(')')[0].split('+'))
    
    def hodge_bundle_metric_order(n):
        # Simplified model: order is proportional to the number of variables
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    orders = []
    depths = []
    
    for n in n_values:
        circuits = generate_boolean_circuit(n)
        for _ in range(5):
            circuit = random.choice(circuits)
            order = hodge_bundle_metric_order(n)
            depth = frege_proof_depth(circuit)
            orders.append(order)
            depths.append(depth)
    
    if not orders or not depths:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = sum(orders) / len(orders)
    mean_depth = sum(depths) / len(depths)
    covariance = sum((x - mean_order) * (y - mean_depth) for x, y in zip(orders, depths)) / len(orders)
    variance_order = sum((x - mean_order) ** 2 for x in orders) / len(orders)
    variance_depth = sum((y - mean_depth) ** 2 for y in depths) / len(depths)
    
    if variance_order == 0 or variance_depth == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_r = covariance / (math.sqrt(variance_order) * math.sqrt(variance_depth))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_r,
        "instances_tested": len(orders),
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_r) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + \
            [31, 37, 41, 43, 47, 53, 59, 61, 67, 71] + \
            [73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")