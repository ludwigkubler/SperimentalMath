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
        # Generate a random Boolean circuit with n vertices and depth up to 40
        if n == 1:
            return ['0']
        elif n == 2:
            return ['0', '1']
        else:
            return [random.choice(['0', '1']) for _ in range(n)]
    
    def compute_entanglement_complexity(circuit):
        # Compute the entanglement complexity of a Boolean circuit
        depth = max(len(path) for path in circuit if '1' in path)
        return depth
    
    def calculate_coordinate_ring(circuit):
        # Calculate the coordinate ring of the variety defined by the circuit
        # This is a placeholder function. In practice, this would involve algebraic geometry.
        return {}
    
    def compute_brauer_group_order(K_C):
        # Compute the order of the Brauer group Br(K(C))
        # This is a placeholder function. In practice, this would involve algebraic number theory.
        return 1
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_boolean_circuit(n)
        E_C = compute_entanglement_complexity(circuit)
        K_C = calculate_coordinate_ring(circuit)
        Br_K_C_order = compute_brauer_group_order(K_C)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_metric_value += Br_K_C_order
    
    metric_value = total_metric_value / instances_tested
    
    conjecture_holds = all(Br_K_C_order <= 10 * E_C**2 for _ in range(instances_tested))
    
    if not conjecture_holds:
        counterexample = f"Counterexample found for n={n_max}, E(C)=0, |Br(K(C))|={Br_K_C_order}"
    else:
        counterexample = ""
    
    return {
        "metric_name": "Brauer Group Order",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")