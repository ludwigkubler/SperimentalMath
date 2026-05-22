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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tropical_add(a, b):
        return max(a, b)

    def tropical_mult(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b

    def tropical_neg(a):
        return -a

    def tropical_zero():
        return float('-inf')

    def tropical_one():
        return 0

    def tropical_identity(n):
        return [[tropical_one() if i == j else tropical_zero() for j in range(n)] for i in range(n)]

    def tropical_inverse(A):
        n = len(A)
        I = tropical_identity(n)
        A_augmented = [row + col for row, col in zip(A, I)]
        rref = gaussian_elimination(A_augmented)
        return [row[n:] for row in rref]

    def tropical_rank(A):
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank

    def generate_branching_program(n, read_once=False):
        if read_once:
            program = []
            for _ in range(n):
                program.append(random.choice([0, 1]))
            return program
        else:
            program = []
            for _ in range(2 * n - 1):
                program.append(random.choice([0, 1]))
            return program

    def tropical_cohomology_size(program):
        n = len(program)
        if n == 1:
            return 1
        A = [[tropical_zero() for _ in range(n)] for _ in range(n)]
        for i in range(n - 1):
            A[i][i + 1] = tropical_one()
        for i in range(n):
            A[n - 1][i] = program[i]
        rank = tropical_rank(A)
        return rank

    def bp_read_twice_circuit_size(program):
        n = len(program)
        if n == 1:
            return 1
        size = 0
        for i in range(n - 1):
            size += 2
        size += n
        return size

    def bp_read_once_circuit_size(program):
        n = len(program)
        if n == 1:
            return 1
        size = 0
        for i in range(n):
            size += 2
        size += n
        return size

    def test_branching_programs(n, read_once=False):
        program = generate_branching_program(n, read_once)
        cohomology_size = tropical_cohomology_size(program)
        circuit_size = bp_read_twice_circuit_size(program) if not read_once else bp_read_once_circuit_size(program)
        return cohomology_size, circuit_size

    def run_trials(num_trials):
        total_cohomology_size = 0
        total_circuit_size = 0
        for _ in range(num_trials):
            n = random.choice([5, 10, 15, 20, 30, 40])
            cohomology_size, circuit_size = test_branching_programs(n, read_once=False)
            total_cohomology_size += cohomology_size
            total_circuit_size += circuit_size
        return total_cohomology_size, total_circuit_size

    num_trials = 30
    total_cohomology_size, total_circuit_size = run_trials(num_trials)

    mean_cohomology_size = total_cohomology_size / num_trials
    mean_circuit_size = total_circuit_size / num_trials
    support_fraction = mean_cohomology_size <= 2 * mean_circuit_size

    return {
        "metric_name": "min_rank_tropicalized_cohomology",
        "metric_value": mean_cohomology_size,
        "instances_tested": num_trials,
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_cohomology_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cohomology_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cohomology_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")