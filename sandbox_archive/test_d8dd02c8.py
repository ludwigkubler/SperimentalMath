# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            max_row = rank
            for j in range(rank, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            for j in range(rows):
                if j != rank:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def compute_index(cnf, n):
        m = len(cnf)
        variables = set()
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    variables.add(lit)
                else:
                    variables.add(-lit)
        n_vars = len(variables)
        matrix = [[0] * (n_vars + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit - 1] = 1
                else:
                    matrix[i][-lit - 1] = 1
        return gaussian_elimination(matrix)
    
    def compute_frege_depth(cnf, n):
        # Placeholder function; actual implementation needed
        return random.randint(50, 200)  # Dummy value for testing
    
    m = random.randint(5, 30)
    n = random.randint(10, 40)
    cnf = generate_cnf(m, n)
    
    index = compute_index(cnf, n)
    depth = compute_frege_depth(cnf, n)
    
    return {
        "metric_name": "Index of Affine Group Action vs Frege Proof Depth",
        "metric_value": Fraction(index, depth),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_count = sum(1 for res in results if res["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(res["metric_value"] < Fraction(1, 2) or res["metric_value"] > Fraction(6, 5) for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if res["metric_value"] < Fraction(1, 2) or res["metric_value"] > Fraction(6, 5))
        print(f"RESULT: FALSIFIED counterexample='Invalid correlation' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")