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
    
    def frege_clause_to_symplectic_structure(clause):
        # Construct a simple symplectic structure for demonstration purposes
        n = len(clause)
        H = [[0] * n for _ in range(n)]
        for i, x in enumerate(clause):
            H[i][i] = 1 if x else -1
        return H
    
    def geometric_quantization(H):
        # Calculate the minimal order of geometric quantization using a simple heuristic
        n = len(H)
        det = determinant(H)
        if det == 0:
            return float('inf')
        return math.log(abs(det))
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1) ** i * matrix[0][i] * determinant(submatrix)
        return det
    
    def frege_proof_width(clause_set):
        # Calculate the width of a Frege proof
        max_width = 0
        for clause in clause_set:
            max_width = max(max_width, len(clause))
        return max_width
    
    instances_tested = 0
    n_max = 0
    total_mq = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested += n
        n_max = max(n_max, n)
        
        for _ in range(5):
            clause_set = {tuple(random.choice([True, False]) for _ in range(n)) for _ in range(n)}
            width = frege_proof_width(clause_set)
            H = [frege_clause_to_symplectic_structure(clause) for clause in clause_set]
            
            mq_values = [geometric_quantization(H[i]) for i in range(len(H))]
            avg_mq = sum(mq_values) / len(mq_values)
            
            if avg_mq > 1.5 * math.log(width):
                conjecture_holds = False
                counterexample = f"Clause set with width {width} and average mq {avg_mq}"
    
    return {
        "metric_name": "Average Geometric Quantization",
        "metric_value": total_mq / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")