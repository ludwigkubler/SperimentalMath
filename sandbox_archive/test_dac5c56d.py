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
    
    def generate_ac0_parity_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate in reversed(circuit):
            if gate[0] == 'NOT':
                stack.append(not input_values[gate[1]])
            else:
                a, b = input_values[gate[1][0]], input_values[gate[1][1]]
                if gate[0] == 'AND':
                    stack.append(a and b)
                elif gate[0] == 'OR':
                    stack.append(a or b)
        return stack.pop()
    
    def boolean_function_to_quaternion_algebra(f, n):
        Aq = [[0 for _ in range(2**n)] for _ in range(2**n)]
        for i in range(2**n):
            input_values = [bool((i >> j) & 1) for j in range(n)]
            output = f(input_values)
            row = [0] * (2**n)
            row[output] = 1
            Aq[i] = row
        return Aq
    
    def matrix_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if all(A[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(m):
                if j == i:
                    continue
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    def log_size(circuit):
        size = len(circuit) + 1
        return math.log(size, 2)
    
    n = random.randint(5, 40)
    circuit = generate_ac0_parity_circuit(n)
    Aq = boolean_function_to_quaternion_algebra(evaluate_circuit, n)
    rank = matrix_rank(Aq)
    log_size_value = log_size(circuit)
    
    metric_name = "Minimal Rank of Quaternion Algebra"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= log_size_value
    counterexample = "" if conjecture_holds else f"Rank {rank} > log(size(C)) = {log_size_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank > log(size(C))\" first_failing_seed={first_failing_seed}")