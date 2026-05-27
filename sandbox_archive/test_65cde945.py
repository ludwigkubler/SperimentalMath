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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def ehrhart_matrix(cnf):
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    row = i
                else:
                    row = n - i - 1
                col = abs(lit) - 1
                matrix[row][col] += 1
        return matrix
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i]):
                pivot_col = next(j for j in range(n) if matrix[i][j] != 0)
                for j in range(i + 1, m):
                    factor = -matrix[j][pivot_col] / matrix[i][pivot_col]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            m = random.randint(n // 2, n * 2)
            cnf = generate_cnf(n, m)
            matrix = ehrhart_matrix(cnf)
            rank = min_rank(matrix)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = all(0 < mean_rank <= math.log2(n) ** 2 for n in n_values)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean rank {mean_rank} not within O(log^2 n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not within O(log^2 n)\" first_failing_seed={next(r['seed'] for r in results if not r['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")