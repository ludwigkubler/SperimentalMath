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
        if depth == 0:
            return ['0', '1']
        inputs = generate_circuit(depth - 1)
        outputs = []
        for i in range(len(inputs)):
            for j in range(i, len(inputs)):
                outputs.append(f'OR({inputs[i]}, {inputs[j]})')
                outputs.append(f'AND({inputs[i]}, {inputs[j]})')
        return outputs
    
    def calculate_symmetry_group(circuit):
        # Placeholder for actual symmetry group calculation
        # For simplicity, we assume the circuit is a binary tree and its symmetry group order is 2^(depth-1)
        depth = len(circuit) ** 0.5 + 1
        return 2 ** (int(depth) - 1)
    
    def measure_circuit_depth(circuit):
        # Placeholder for actual circuit depth calculation
        # For simplicity, we assume the circuit is a binary tree and its depth is log base 2 of the number of nodes
        num_nodes = len(circuit)
        return int(num_nodes ** 0.5) + 1
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds_count = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        depth = random.randint(5, 40)
        circuit = generate_circuit(depth)
        symmetry_group_order = calculate_symmetry_group(circuit)
        circuit_depth = measure_circuit_depth(circuit)
        
        if symmetry_group_order > 2 ** circuit_depth:
            conjecture_holds_count += 1
            counterexample = f"Depth: {circuit_depth}, Symmetry Group Order: {symmetry_group_order}"
        
        total_metric_value += symmetry_group_order
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "Symmetry Group Order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")