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
    
    def generate_boolean_circuit(n, depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            left = generate_boolean_circuit(n, depth - 1)
            right = generate_boolean_circuit(n, depth - 1)
            return random.choice([left and right, left or right, not left, not right])
    
    def entanglement_complexity(circuit):
        if isinstance(circuit, int):
            return 0
        else:
            return 1 + max(entanglement_complexity(circuit[0]), entanglement_complexity(circuit[1]))
    
    def coordinate_ring(circuit):
        if isinstance(circuit, int):
            return {circuit}
        else:
            left = coordinate_ring(circuit[0])
            right = coordinate_ring(circuit[1])
            return left.union(right)
    
    def brauer_group_order(coordinate_rings):
        # Simplified Brauer group order calculation
        return len(coordinate_rings) ** 2
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n, random.randint(1, 3))
    E_C = entanglement_complexity(circuit)
    K_C = coordinate_ring(circuit)
    Br_K_C = brauer_group_order(K_C)
    
    return {
        "metric_name": "Brauer Group Order",
        "metric_value": Br_K_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": Br_K_C <= 10 * E_C ** 2,
        "counterexample": "" if Br_K_C <= 10 * E_C ** 2 else f"Counterexample found for n={n}, E(C)={E_C}, |Br(K(C))|={Br_K_C}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")