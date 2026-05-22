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
    
    def generate_read_twice_branching_program(n):
        program = []
        for _ in range(n):
            if random.choice([True, False]):
                program.append(random.randint(0, 1))
            else:
                program.append(generate_read_twice_branching_program(n-1))
        return program
    
    def compute_symplectic_form(program):
        n = len(program)
        form = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if isinstance(program[i], list) and isinstance(program[j], list):
                    form[i][j] = sum(x * y for x, y in zip(program[i], program[j]))
                else:
                    form[i][j] = program[i] * program[j]
        return form
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(i, n):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for j in range(n):
                matrix[pivot_row][j], matrix[i][j] = matrix[i][j], matrix[pivot_row][j]
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n = random.randint(5, 40)
    program = generate_read_twice_branching_program(n)
    form = compute_symplectic_form(program)
    rank = min_rank(form)
    expected_rank = log2(n) ** 2
    
    metric_value = rank / expected_rank
    conjecture_holds = abs(metric_value - 1) <= 0.3
    counterexample = "" if conjecture_holds else "minimal_rank < Θ(log^2 size(P))"
    
    return {
        "metric_name": "Rank/Expected Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='minimal_rank < Θ(log^2 size(P))' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")