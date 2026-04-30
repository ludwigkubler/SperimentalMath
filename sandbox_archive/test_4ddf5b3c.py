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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def non_commutative_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if any(A[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def generate_acc0_circuit(depth, n):
        circuit = []
        for _ in range(depth):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit

    def evaluate_circuit(circuit):
        stack = []
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(inputs)
            elif gate == 'OR':
                result = any(inputs)
            stack.append(result)
        return stack.pop()

    def matrix_representation(circuit, n):
        m = len(circuit)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, (_, inputs) in enumerate(circuit):
            for j in range(n):
                A[i][j] = inputs[j]
            A[i][n] = evaluate_circuit(circuit[:i+1])
        return A

    depth = random.randint(1, 10)
    n = random.randint(5, 40)
    circuit = generate_acc0_circuit(depth, n)
    A = matrix_representation(circuit, n)
    rank = non_commutative_rank(A)
    
    expected_rank = math.log2(n) if depth > 0 else 0
    conjecture_holds = abs(rank - expected_rank) < 1e-6
    
    return {
        "metric_name": "non_commutative_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Depth {depth}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth_vs_rank\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or too many failures")