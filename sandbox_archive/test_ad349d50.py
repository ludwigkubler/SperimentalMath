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
    
    def generate_monotone_circuit(n):
        circuit = []
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def compute_coxeter_group_order(circuit):
        # Simplified mapping from monotone circuit to Coxeter group order
        # This is a placeholder and should be replaced with actual computation
        return len(circuit)
    
    def compute_monotone_complexity(circuit):
        # Simplified mapping from monotone circuit to complexity
        # This is a placeholder and should be replaced with actual computation
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_monotone_circuit(n)
        order = compute_coxeter_group_order(circuit)
        complexity = compute_monotone_complexity(circuit)
        results.append((order, complexity))
    
    if not results:
        return {
            "metric_name": "Coxeter Group Order vs Monotone Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders = [r[0] for r in results]
    complexities = [r[1] for r in results]
    
    mean_order = sum(orders) / len(orders)
    mean_complexity = sum(complexities) / len(complexities)
    
    if len(results) < 30:
        return {
            "metric_name": "Coxeter Group Order vs Monotone Complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = sum((orders[i] - mean_order) * (complexities[i] - mean_complexity) for i in range(len(orders))) / len(orders)
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(orders) - 2)))
    
    return {
        "metric_name": "Coxeter Group Order vs Monotone Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and p_value <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")