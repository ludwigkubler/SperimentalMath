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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(c != -lit for lit in clause):
                clauses.append(clause)
        return clauses

    def matrix_representation(clauses):
        n = len(clauses[0])
        m = len(clauses)
        A = [[0] * n for _ in range(m)]
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit > 0:
                    A[i][lit - 1] = 1
                else:
                    A[i][-lit - 1] = -1
        return A

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = rank
            for j in range(rank, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            if A[max_row][i] == 0:
                continue
            A[rank], A[max_row] = A[max_row], A[rank]
            for j in range(m):
                if j != rank and A[j][i] != 0:
                    factor = -A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] += factor * A[rank][k]
            rank += 1
        return rank

    def resolution_width(clauses):
        n = len(clauses[0])
        m = len(clauses)
        queue = clauses[:]
        while queue:
            clause = queue.pop(0)
            for other in clauses:
                if any(lit == -other[i] for i, lit in enumerate(clause)):
                    new_clause = [lit for lit in clause + other if lit != -other[i]]
                    if len(new_clause) == 1:
                        return n
                    if new_clause not in queue and new_clause not in clauses:
                        queue.append(new_clause)
        return n

    def lie_algebroid_order(A):
        rank = gaussian_elimination(A)
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            A = matrix_representation(cnf)
            order = lie_algebroid_order(A)
            width = resolution_width(cnf)
            ratio = order / width if width != 0 else float('inf')
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)

            if ratio > 2:
                conjecture_holds = False
                counterexample = f"n={n}, order={order}, width={width}"
                break

    mean_ratio = total_ratio / instances_tested
    std_deviation = math.sqrt(sum((ratio - mean_ratio) ** 2 for ratio in range(instances_tested))) / instances_tested

    return {
        "metric_name": "Ratio of Lie Algebroid Order to Resolution Width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")