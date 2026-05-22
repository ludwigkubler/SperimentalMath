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
    
    def generate_random_cnf(n, k):
        if n < k or k <= 0:
            return []
        variables = list(range(1, n + 1))
        clauses = set()
        for _ in range(k):
            clause = random.sample(variables, k)
            clauses.add(tuple(sorted(clause)))
        return list(clauses)

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for col in range(cols):
            pivot_row = -1
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for other_row in range(rank, rows):
                factor = -matrix[other_row][col] / matrix[pivot_row][col]
                for j in range(cols):
                    if matrix[pivot_row][j]:
                        matrix[other_row][j] += factor * matrix[pivot_row][j]
        return rank

    def compute_minimal_intersection_rank(cnf):
        n = len(cnf)
        variables = set()
        for clause in cnf:
            variables.update(clause)
        m = len(variables)
        matrix = [[0] * (m + 1) for _ in range(m)]
        for i, var in enumerate(variables):
            for clause in cnf:
                if var in clause:
                    matrix[i][clause.index(var)] = 1
        return gaussian_elimination(matrix)

    def construct_monotone_circuit(cnf):
        n = len(cnf)
        variables = set()
        for clause in cnf:
            variables.update(clause)
        m = len(variables)
        circuit = []
        for var in variables:
            gate = random.choice(['AND', 'OR'])
            inputs = random.sample(list(variables - {var}), random.randint(1, m-2))
            circuit.append((gate, var, inputs))
        return circuit

    def compute_circuit_size(circuit):
        size = 0
        for gate in circuit:
            if gate[0] == 'AND' or gate[0] == 'OR':
                size += len(gate[2])
            else:
                size += 1
        return size

    n_values = [5, 10, 15, 20, 30, 40]
    total_minimal_intersection_rank = 0
    total_circuit_size = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            k = random.randint(1, min(n-1, 5))
            cnf = generate_random_cnf(n, k)
            if not cnf:
                continue
            minimal_intersection_rank = compute_minimal_intersection_rank(cnf)
            circuit = construct_monotone_circuit(cnf)
            circuit_size = compute_circuit_size(circuit)
            total_minimal_intersection_rank += minimal_intersection_rank
            total_circuit_size += circuit_size
            instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "minimal_intersection_rank_to_circuit_depth_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }

    mean_minimal_intersection_rank = total_minimal_intersection_rank / instances_tested
    mean_circuit_size = total_circuit_size / instances_tested

    if mean_minimal_intersection_rank == 0 or mean_circuit_size == 0:
        return {
            "metric_name": "minimal_intersection_rank_to_circuit_depth_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "zero_mean"
        }

    ratio = mean_minimal_intersection_rank / mean_circuit_size
    std_deviation = math.sqrt((sum((x - ratio) ** 2 for x in [mean_minimal_intersection_rank / mean_circuit_size] * instances_tested)) / instances_tested)
    upper_bound = ratio + 2 * std_deviation

    return {
        "metric_name": "minimal_intersection_rank_to_circuit_depth_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": ratio > upper_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")

    total_minimal_intersection_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    total_circuit_size = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)

    mean_minimal_intersection_rank = total_minimal_intersection_rank / instances_tested
    mean_circuit_size = total_circuit_size / instances_tested

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_intersection_rank} std={std_deviation} support_fraction=1.0")
    elif sum(r["conjecture_holds"] for r in results) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_minimal_intersection_rank} std={std_deviation} support_fraction={(sum(r['conjecture_holds'] for r in results) / len(results)):.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"minimal_intersection_rank_to_circuit_depth_ratio\" first_failing_seed={first_failing_seed}")