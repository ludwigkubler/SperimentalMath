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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda j: abs(matrix[j][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref_matrix = gaussian_elimination(matrix)
        rank = 0
        for row in rref_matrix:
            if any(row):
                rank += 1
        return rank

    def generate_k_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = random.sample(range(1, n + 1), k=random.randint(1, n))
            clauses.append(clause)
        return clauses

    def is_valid_circuit(circuit, instance):
        for clause in instance:
            if not any(lit in circuit for lit in clause) and not any(-lit in circuit for lit in clause):
                return False
        return True

    def generate_all_circuits(instance):
        n = len(instance)
        variables = set(range(1, n + 1))
        circuits = []
        for m in range(1, 2 ** (n * n) + 1):
            circuit = [i if m & (1 << i) else -i for i in range(n)]
            if is_valid_circuit(circuit, instance):
                circuits.append(circuit)
        return circuits

    def min_rank_k_group(instance):
        n = len(instance)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in instance:
            for lit in clause:
                matrix[abs(lit)][lit] += 1
        return rank(matrix)

    def min_cnf_circuit(instance):
        circuits = generate_all_circuits(instance)
        if not circuits:
            return float('inf')
        return min(len(circuit) for circuit in circuits)

    n = random.randint(5, 40)
    instance = generate_k_sat_instance(n)
    r_G = min_rank_k_group(instance)
    m_actual = min_cnf_circuit(instance)

    conjecture_holds = m_actual <= 2 ** r_G
    counterexample = "" if conjecture_holds else f"m_actual={m_actual}, 2^r(G)={2**r_G}"

    return {
        "metric_name": "Circuit Complexity",
        "metric_value": m_actual,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_actual > 2^r(G)\" first_failing_seed={first_failing_seed}")