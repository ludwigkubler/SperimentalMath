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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_depth(circuit):
        n = len(circuit)
        depth = 0
        while len(circuit) > 1:
            circuit = [circuit[i] ^ circuit[i + 1] for i in range(len(circuit) // 2)]
            depth += 1
        return depth
    
    def affine_quotient_group_size(n):
        # Simplified encoding of a boolean function as a matrix over GF(2)
        # This is a placeholder and should be replaced with a proper mapping
        return 2**n
    
    n_max = 40
    instances_tested = 30
    total_g = 0
    total_d = 0
    total_G_C_over_d_squared = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        circuit = generate_circuit(n)
        d = frege_proof_depth(circuit)
        G_C = affine_quotient_group_size(n)
        
        if d == 0:
            continue
        
        g = len(bin(G_C).replace("0", "")) - 1
        total_g += g
        total_d += d
        total_G_C_over_d_squared += G_C / (d ** 2)
    
    if instances_tested < 30:
        return {
            "metric_name": "g",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_g = total_g / instances_tested
    mean_G_C_over_d_squared = total_G_C_over_d_squared / instances_tested
    
    if mean_g <= 0 or mean_G_C_over_d_squared <= 0:
        return {
            "metric_name": "g",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "non_positive_values"
        }
    
    correlation_coefficient = (total_g * total_G_C_over_d_squared - instances_tested * mean_g * mean_G_C_over_d_squared) / \
                               math.sqrt((instances_tested * sum(g**2 for g in range(5, 41)) - instances_tested**2 * mean_g**2) *
                                         (instances_tested * sum(G_C_over_d_squared**2 for G_C_over_d_squared in [G_C / d**2 for n in range(5, 41)]) -
                                          instances_tested**2 * mean_G_C_over_d_squared**2))
    
    if correlation_coefficient < 0.8:
        return {
            "metric_name": "g",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"correlation_coefficient={correlation_coefficient}"
        }
    
    if mean_G_C_over_d_squared > 100:  # Placeholder constant, adjust as needed
        return {
            "metric_name": "g",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_G_C_over_d_squared={mean_G_C_over_d_squared}"
        }
    
    return {
        "metric_name": "g",
        "metric_value": mean_g,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_g = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_g)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_g} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")