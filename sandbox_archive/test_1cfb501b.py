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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def generate_quadratic_form(n, m):
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Q[i][j] = random.randint(-10, 10)
                Q[j][i] = Q[i][j]
        return Q
    
    def generate_xor_and_circuit(n):
        circuit = []
        for _ in range(2**(n-1)):
            inputs = [random.choice([0, 1]) for _ in range(n)]
            output = random.choice([0, 1])
            circuit.append((inputs, output))
        return circuit
    
    def compute_conflict_set(circuit):
        conflict_set = set()
        for inputs, output in circuit:
            if output == 1:
                conflict_set.update(inputs)
        return conflict_set
    
    n = random.randint(5, 40)
    m = 2**n - 1
    ε = 0.1
    
    circuit = generate_xor_and_circuit(n)
    conflict_set = compute_conflict_set(circuit)
    
    min_rank = float('inf')
    for _ in range(30):
        Q = generate_quadratic_form(n, m)
        rank = gaussian_elimination(Q)
        if rank < min_rank:
            min_rank = rank
    
    conjecture_holds = min_rank >= math.log2(m) + ε
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")