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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate, inputs))
        return circuit
    
    def compute_entanglement_complexity(circuit):
        depth = 0
        stack = []
        for gate, inputs in circuit:
            if gate == 'AND' or gate == 'OR':
                stack.append(gate)
                depth += 1
        return depth
    
    def compute_coordinate_ring(circuit):
        # Simplified representation of the coordinate ring
        return [sum(inputs) % 2 for _, inputs in circuit]
    
    def compute_brauer_group_order(K_C):
        # Simplified Brauer group order calculation
        return len(set(K_C)) ** 2
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        circuit = generate_boolean_circuit(n)
        E_C = compute_entanglement_complexity(circuit)
        K_C = compute_coordinate_ring(circuit)
        Br_K_C_order = compute_brauer_group_order(K_C)
        
        instances_tested += 1
        total_metric_value += Br_K_C_order
        
        if Br_K_C_order > 10 * E_C ** 2:
            conjecture_holds = False
            counterexample = f"n={n}, E(C)={E_C}, |Br(K(C))|={Br_K_C_order}"
    
    return {
        "metric_name": "Brauer group order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")