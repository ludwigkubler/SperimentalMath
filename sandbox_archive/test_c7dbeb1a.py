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
    
    def generate_random_circuit(n, d):
        if n == 1:
            return ['0'] * (2 ** d - 1)
        else:
            subcircuits = [generate_random_circuit(n // 2, d // 2) for _ in range(4)]
            circuit = []
            for i in range(len(subcircuits[0])):
                circuit.append('(' + ' & '.join(subcircuits[j][i] for j in range(4)) + ')')
            return circuit
    
    def quasi_monte_carlo_points(n):
        points = []
        for i in range(n):
            point = [random.uniform(-1, 1) for _ in range(n)]
            points.append(point)
        return points
    
    def frege_proof_entanglement_complexity(circuit):
        # Placeholder function to simulate entanglement complexity
        return len(circuit) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(1, 10)
            circuit = generate_random_circuit(n, d)
            points = quasi_monte_carlo_points(n)
            entanglement_complexity = frege_proof_entanglement_complexity(circuit)
            results.append({
                "n": n,
                "d": d,
                "entanglement_complexity": entanglement_complexity
            })
    
    if not results:
        return {
            "metric_name": "frege_proof_entanglement_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "frege_proof_entanglement_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instance sizes"
        }
    
    entanglement_complexities = [result["entanglement_complexity"] for result in results]
    mean_entanglement_complexity = sum(entanglement_complexities) / len(entanglement_complexities)
    std_dev_entanglement_complexity = math.sqrt(sum((x - mean_entanglement_complexity) ** 2 for x in entanglement_complexities) / len(entanglement_complexities))
    
    conjecture_holds = all(result["entanglement_complexity"] <= n ** (1/3) * d ** (2/3) for result in results)
    
    return {
        "metric_name": "frege_proof_entanglement_complexity",
        "metric_value": mean_entanglement_complexity,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Entanglement complexity exceeds predicted bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Entanglement complexity exceeds predicted bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No seeds supported the conjecture")