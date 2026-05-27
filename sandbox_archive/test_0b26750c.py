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
    
    def dpll_depth(clauses, assignment):
        if not clauses:
            return 0
        for clause in clauses:
            unsatisfied = [var for var in clause if var not in assignment and -var not in assignment]
            if not unsatisfied:
                continue
            p_var = random.choice(unsatisfied)
            new_assignment = assignment.copy()
            new_assignment[p_var] = True
            depth_true = dpll_depth([c for c in clauses if p_var not in c], new_assignment) + 1
            new_assignment[p_var] = False
            new_assignment[-p_var] = True
            depth_false = dpll_depth([c for c in clauses if -p_var not in c], new_assignment) + 1
            return max(depth_true, depth_false)
        return float('inf')
    
    def tropicalized_lie_algebra(clauses):
        n = len(set(abs(var) for clause in clauses for var in clause))
        A = [[0] * n for _ in range(n)]
        B = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i, var1 in enumerate(clause):
                for j, var2 in enumerate(clause):
                    if i != j and abs(var1) == abs(var2):
                        A[i][j] += 1
                        B[j][i] += 1
        return A, B
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause.append(-random.choice(variables))
            clauses.append(clause)
        return clauses
    
    def construct_lie_algebra(clauses):
        A, B = tropicalized_lie_algebra(clauses)
        C = [[A[i][j] + B[j][i] for j in range(len(A))] for i in range(len(A))]
        return C
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 3 * n)
    clauses = generate_3cnf(n, m)
    
    depth = dpll_depth(clauses, {})
    lie_algebra = construct_lie_algebra(clauses)
    rank = matrix_rank(lie_algebra)
    
    if rank > math.log(depth):
        return {
            "metric_name": "rank_to_depth_ratio",
            "metric_value": rank / depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} greater than log({depth}) = {math.log(depth)}"
        }
    
    return {
        "metric_name": "rank_to_depth_ratio",
        "metric_value": rank / depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing['counterexample']}\" first_failing_seed={first_failing['seed']}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")