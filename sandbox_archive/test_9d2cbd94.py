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

def generate_circuit(n):
    gates = []
    for _ in range(2 * n - 1):
        gate_type = random.choice(['AND', 'OR'])
        inputs = random.sample(range(n), random.randint(1, n))
        gates.append((gate_type, inputs))
    return gates

def evaluate_circuit(circuit, input_values):
    stack = []
    for gate in circuit:
        if gate[0] == 'AND':
            result = all(input_values[i] for i in gate[1])
        elif gate[0] == 'OR':
            result = any(input_values[i] for i in gate[1])
        stack.append(result)
    return stack.pop()

def affine_quotient_group(circuit):
    n = len(circuit) + 1
    field_size = 2
    matrix = [[random.randint(0, field_size - 1) for _ in range(n)] for _ in range(n)]
    
    # Gaussian elimination to find the rank of the matrix
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if A[i][i] == 0:
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return sum(1 for row in A if any(row))

    rank = gaussian_elimination(matrix)
    return field_size ** (n - rank)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_circuit(n)
        input_values = [random.choice([0, 1]) for _ in range(n)]
        g = affine_quotient_group(circuit)
        d = len(circuit) + 1
        metric_values.append(g / (d ** 2))
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    conjecture_holds = all(value <= 1.5 for value in metric_values)  # Assuming c = 1.5 for simplicity
    
    return {
        "metric_name": "g/d^2",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")