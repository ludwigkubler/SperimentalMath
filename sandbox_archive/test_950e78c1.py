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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n - 1, i - 1, -1):
            if A[i][j]:
                pivot = A[i][j]
                for k in range(m):
                    A[k][j] /= pivot
                for k in range(i + 1, m):
                    factor = A[k][j]
                    for l in range(j, n):
                        A[k][l] -= factor * A[i][l]
    return A

def rank(A):
    rref = gaussian_elimination([row[:] for row in A])
    return sum(1 for row in rref if any(row))

def generate_boolean_circuit(depth, size):
    literals = [f'x{i}' for i in range(size)]
    circuit = []
    for _ in range(depth):
        new_layer = []
        for _ in range(size):
            gate = random.choice(['&', '|'])
            inputs = random.sample(literals, 2)
            new_layer.append((gate, inputs))
        literals.extend([f'x{i}' for i in range(len(circuit), len(circuit) + size)])
        circuit.append(new_layer)
    return circuit

def evaluate_circuit(circuit):
    stack = []
    for layer in circuit:
        for gate, inputs in layer:
            if gate == '&':
                stack.append(stack.pop() & stack.pop())
            elif gate == '|':
                stack.append(stack.pop() | stack.pop())
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(n):
        depth = random.randint(5, 40)
        size = random.randint(10, 20)
        circuit = generate_boolean_circuit(depth, size)
        result = evaluate_circuit(circuit)
        if result == 0 or result == 1:
            instances_tested += 1
            total_rank += rank([[int(x) for x in bin(result)[2:].zfill(size)]])
        else:
            conjecture_holds = False
            counterexample = "Invalid circuit output"

    metric_value = total_rank / instances_tested if instances_tested > 0 else 0
    return {
        "metric_name": "Minimal Rank of Sheaves",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")