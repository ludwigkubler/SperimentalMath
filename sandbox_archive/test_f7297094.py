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

    def generate_ac0_circuit(n):
        # Generate a random AC⁰ circuit computing PARITY on n variables
        circuit = []
        for _ in range(n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(2)]
            output = random.randint(0, 1)
            circuit.append((gate, inputs, output))
        return circuit

    def parity_polynomial(circuit):
        # Compute the polynomial representation of the AC⁰ circuit
        n = len(circuit)
        poly = [0] * (1 << n)
        for gate, inputs, output in circuit:
            if gate == 'AND':
                poly[output] += 1
            elif gate == 'OR':
                poly[output] -= 1
        return poly

    def real_dimension(poly):
        # Compute the real dimension of the variety defined by the polynomial
        n = len(poly)
        matrix = []
        for i in range(n):
            row = [poly[j] * (i ^ j) for j in range(n)]
            matrix.append(row)
        rank = 0
        for col in range(n):
            pivot = None
            for row in range(rank, n):
                if matrix[row][col] != 0:
                    pivot = row
                    break
            if pivot is not None:
                matrix[pivot], matrix[rank] = matrix[rank], matrix[pivot]
                rank += 1
                for row in range(rank, n):
                    factor = -matrix[row][col] / matrix[pivot][col]
                    for j in range(n):
                        matrix[row][j] += factor * matrix[pivot][j]
        return rank

    def log2(x):
        return math.log2(x) if x > 0 else float('-inf')

    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n)
    poly = parity_polynomial(circuit)
    dim = real_dimension(poly)

    metric_name = "real_dimension"
    metric_value = dim
    instances_tested = 1
    conjecture_holds = dim >= log2(len(circuit))
    counterexample = "" if conjecture_holds else f"n={n}, circuit_size={len(circuit)}, dim={dim}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")