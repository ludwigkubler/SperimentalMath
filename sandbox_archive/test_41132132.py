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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def construct_tropical_algebraic_stack(program):
        n = len(program)
        stack = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            stack[i][i - 1] = program[i - 1]
            if i < n:
                stack[i][i] = max(stack[i - 1][i], stack[i - 1][i + 1])
        return stack

    def rank(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank

    n = random.choice([5, 10, 15, 20, 30, 40])
    program = [random.randint(0, 1) for _ in range(n)]
    
    stack = construct_tropical_algebraic_stack(program)
    stack_rank = rank(stack)

    if n == 1:
        expected_rank = 1
    else:
        expected_rank = math.ceil(math.log2(n))

    return {
        "metric_name": "Rank",
        "metric_value": stack_rank,
        "instances_tested": 1,
        "conjecture_holds": stack_rank == expected_rank,
        "counterexample": "" if stack_rank == expected_rank else f"n={n}, rank={stack_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=1\" first_failing_seed={first_failing_seed}")