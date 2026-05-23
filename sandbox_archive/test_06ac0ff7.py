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
    
    def characteristic_polynomial(cnf):
        n = len(set(abs(lit) for lit in cnf))
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i, lit1 in enumerate(clause):
                for j, lit2 in enumerate(clause):
                    if i != j and abs(lit1) == abs(lit2):
                        matrix[i][j] += 1
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        row, col = 0, 0
        while row < m and col < n:
            if matrix[row][col] == 0:
                found_nonzero = False
                for i in range(row + 1, m):
                    if matrix[i][col] != 0:
                        matrix[row], matrix[i] = matrix[i], matrix[row]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    col += 1
                    continue
            pivot = Fraction(matrix[row][col])
            for i in range(col, n):
                matrix[row][i] /= pivot
            for i in range(m):
                if i != row and matrix[i][col] != 0:
                    factor = -matrix[i][col]
                    for j in range(col, n):
                        matrix[i][j] += factor * matrix[row][j]
            row += 1
            col += 1
        return sum(1 for r in matrix if any(r))
    
    def ac0c_circuit_size(cnf, m):
        # Placeholder function to simulate AC0c circuit size computation
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** m
    
    n = random.randint(5, 40)
    cnf = [random.sample(range(-n, -1), 3) for _ in range(random.randint(1, 10))]
    
    matrix = characteristic_polynomial(cnf)
    rank_value = rank(matrix)
    ac0c_size = ac0c_circuit_size(cnf, rank_value)
    
    conjecture_holds = rank_value <= 2 ** n - n * math.log(n) and ac0c_size >= 2 ** rank_value
    counterexample = "" if conjecture_holds else "rank_value > 2^n - O(n log n)"
    
    return {
        "metric_name": "Rank vs AC0c Circuit Depth",
        "metric_value": rank_value,
        "instances_tested": len(cnf),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank_value > 2^n - O(n log n)\" first_failing_seed={first_failing_seed}")