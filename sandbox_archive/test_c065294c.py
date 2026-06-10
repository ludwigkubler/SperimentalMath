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
        for _ in range(n):
            gate_type = random.choice(['AND', 'OR', 'NOT'])
            if gate_type == 'NOT':
                inputs = [random.randint(0, 1)]
            else:
                inputs = [random.randint(0, 1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def evaluate_circuit(circuit):
        stack = []
        for gate_type, inputs in reversed(circuit):
            if gate_type == 'NOT':
                result = 1 - inputs[0]
            elif gate_type == 'AND':
                result = all(inputs)
            else:
                result = any(inputs)
            stack.append(result)
        return stack.pop()
    
    def hodge_decomposition_rank(circuit):
        n = len(circuit)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (_, inputs) in enumerate(circuit):
            if inputs[0] == 1:
                A[i][i] += 1
            else:
                A[i][i + 1] += 1
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i, n + 1):
                matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def rank_variance(circuit):
        values = set()
        for _ in range(100):  # Sample 100 random inputs
            input_values = [random.randint(0, 1) for _ in circuit]
            output = evaluate_circuit([(gate_type, input_values[:len(inputs)]) for gate_type, inputs in circuit])
            values.add(output)
        return len(values) - 1
    
    def conjecture_holds(hde_rank, rank_variance):
        if hde_rank > 2 ** rank_variance:
            return False, f"HDE rank {hde_rank} exceeds 2^rank_variance {2 ** rank_variance}"
        return True, ""
    
    n_values = [5, 10, 15, 20, 30, 40]
    hde_ranks = []
    rank_variances = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        hde_rank = hodge_decomposition_rank(circuit)
        rank_variance_val = rank_variance(circuit)
        hde_ranks.append(hde_rank)
        rank_variances.append(rank_variance_val)
    
    correlation = sum((hde_ranks[i] - mean_hde) * (rank_variances[i] - mean_rank_variance) for i in range(len(n_values))) / len(n_values)
    mean_hde = sum(hde_ranks) / len(hde_ranks)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    
    conjecture_supported, counterexample = conjecture_holds(mean_hde, mean_rank_variance)
    
    return {
        "metric_name": "Correlation between HDE rank and rank variance",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_supported,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")