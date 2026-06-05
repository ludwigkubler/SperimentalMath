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

def generate_boolean_circuit(n):
    if n < 1:
        return []
    
    circuit = []
    inputs = [0] * (n - 1)
    for i in range(1, n):
        gate_type = random.choice(['OR', 'AND'])
        if gate_type == 'OR':
            inputs.append(inputs[-1] | inputs[-2])
        else:
            inputs.append(inputs[-1] & inputs[-2])
        circuit.append((gate_type, inputs[-3], inputs[-2]))
    return circuit

def construct_cocomplex(circuit):
    cocomplex = []
    for gate in circuit:
        if gate[0] == 'OR':
            cocomplex.append([gate[1], gate[2]])
        else:
            cocomplex.append([gate[1], gate[2]])
    return cocomplex

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    # Back-substitute to find the solution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = Fraction(matrix[i][-1], matrix[i][i])
        for j in range(i):
            matrix[j][-1] -= matrix[j][i] * solution[i]
    return solution

def minimal_rank(cocomplex):
    n = len(cocomplex)
    identity_matrix = [[Fraction(0, 1)] * n + [Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    augmented_matrix = [row + cocomplex[i] for i, row in enumerate(identity_matrix)]
    rank = gaussian_elimination(augmented_matrix)
    return sum(1 for x in rank if x != Fraction(0, 1))

def circuit_monotone_width(circuit):
    width = 0
    for gate in circuit:
        inputs = [gate[1], gate[2]]
        width = max(width, len(inputs))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested):
            circuit = generate_boolean_circuit(n)
            cocomplex = construct_cocomplex(circuit)
            mrank = minimal_rank(cocomplex)
            w_mon = circuit_monotone_width(circuit)
            
            metric_values.append((mrank, w_mon))
    
    if len(metric_values) < 180:
        return {
            "metric_name": "min_rank_vs_w_mon",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mrank_values, w_mon_values = zip(*metric_values)
    correlation_coefficient = sum((m - mean_mrank) * (w - mean_w_mon) for m, w in zip(mrank_values, w_mon_values)) / len(metric_values)
    mean_abs_diff = sum(abs(m - w) for m, w in zip(mrank_values, w_mon_values)) / len(metric_values)
    
    if correlation_coefficient < 0.8 or mean_abs_diff > 3:
        conjecture_holds = False
        counterexample = "correlation_too_low_or_mean_abs_diff_too_high"
    
    return {
        "metric_name": "min_rank_vs_w_mon",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) >= 8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low_or_mean_abs_diff_too_high\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")