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
    
    def log_w(w):
        count = 0
        while w > 1:
            w = math.log(w)
            count += 1
        return count
    
    def frobenius_norm(matrix):
        n = len(matrix)
        sum_of_squares = 0
        for i in range(n):
            for j in range(n):
                sum_of_squares += matrix[i][j] ** 2
        return math.sqrt(sum_of_squares)
    
    def xor_and_tree_width(f):
        # Placeholder function to compute XOR-AND tree width
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) ** (1/3)
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 0:
            return [[1]]
        elif n == 1:
            return matrix[0][0]
        
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det
    
    def random_boolean_function(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    n = random.randint(5, 40)
    f = random_boolean_function(n)
    w = xor_and_tree_width(f)
    char_poly = characteristic_polynomial(f)
    matrix = [[char_poly[i][j] for j in range(len(char_poly))] for i in range(len(char_poly))]
    rank = frobenius_norm(matrix)
    
    return {
        "metric_name": "Frobenius Norm Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= w ** (1/3) * log_w(w),
        "counterexample": "" if rank <= w ** (1/3) * log_w(w) else f"Counterexample: n={n}, w={w}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")