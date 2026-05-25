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
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [left[0] ^ right[0]] + left + right
    
    def noncommutative_polynomial(circuit):
        if len(circuit) == 1:
            return f"x_{circuit[0]}"
        else:
            return f"({noncommutative_polynomial(circuit[:len(circuit)//2])} * {noncommutative_polynomial(circuit[len(circuit)//2:])})"
    
    def minimal_rank(poly):
        # Placeholder for actual computation of minimal rank
        # This is a dummy implementation for testing purposes
        return len(poly.split('*'))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        poly = noncommutative_polynomial(circuit)
        rank = minimal_rank(poly)
        results.append({"n": n, "circuit_size": len(circuit), "rank": rank})
    
    if not results:
        return {
            "metric_name": "rho_f",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rho_circuit = [result["rank"] / result["circuit_size"] for result in results]
    mean_rho = sum(rho_circuit) / len(rho_circuit)
    std_rho = math.sqrt(sum((x - mean_rho) ** 2 for x in rho_circuit) / len(rho_circuit))
    
    return {
        "metric_name": "rho_f",
        "metric_value": mean_rho,
        "instances_tested": len(results),
        "conjecture_holds": False,  # Placeholder
        "counterexample": ""  # Placeholder
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=not_enough_data n_tested=<k>")
    else:
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")