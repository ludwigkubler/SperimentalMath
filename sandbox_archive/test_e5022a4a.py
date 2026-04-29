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
    
    def generate_ac0_circuit(n, size):
        # Generate a random AC⁰ circuit with n inputs and given size
        circuit = []
        for _ in range(size):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs = [random.randint(0, 1) for _ in range(n)]
                circuit.append((gate_type, inputs))
            else:
                inputs = [random.randint(0, 1) for _ in range(n)]
                circuit.append((gate_type, inputs))
        return circuit
    
    def compute_linearly_independent_functions(circuit):
        # Compute the linearly independent functions using Fourier analysis
        n = len(circuit[0][1])
        count = 0
        for i in range(2**n):
            values = [circuit[j] for j in range(len(circuit)) if all(x == y for x, y in zip(bin(i)[2:].zfill(n), circuit[j][1]))]
            if len(values) > count:
                count = len(values)
        return count
    
    def is_linearly_independent(f1, f2):
        # Check if two functions are linearly independent
        n = len(f1[1])
        matrix = []
        for i in range(2**n):
            row = [f1[j] for j in range(len(f1)) if all(x == y for x, y in zip(bin(i)[2:].zfill(n), f1[j][1]))]
            row += [f2[j] for j in range(len(f2)) if all(x == y for x, y in zip(bin(i)[2:].zfill(n), f2[j][1]))]
            matrix.append(row)
        return gaussian_elimination(matrix) == 0
    
    def gaussian_elimination(matrix):
        # Perform Gaussian elimination to check linear independence
        n = len(matrix[0]) // 2
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(2 * n):
                    matrix[j][k] -= factor * matrix[i][k]
        return sum(abs(matrix[i][i]) for i in range(n))
    
    def parity_function(x):
        # Compute the PARITY function
        return sum(x) % 2
    
    n = random.randint(5, 40)
    size = random.randint(1, 10 * n)
    circuit = generate_ac0_circuit(n, size)
    linearly_independent_count = compute_linearly_independent_functions(circuit)
    
    conjecture_holds = linearly_independent_count >= math.log2(size)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "linearly_independent_count",
        "metric_value": linearly_independent_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")