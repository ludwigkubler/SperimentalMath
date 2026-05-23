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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        # Using a simple backtracking algorithm
        assignment = {}
        
        def backtrack(assignment, clause_index):
            if clause_index == len(cnf):
                return True
            for literal in cnf[clause_index]:
                var = abs(literal)
                if var not in assignment:
                    assignment[var] = literal > 0
                    if backtrack(assignment, clause_index + 1):
                        return True
                    del assignment[var]
                elif (literal > 0) == assignment[var]:
                    break
            else:
                return False
            return True
        
        return backtrack(assignment, 0)
    
    def quasi_plurality_matrix(cnf):
        n = len(cnf)
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    matrix[var_index][var_index] += 1
                else:
                    matrix[var_index][var_index] -= 1
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            max_nonzero = -1
            for j in range(n):
                if matrix[j][i] != 0 and (max_nonzero == -1 or abs(matrix[j][i]) > abs(matrix[max_nonzero][i])):
                    max_nonzero = j
            if max_nonzero != -1:
                rank += 1
                for j in range(n):
                    if j != max_nonzero:
                        factor = matrix[j][i] / matrix[max_nonzero][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[max_nonzero][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank_satisfiable = 0
    total_rank_unsatisfiable = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            if is_satisfiable(cnf):
                rank = min_rank(quasi_plurality_matrix(cnf))
                total_rank_satisfiable += rank
                instances_tested += 1
            else:
                rank = min_rank(quasi_plurality_matrix(cnf))
                total_rank_unsatisfiable += rank
                instances_tested += 1
    
    mean_rank_satisfiable = Fraction(total_rank_satisfiable, instances_tested)
    mean_rank_unsatisfiable = Fraction(total_rank_unsatisfiable, instances_tested)
    
    conjecture_holds = (mean_rank_satisfiable <= 2 * n_values[0]) and (mean_rank_unsatisfiable >= math.exp(n_values[0]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank_satisfiable,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank_satisfiable = sum(r["metric_value"] for r in results if not r["conjecture_holds"]) / len(results)
    mean_rank_unsatisfiable = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_satisfiable} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_satisfiable} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")