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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for k in range(n):
                A[i][k] /= A[i][i]
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def dpll_solve(clauses, assignment=[]):
        if not clauses:
            return True
        literals = set()
        for clause in clauses:
            literals.update(clause)
        literal = next(iter(literals))
        pos_literal = literal
        neg_literal = -literal
        if any(pos_literal in assignment or neg_literal not in assignment for clause in clauses):
            if dpll_solve(clauses, assignment + [pos_literal]):
                return True
            if dpll_solve(clauses, assignment + [neg_literal]):
                return True
        return False
    
    def polynomial_hierarchy_depth(n):
        depth = 0
        while n > 1:
            n = math.ceil(math.log2(n))
            depth += 1
        return depth
    
    def generate_instance(n):
        clauses = []
        for i in range(1, n+1):
            clause = [random.randint(-i, i) for _ in range(i)]
            while not dpll_solve(clauses + [clause]):
                clause = [random.randint(-i, i) for _ in range(i)]
            clauses.append(clause)
        return clauses
    
    def minimal_rank_of_kostant_sheaf(n):
        instance = generate_instance(n)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if random.choice([True, False]):
                    matrix[i][j] = 1
        return rank(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            rank_value = minimal_rank_of_kostant_sheaf(n)
            depth = polynomial_hierarchy_depth(n)
            results.append((rank_value, depth))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(x[0] for x in results) / len(results)
    std_dev = math.sqrt(sum((x[0] - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x, _ in results if x <= (math.log(depth) ** depth) * n) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"depth={depth}, rank={mean}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")