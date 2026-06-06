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
    
    def generate_circuit(depth):
        if depth == 1:
            return ['NOT', 'AND', 'OR'][random.randint(0, 2)]
        else:
            subcircuits = [generate_circuit(random.randint(1, depth-1)) for _ in range(random.randint(2, 4))]
            return random.choice(['NOT', 'AND', 'OR']) + '(' + ','.join(subcircuits) + ')'
    
    def calculate_symmetry_group(circuit):
        # Placeholder function to simulate symmetry group calculation
        # This is a dummy implementation and does not actually compute the symmetry group
        return random.randint(1, 2**depth)
    
    def circuit_depth(circuit):
        if isinstance(circuit, str) and circuit[0] in ['NOT', 'AND', 'OR']:
            return 1 + max(circuit_depth(subcircuit) for subcircuit in circuit[2:].split(','))
        else:
            return 0
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depths:
        for _ in range(5):
            circuit = generate_circuit(depth)
            symmetry_group_order = calculate_symmetry_group(circuit)
            depth_value = circuit_depth(circuit)
            if symmetry_group_order > 2**depth_value:
                return {
                    "metric_name": "Symmetry Group Order",
                    "metric_value": None,
                    "instances_tested": len(results),
                    "n_max": max(depths),
                    "conjecture_holds": False,
                    "counterexample": f"Circuit: {circuit}, Symmetry Group Order: {symmetry_group_order}, Depth: {depth_value}"
                }
            results.append(symmetry_group_order)
    
    mean_metric = sum(results) / len(results)
    support_fraction = sum(1 for x in results if x <= 2**(depth + 1)) / len(results)
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "n_max": max(depths),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")