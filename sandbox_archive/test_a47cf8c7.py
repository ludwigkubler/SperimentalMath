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
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            if factor == 0:
                continue
            for j in range(cols):
                matrix[i][j] /= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row[j] != 0 for j in range(cols)):
                rank += 1
        return rank
    
    def frege_proof_length(n, m):
        # Placeholder function; replace with actual Frege proof length calculation
        return n * m
    
    def generate_instance(n, m):
        variables = [random.choice([True, False]) for _ in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(range(n), random.randint(1, n))
            clauses.append(clause)
        matrix = [[0] * (n + 1) for _ in range(m + 1)]
        for i, clause in enumerate(clauses, start=1):
            for var in clause:
                matrix[i][var] = 1
            matrix[i][-1] = -1
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            matrix = generate_instance(n, m)
            rank = min_rank(matrix)
            proof_length = frege_proof_length(n, m)
            results.append((rank, proof_length))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks, proof_lengths = zip(*results)
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (proof_lengths[i] - mean(proof_lengths)) for i in range(len(results))) / len(results) / stdev(ranks) / stdev(proof_lengths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(p <= 50 for p in proof_lengths),
        "counterexample": ""
    }

def mean(data):
    return sum(data) / len(data)

def stdev(data):
    avg = mean(data)
    variance = sum((x - avg) ** 2 for x in data) / len(data)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = mean([r["metric_value"] for r in results])
        std_value = stdev([r["metric_value"] for r in results])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"] and r["counterexample"] == "")
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_acceptance_criterion")