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
    
    def generate_random_circuit(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    def calculate_entanglement_complexity(circuit):
        # Simplified version of entanglement complexity calculation
        return len(circuit)
    
    def calculate_symplectic_form_degree(circuit):
        n = len(circuit[0])
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        # Gaussian elimination to find the rank of the circuit matrix
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(circuit[r][i]))
            if circuit[max_row][i] == 0:
                continue
            circuit[i], circuit[max_row] = circuit[max_row], circuit[i]
            for j in range(n):
                if i != j:
                    factor = Fraction(circuit[j][i], circuit[i][i])
                    for k in range(n):
                        circuit[j][k] -= factor * circuit[i][k]
        
        rank = sum(1 for row in circuit if any(row))
        return n - rank
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfd_values = []
    entanglement_complexity_values = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        mfd = calculate_symplectic_form_degree(circuit)
        entanglement_complexity = calculate_entanglement_complexity(circuit)
        
        if mfd > entanglement_complexity:
            return {
                "metric_name": "Pearson Correlation",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"mfd({n}) > EntanglementComplexity({n})"
            }
        
        mfd_values.append(mfd)
        entanglement_complexity_values.append(entanglement_complexity)
    
    correlation = pearson_correlation(mfd_values, entanglement_complexity_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mfd(C) > EntanglementComplexity(C)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")