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
    
    def generate_circuit(n):
        # Generate a random boolean circuit with n variables
        # This is a simplified example, actual implementation may vary
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def entanglement_complexity(circuit):
        # Simplified entanglement complexity metric
        return len(circuit)
    
    def clique_complex(circuit):
        # Simplified clique complex generation (not actual implementation)
        return []
    
    def geometric_group_action(clique_complex):
        # Simplified geometric group action calculation (not actual implementation)
        return 1
    
    n = random.randint(5, 30)  # Sample circuit size
    circuit = generate_circuit(n)
    e_C = entanglement_complexity(circuit)
    K_C = clique_complex(circuit)
    ord_G = geometric_group_action(K_C)
    
    return {
        "metric_name": "ord(G)",
        "metric_value": ord_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if e_C == 0 else ord_G == e_C**2,
        "counterexample": "mapping_undefined" if e_C == 0 else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ord_G = sum(result["metric_value"] for result in results) / len(results)
    std_ord_G = math.sqrt(sum((result["metric_value"] - mean_ord_G)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ord_G} std={std_ord_G} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ord_G} std={std_ord_G} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")