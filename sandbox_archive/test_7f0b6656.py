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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            if all(abs(x) <= n for x in clause):
                clauses.append(clause)
        return clauses
    
    def grothendieck_witt_class(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for x in clause:
                if x > 0:
                    A[x][x] += 1
                else:
                    A[-x][-x] -= 1
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n + 1):
                        matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def resolution_width(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        clauses = {tuple(sorted(clause)) for clause in cnf}
        queue = list(clauses)
        while queue:
            clause1 = queue.pop(0)
            for clause2 in clauses:
                if len(set(clause1).intersection(set(clause2))) == 1:
                    new_clause = tuple(sorted([x for x in clause1 + clause2 if x != -x]))
                    if new_clause not in clauses:
                        queue.append(new_clause)
                        clauses.add(new_clause)
        return max(len(clause) for clause in clauses)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    w_f = grothendieck_witt_class(cnf)
    t_star = resolution_width(cnf)
    
    metric_name = "Resolution Proof Width"
    metric_value = t_star
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if 0.9 <= w_f / t_star <= 1.1:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")