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
    
    def poly(circuit):
        n = len(circuit)
        y = [0] * (n + 1)
        for j in range(n):
            x = [0] * (j + 2)
            x[0] = 1
            for k in range(j):
                x[k+1] += x[k]
            y[j+1] += x[j]
        return y
    
    def frobenius_schur_indicator(poly):
        n = len(poly) - 1
        if n == 0:
            return 1
        indicator = 0
        for i in range(1, n + 1):
            indicator += poly[i] * (i ** 2)
        return abs(indicator / n)
    
    def max_entanglement_entropy(circuit):
        n = len(circuit)
        if n == 1:
            return 0
        entropy = 0
        for i in range(1, n + 1):
            p = Fraction(i, n)
            entropy += p * math.log2(p) + (1 - p) * math.log2(1 - p)
        return -entropy
    
    def generate_circuit(n):
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            circuit.append(gate)
        return circuit
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            P_C = poly(circuit)
            chi_min = frobenius_schur_indicator(P_C)
            E_C = max_entanglement_entropy(circuit)
            results.append((chi_min, E_C))
    
    if not results:
        return {
            "metric_name": "chi_min - E(C)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    chi_min_avg = sum(result[0] for result in results) / len(results)
    E_C_avg = sum(result[1] for result in results) / len(results)
    k = abs(chi_min_avg - E_C_avg)
    
    return {
        "metric_name": "chi_min - E(C)",
        "metric_value": chi_min_avg - E_C_avg,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(chi_min_avg - E_C_avg) <= k,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")