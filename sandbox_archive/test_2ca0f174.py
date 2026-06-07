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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(k, n):
        if k > n or n < 2:
            return None
        vertices = list(range(n))
        clique = []
        for _ in range(k):
            v = random.choice(vertices)
            clique.append(v)
            vertices.remove(v)
        return clique

    def matrix_multiplication(A, B):
        m, p = len(A), len(B[0])
        n = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(m)]
        return result

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rref = gaussian_elimination(matrix)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def hodge_index(n):
        # Example Hodge index calculation (simplified)
        return n * (n - 1) // 2

    instances_tested = 0
    total_hodge_index = 0
    total_variance = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            k = random.randint(2, min(n - 1, 6))
            clique = generate_k_clique(k, n)
            if not clique:
                continue
            
            instances_tested += 1
            h_index = hodge_index(n)
            total_hodge_index += h_index
            
            V = [[0] * k for _ in range(k)]
            for i in range(k):
                for j in range(i + 1, k):
                    V[i][j] = V[j][i] = random.randint(1, n)
            
            variance = rank(V)
            total_variance += variance
    
    if instances_tested == 0:
        return {
            "metric_name": "Hodge Index vs Variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_hodge_index = Fraction(total_hodge_index, instances_tested)
    mean_variance = total_variance / instances_tested
    
    correlation_coefficient = (instances_tested * sum(h * v for h, v in zip(mean_hodge_index.numerator, mean_variance.numerator)) -
                               mean_hodge_index.numerator * mean_variance.numerator) / \
                              math.sqrt((instances_tested * sum(h**2 for h in mean_hodge_index.numerator) - mean_hodge_index.numerator**2) *
                                        (instances_tested * sum(v**2 for v in mean_variance.numerator) - mean_variance.numerator**2))
    
    return {
        "metric_name": "Hodge Index vs Variance",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8 and all(correlation_coefficient >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and min(r['metric_value'] for r in results if r['metric_value'] is not None) >= 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")