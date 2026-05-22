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
    
    def schur_representation(poly):
        n = len(poly) - 1
        representation = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == j:
                    representation[i][j] = poly[i]
        return representation
    
    def matrix_multiplication(A, B):
        result = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def find_counterexample(poly):
        min_rank = float('inf')
        max_complexity = 0
        n = len(poly) - 1
        for x in range(2**n):
            representation = schur_representation(evaluate_polynomial(poly, x))
            rank = determinant(representation)
            if rank < min_rank:
                min_rank = rank
            complexity = monotone_circuit_complexity(x, n)
            if complexity > max_complexity:
                max_complexity = complexity
        return min_rank, max_complexity
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i in range(len(poly)):
            result += poly[i] * (x ** i)
        return result
    
    def monotone_circuit_complexity(x, n):
        # Placeholder function; actual implementation needed
        return sum(1 for bit in bin(x)[2:] if bit == '1')
    
    min_rank, max_complexity = find_counterexample([random.random() for _ in range(random.randint(5, 40))])
    conjecture_holds = min_rank >= max_complexity * 0.1  # Placeholder constant
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_over_max_complexity",
        "metric_value": min_rank / max_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 3071) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")