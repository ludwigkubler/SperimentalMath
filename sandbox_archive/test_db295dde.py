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
    
    def generate_3cnf(n, clause_density):
        num_clauses = int(n * clause_density)
        clauses = []
        for _ in range(num_clauses):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            random.shuffle(literals)
            clauses.append(' '.join(map(str, literals)))
        return ' '.join(clauses)

    def ac0_parity_circuit(depth, n):
        if depth == 0:
            return [random.choice([1, -1]) * (i + 1) for i in range(n)]
        else:
            inputs = ac0_parity_circuit(depth - 1, n)
            outputs = []
            for i in range(n):
                output = 1
                for j in range(i, n, 2):
                    output *= inputs[j]
                outputs.append(output)
            return outputs

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            if rank < rows:
                pivot_row = rank
                while matrix[pivot_row][i] == 0:
                    pivot_row += 1
                    if pivot_row == rows:
                        break
                if pivot_row != rank:
                    matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
                for j in range(rank + 1, rows):
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(i, cols):
                        matrix[j][k] += factor * matrix[rank][k]
            rank += 1
        return rank

    def minimal_rank_of_quotient_singularity(n, depth):
        circuit = ac0_parity_circuit(depth, n)
        matrix = [[circuit[i]] for i in range(n)]
        return gaussian_elimination(matrix)

    n_values = [10, 20, 30, 40]
    d_values = [int(c * n**0.5) for c in [0.1, 0.2, 0.3, 0.4]]
    results = []

    for n in n_values:
        for d in d_values:
            if d > n**0.5:
                continue
            clause_density = 0.5
            formula = generate_3cnf(n, clause_density)
            rank = minimal_rank_of_quotient_singularity(n, d)
            results.append({
                "n": n,
                "d": d,
                "rank": rank,
                "expected": d**2 * math.log(n),
                "conjecture_holds": rank > d**2 * math.log(n)
            })

    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Minimal Rank of Quotient Singularity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(result["metric_value"] > 10 for result in results) or support_fraction < 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")