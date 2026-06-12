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
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            if gate == 'NOT':
                circuit.append((gate, random.randint(0, n-1)))
            else:
                inputs = sorted(random.sample(range(n), 2))
                circuit.append((gate, *inputs))
        return circuit
    
    def entanglement_complexity(circuit):
        # Simplified heuristic for entanglement complexity
        return len(circuit)
    
    def minimal_index_of_representation(circuit):
        n = len(circuit)
        matrix = [[0] * n for _ in range(n)]
        for gate, *inputs in circuit:
            if gate == 'NOT':
                matrix[inputs[0]][inputs[0]] = 1
            else:
                for i in inputs:
                    matrix[i][i] += 1
        # Simplified heuristic for minimal index
        return sum(1 for row in matrix if any(row))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            entanglement = entanglement_complexity(circuit)
            index = minimal_index_of_representation(circuit)
            metrics.append((entanglement, index))
            instances_tested += 1
    
    if not metrics:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglement_values = [m[0] for m in metrics]
    index_values = [m[1] for m in metrics]
    
    mean_entanglement = sum(entanglement_values) / len(entanglement_values)
    mean_index = sum(index_values) / len(index_values)
    
    if len(set(index_values)) == 1 or len(set(entanglement_values)) == 1:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "saturation"
        }
    
    # Perform linear regression
    n = len(metrics)
    sum_x = sum(x for x, _ in metrics)
    sum_y = sum(y for _, y in metrics)
    sum_xy = sum(x * y for x, y in metrics)
    sum_xx = sum(x ** 2 for x, _ in metrics)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    r_squared = (n * sum_xy - sum_x * sum_y) ** 2 / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
    
    if r_squared < 0.05:
        return {
            "metric_name": "minimal_index",
            "metric_value": slope,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_index",
            "metric_value": slope,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"p-value={1-r_squared}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break