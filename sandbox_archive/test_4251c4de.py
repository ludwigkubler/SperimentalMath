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
        return [row[:n-1] for row in A]

    def schur_function_basis(n, k):
        if n == 0 and k == 0:
            return [[1]]
        basis = []
        for i in range(k+1):
            sub_basis = schur_function_basis(n-1, k-i)
            for sb in sub_basis:
                new_row = [0] * (n + k - i)
                new_row[i:i+k+1] = [sb[j] for j in range(k+i+1)]
                basis.append(new_row)
        return basis

    def quotient_hecke_algebra_rank(n, d):
        if d == 0:
            return 1
        basis = schur_function_basis(n, n-1)
        A = [[0] * len(basis) for _ in range(len(basis))]
        for i in range(len(basis)):
            for j in range(len(basis)):
                for k in range(n):
                    A[i][j] += basis[i][k] * basis[j][k]
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def generate_permutation_circuit(n, d):
        circuit = []
        for _ in range(d):
            gate = random.choice(['SWAP', 'NOT'])
            if gate == 'SWAP':
                qubit1 = random.randint(0, n-1)
                qubit2 = random.randint(0, n-1)
                while qubit1 == qubit2:
                    qubit2 = random.randint(0, n-1)
                circuit.append((gate, qubit1, qubit2))
            else:
                qubit = random.randint(0, n-1)
                circuit.append((gate, qubit))
        return circuit

    def compute_circuit_size(circuit):
        size = 0
        for gate in circuit:
            if gate[0] == 'SWAP':
                size += 2
            else:
                size += 1
        return size

    n_values = [5, 10, 15, 20, 30, 40]
    d_values = list(range(1, 7))
    total_ranks = 0
    instances_tested = 0

    for n in n_values:
        for d in d_values:
            for _ in range(5):
                circuit = generate_permutation_circuit(n, d)
                rank = quotient_hecke_algebra_rank(n, d)
                if rank < (n ** 1.5) / d:
                    return {
                        "metric_name": "Minimal Rank",
                        "metric_value": rank,
                        "instances_tested": instances_tested,
                        "conjecture_holds": False,
                        "counterexample": f"n={n}, d={d}, circuit_size={compute_circuit_size(circuit)}, rank={rank}"
                    }
                total_ranks += rank
                instances_tested += 1

    mean_rank = total_ranks / instances_tested
    support_fraction = (instances_tested - sum(1 for _ in range(instances_tested) if quotient_hecke_algebra_rank(n, d) < (n ** 1.5) / d)) / instances_tested

    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 71))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")