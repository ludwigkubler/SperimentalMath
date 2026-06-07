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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), random.randint(1, n)))
            circuit.append((gate, inputs))
        return circuit
    
    def calculate_entanglement_complexity(circuit):
        complexity = 0
        for gate, inputs in circuit:
            complexity += len(inputs)
        return complexity
    
    def calculate_symplectic_form_degree(circuit):
        n = len(circuit) + 1
        symplectic_matrix = [[0] * n for _ in range(n)]
        
        # Initialize the symplectic matrix based on the circuit
        for i, (gate, inputs) in enumerate(circuit):
            if gate == 'AND':
                for j in inputs:
                    symplectic_matrix[i][j] = 1
            elif gate == 'OR':
                for j in inputs:
                    symplectic_matrix[j][i] = 1
        
        # Compute the rank of the symplectic matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                if matrix[i][i] == 0:
                    for j in range(i + 1, rows):
                        if matrix[j][i] != 0:
                            matrix[i], matrix[j] = matrix[j], matrix[i]
                            break
                    else:
                        continue
                pivot = matrix[i][i]
                for j in range(cols):
                    matrix[i][j] /= pivot
                for j in range(rows):
                    if j == i:
                        continue
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
            return matrix
        
        gaussian_elimination(symplectic_matrix)
        
        rank = 0
        for row in symplectic_matrix:
            if any(row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfd_sum = 0
    entanglement_complexity_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            mfd = calculate_symplectic_form_degree(circuit)
            entanglement_complexity = calculate_entanglement_complexity(circuit)
            
            if mfd > entanglement_complexity:
                return {
                    "metric_name": "mfd vs EntanglementComplexity",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"mfd({n}) > EntanglementComplexity({n})"
                }
            
            mfd_sum += mfd
            entanglement_complexity_sum += entanglement_complexity
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_mfd = mfd_sum / instances_tested
    mean_entanglement_complexity = entanglement_complexity_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mfd * entanglement_complexity for mfd, entanglement_complexity in zip(range(instances_tested), range(instances_tested))) -
                               mean_mfd * instances_tested - 
                               mean_entanglement_complexity * instances_tested) / \
                              math.sqrt((instances_tested * sum(mfd**2 for mfd in range(instances_tested)) - mean_mfd**2) *
                                        (instances_tested * sum(entanglement_complexity**2 for entanglement_complexity in range(instances_tested)) - mean_entanglement_complexity**2))
    
    return {
        "metric_name": "mfd vs EntanglementComplexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mfd(C) > EntanglementComplexity(C)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")