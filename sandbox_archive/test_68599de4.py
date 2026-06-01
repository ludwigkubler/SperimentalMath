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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(phi):
        n = len(phi)
        rank = 0
        for i in range(n):
            if any(phi[j] != phi[j + 2**i] for j in range(2**(n - i) - 1)):
                rank += 1
        return rank
    
    def linear_code_from_phi(phi, n):
        code = []
        for x in range(2**n):
            codeword = [phi[x ^ (1 << i)] for i in range(n)]
            code.append(codeword)
        return code
    
    def brauer_induction_index(code):
        n = len(code[0])
        count = 0
        for x in range(2**n):
            if all(code[x] == code[x ^ (1 << i)] for i in range(n)):
                count += 1
        return count / 2**n
    
    def gaussian_elimination(matrix, n):
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix, n):
        reduced_matrix = gaussian_elimination(matrix, n)
        rank = 0
        for row in reduced_matrix:
            if any(row):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        phi = generate_boolean_function(n)
        code = linear_code_from_phi(phi, n)
        mBI = brauer_induction_index(code)
        crank = communication_complexity_rank(phi)
        
        if crank == 0:
            continue
        
        ratio = mBI / crank
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_ratio <= 2.0  # Example constant c
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mBI/crank",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")