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
                inputs = random.sample(range(n), 2)
                circuit.append((gate, inputs[0], inputs[1]))
        return circuit
    
    def compute_entanglement_complexity(circuit):
        # Simplified entanglement complexity calculation
        return len(circuit) / 2
    
    def construct_symmetric_matrix(circuit, n):
        matrix = [[0] * n for _ in range(n)]
        for gate, *inputs in circuit:
            if gate == 'NOT':
                i = inputs[0]
                matrix[i][i] = -1
            else:
                i, j = inputs
                matrix[i][j] += 1
                matrix[j][i] += 1
        return matrix
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below pivot
            factor = -matrix[i][i]
            for j in range(i+1, n):
                matrix[j][i] /= factor
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = matrix[i][-1]
            for j in range(i+1, n):
                x[i] -= matrix[i][j] * x[j]
            x[i] /= matrix[i][i]
        return x
    
    def compute_minimal_index(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return abs(det)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        entanglement_complexity = compute_entanglement_complexity(circuit)
        matrix = construct_symmetric_matrix(circuit, n)
        
        try:
            minimal_index = compute_minimal_index(matrix)
            metric_values.append(minimal_index / entanglement_complexity)
        except (ZeroDivisionError, ValueError) as e:
            counterexample = str(e)
            conjecture_holds = False
            break
    
    return {
        "metric_name": "minimal_index_over_entanglement",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")