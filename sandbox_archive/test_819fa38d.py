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
    
    def generate_monotone_k_clique_circuit(n, k):
        if n < k or k == 0:
            return None
        circuit = []
        for i in range(k):
            for j in range(i + 1, k + 1):
                circuit.append((i, j))
        for i in range(k, n):
            for j in range(1, k + 1):
                if random.choice([True, False]):
                    circuit.append((i, j))
        return circuit
    
    def incidence_structure(circuit):
        structure = {}
        for u, v in circuit:
            if u not in structure:
                structure[u] = set()
            if v not in structure:
                structure[v] = set()
            structure[u].add(v)
            structure[v].add(u)
        return structure
    
    def quasi_crystalline_representation(structure):
        # Placeholder for actual implementation
        return 0  # This should be replaced with a proper implementation
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_monotone_k_clique_circuit(n, k=2)
        if circuit is None:
            continue
        structure = incidence_structure(circuit)
        Q = quasi_crystalline_representation(structure)
        
        if Q == 0:
            continue
        
        expected_order = n**2 * math.log(n)
        order_ratio = Q / expected_order
        
        results.append({
            "n": n,
            "Q": Q,
            "expected_order": expected_order,
            "order_ratio": order_ratio
        })
    
    if not results:
        return {
            "metric_name": "Order Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    metric_values = [result["order_ratio"] for result in results]
    mean_order_ratio = sum(metric_values) / len(metric_values)
    std_deviation = math.sqrt(sum((x - mean_order_ratio)**2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(0.7 <= ratio <= 1.3 for ratio in metric_values)
    counterexample = "" if conjecture_holds else "Order Ratio out of bounds"
    
    return {
        "metric_name": "Order Ratio",
        "metric_value": mean_order_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid circuits generated")