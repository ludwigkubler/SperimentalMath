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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n inputs
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def noncommutative_poly_representation(circuit):
        # Simplified representation using a matrix
        n = len(circuit[0][1])
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for gate, inputs in circuit:
            if gate == 'AND':
                for i in range(2**n):
                    for j in range(2**n):
                        if all(inputs[k] == (i >> k) & 1 and (j >> k) & 1 for k in range(n)):
                            matrix[i][j] += 1
            elif gate == 'OR':
                for i in range(2**n):
                    for j in range(2**n):
                        if any(inputs[k] == (i >> k) & 1 or (j >> k) & 1 for k in range(n)):
                            matrix[i][j] += 1
        return matrix
    
    def entanglement_complexity(circuit):
        # Simplified measure of entanglement complexity
        n = len(circuit[0][1])
        complexity = sum(1 for gate, inputs in circuit if gate == 'AND')
        return complexity
    
    def min_poly_rep_order(matrix):
        # Compute the minimal order of the noncommutative polynomial representation
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if matrix[j][i] != 0), None)
            if pivot is not None:
                rank += 1
                for j in range(n):
                    if j != pivot:
                        factor = Fraction(matrix[j][pivot], matrix[pivot][pivot])
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[pivot][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        matrix = noncommutative_poly_representation(circuit)
        order = min_poly_rep_order(matrix)
        complexity = entanglement_complexity(circuit)
        results.append((order, complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders, complexities = zip(*results)
    mean_order = sum(orders) / len(orders)
    mean_complexity = sum(complexities) / len(complexities)
    covariance = sum((o - mean_order) * (c - mean_complexity) for o, c in results) / len(results)
    variance_order = sum((o - mean_order)**2 for o in orders) / len(orders)
    variance_complexity = sum((c - mean_complexity)**2 for c in complexities) / len(complexities)
    
    if variance_order == 0 or variance_complexity == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_order) * math.sqrt(variance_complexity))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=no_results")
        sys.exit(0)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_corr\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")