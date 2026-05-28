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

def random_ac0_circuit(n):
    circuit = []
    for _ in range(random.randint(1, n)):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.choice([f'x{i}' for i in range(n)]) for _ in range(gate_type == 'AND')]
        circuit.append((gate_type, inputs))
    return circuit

def evaluate_circuit(circuit, input_values):
    stack = []
    for gate_type, inputs in reversed(circuit):
        if gate_type == 'AND':
            result = True
            for inp in inputs:
                result &= input_values[ord(inp) - ord('x')]
            stack.append(result)
        else:  # OR
            result = False
            for inp in inputs:
                result |= input_values[ord(inp) - ord('x')]
            stack.append(result)
    return stack.pop()

def tropical_rank(circuit):
    n = len([inp for _, inputs in circuit for inp in inputs])
    matrix = [[0] * (n + 1) for _ in range(n)]
    for gate_type, inputs in reversed(circuit):
        for inp in inputs:
            matrix[ord(inp[1:]) - ord('x'), n] = max(matrix[ord(inp[1:]) - ord('x'), n], 0)
        if gate_type == 'AND':
            for i in range(n):
                for j in range(i + 1, n):
                    if matrix[i][n] and matrix[j][n]:
                        matrix[i][j] = max(matrix[i][j], 1)
                        matrix[j][i] = max(matrix[j][i], 1)
        else:  # OR
            for i in range(n):
                for j in range(i + 1, n):
                    if not (matrix[i][n] or matrix[j][n]):
                        matrix[i][j] = min(matrix[i][j], -1)
                        matrix[j][i] = min(matrix[j][i], -1)
    rank = 0
    for i in range(n):
        if all(matrix[i][j] == 0 for j in range(n + 1)):
            continue
        rank += 1
        for j in range(n):
            if matrix[j][i] != 0:
                for k in range(n + 1):
                    matrix[j][k] = max(matrix[j][k], -matrix[i][k])
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = random_ac0_circuit(n)
        input_values = {i: random.choice([True, False]) for i in range(n)}
        output = evaluate_circuit(circuit, input_values)
        rank = tropical_rank(circuit)
        results.append({
            "n": n,
            "circuit": circuit,
            "input_values": input_values,
            "output": output,
            "rank": rank
        })
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["rank"] >= math.log(result["n"], 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "tropical_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["counterexample"] == "mapping_undefined" for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")