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
    
    def generate_boolean_circuit(n):
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(random.randint(5, 10))]
    
    def calculate_symplectic_form(circuit):
        n = len(circuit)
        symplectic_form = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if circuit[i][j % 2]:
                    symplectic_form[i][j] += 1
                    symplectic_form[j][i] += 1
        return symplectic_form
    
    def calculate_minimal_symplectic_form_degree(symplectic_form):
        n = len(symplectic_form) - 1
        degree = 0
        for i in range(n):
            for j in range(i + 1, n):
                if symplectic_form[i][j] > 0:
                    degree += 1
        return degree
    
    def calculate_circuit_entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i][j % 2]:
                    complexity += 1
        return complexity
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfd_values = []
    entanglement_complexity_values = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        symplectic_form = calculate_symplectic_form(circuit)
        mfd = calculate_minimal_symplectic_form_degree(symplectic_form)
        entanglement_complexity = calculate_circuit_entanglement_complexity(circuit)
        
        mfd_values.append(mfd)
        entanglement_complexity_values.append(entanglement_complexity)
    
    correlation_coefficient = pearson_correlation_coefficient(mfd_values, entanglement_complexity_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(mfd <= entanglement_complexity for mfd, entanglement_complexity in zip(mfd_values, entanglement_complexity_values)),
        "counterexample": "" if correlation_coefficient >= 0.8 and all(mfd <= entanglement_complexity for mfd, entanglement_complexity in zip(mfd_values, entanglement_complexity_values)) else "correlation_coefficient < 0.8 or mfd > EntanglementComplexity(C)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")