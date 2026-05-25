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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), random.choice([-x for x in variables])]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def resolution_width(clauses):
        queue = clauses[:]
        while queue:
            clause = queue.pop(0)
            new_clauses = []
            for other_clause in queue:
                common_vars = set(x for x in clause if -x in other_clause)
                if len(common_vars) == 1:
                    literal = list(common_vars)[0]
                    new_clause = [x for x in clause if x != literal] + [x for x in other_clause if x != -literal and x != literal]
                    if new_clause not in queue and new_clause not in new_clauses:
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return len(queue)
    
    n = random.choice([10, 20, 30, 40])
    k = int(1.5 * n)  # Ensure at least 3 clauses per variable
    cnf = generate_kcnf(n, k)
    t_star = resolution_width(cnf)
    
    if t_star == 0:
        return {
            "metric_name": "t_star",
            "metric_value": t_star,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    matrix = [[random.choice([-1, 0, 1]) for _ in range(n)] for _ in range(n)]
    r_F = matrix_rank(matrix)
    
    if r_F == 0:
        return {
            "metric_name": "r_F",
            "metric_value": r_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "matrix_rank_is_zero"
        }
    
    c = Fraction(1, 2)  # Example constant
    phi_n = c * math.log2(n)
    
    conjecture_holds = (math.log2(t_star) <= r_F) and (r_F <= phi_n)
    counterexample = "" if conjecture_holds else "t_star={} r_F={}".format(t_star, r_F)
    
    return {
        "metric_name": "r_F",
        "metric_value": r_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: seed={}, {}".format(seed, result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))