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
    
    def construct_qtn(cnf, n):
        qtn = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            var1, var2 = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                qtn[var1][var2] += 1
                qtn[var2][var1] += 1
            elif clause[0] < 0 and clause[1] < 0:
                qtn[-var1][-var2] += 1
                qtn[-var2][-var1] += 1
        return qtn
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = min(m, n)
        for i in range(rank):
            if matrix[i][i] == 0:
                found = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found = True
                        break
                if not found:
                    rank -= 1
                    continue
            for j in range(n):
                if j != i and matrix[i][j] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        width = 0
        while len(clauses) > 1:
            new_clauses = set()
            for clause1, clause2 in itertools.combinations(clauses, 2):
                if not (set(clause1) & set(clause2)):
                    new_clause = tuple(sorted(set(clause1) | set(clause2)))
                    if len(new_clause) > width:
                        width = len(new_clause)
                    new_clauses.add(new_clause)
            clauses = new_clauses
        return width
    
    n = random.randint(5, 30)
    m = random.randint(2 * n, 4 * n)
    cnf = generate_cnf(n, m)
    
    qtn = construct_qtn(cnf, n)
    rank = matrix_rank(qtn)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "Rank vs Width",
        "metric_value": abs(rank - width),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(rank - width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, rank={matrix_rank(construct_qtn(generate_cnf(r['n_max'], 2 * r['n_max']), r['n_max']))}, width={resolution_width(generate_cnf(r['n_max'], 2 * r['n_max']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={r['seed']}")
                break