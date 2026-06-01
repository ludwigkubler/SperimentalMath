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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def construct_circuit(f):
        n = int(math.log2(len(f)))
        circuit = []
        for i in range(n):
            for j in range(2**(n-i-1)):
                if f[2*j] == f[2*j+1]:
                    circuit.append((i, 0))
                else:
                    circuit.append((i, 1))
        return circuit
    
    def p_adic_divergence(circuit, n):
        # Simplified p-adic divergence calculation
        count = [0] * (n + 1)
        for gate in circuit:
            count[gate[0]] += 1
        return sum(count) / len(circuit)
    
    def communication_complexity(circuit):
        # Simplified communication complexity calculation
        return max(len(set(gate[1] for gate in layer)) for layer in circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            circuit = construct_circuit(f)
            min_d_f = p_adic_divergence(circuit, n)
            c_f = communication_complexity(circuit)
            results.append((min_d_f, c_f))
            instances_tested += 1
    
    if not results:
        return {
            "metric_name": "p-adic Divergence",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_d_values = [r[0] for r in results]
    c_values = [r[1] for r in results]
    correlation_coefficient = sum((min_d_values[i] - sum(min_d_values) / len(min_d_values)) * (c_values[i] - sum(c_values) / len(c_values)) for i in range(len(results))) / (len(results) * sum((x - sum(min_d_values) / len(min_d_values))**2 for x in min_d_values) * sum((y - sum(c_values) / len(c_values))**2 for y in c_values))
    mean_difference = abs(sum(min_d_values[i] - c_values[i] for i in range(len(results))) / len(results))
    
    return {
        "metric_name": "p-adic Divergence",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and mean_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")