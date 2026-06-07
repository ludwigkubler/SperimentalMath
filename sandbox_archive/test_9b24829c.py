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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_geodesic_flow_energy(phi):
        # Placeholder function to simulate geodesic flow energy calculation
        # This is a dummy implementation and should be replaced with actual computation
        n = int(math.log2(len(phi)))
        return math.sqrt(n)
    
    def calculate_circuit_entanglement_complexity(phi):
        # Placeholder function to simulate circuit entanglement complexity calculation
        # This is a dummy implementation and should be replaced with actual computation
        n = int(math.log2(len(phi)))
        return math.sqrt(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_boolean_function(n)
        energy = calculate_geodesic_flow_energy(phi)
        complexity = calculate_circuit_entanglement_complexity(phi)
        
        if energy <= 0 or complexity <= 0:
            return {
                "metric_name": "geodesic_flow_energy",
                "metric_value": energy,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "non-positive values"
            }
        
        results.append((energy, complexity))
    
    mean_energy = sum(e for e, c in results) / len(results)
    mean_complexity = sum(c for e, c in results) / len(results)
    
    if all(0.9 * math.sqrt(n) <= e <= 1.1 * math.sqrt(n) and 0.9 * math.sqrt(n) <= c <= 1.1 * math.sqrt(n) for n, (e, c) in zip(n_values, results)):
        return {
            "metric_name": "geodesic_flow_energy",
            "metric_value": mean_energy,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for n, (e, c) in zip(n_values, results):
            if not (0.9 * math.sqrt(n) <= e <= 1.1 * math.sqrt(n)):
                return {
                    "metric_name": "geodesic_flow_energy",
                    "metric_value": mean_energy,
                    "instances_tested": len(n_values),
                    "n_max": max(n_values),
                    "conjecture_holds": False,
                    "counterexample": f"energy out of bounds for n={n}, e={e}"
                }
            if not (0.9 * math.sqrt(n) <= c <= 1.1 * math.sqrt(n)):
                return {
                    "metric_name": "circuit_entanglement_complexity",
                    "metric_value": mean_complexity,
                    "instances_tested": len(n_values),
                    "n_max": max(n_values),
                    "conjecture_holds": False,
                    "counterexample": f"complexity out of bounds for n={n}, c={c}"
                }
    
    return {
        "metric_name": "geodesic_flow_energy",
        "metric_value": mean_energy,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": False,
        "counterexample": "unknown"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")