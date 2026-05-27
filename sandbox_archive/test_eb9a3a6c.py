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
    
    def generate_tseitin_circuit(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([variables[i], f'y{i}{j}'])
                clauses.append([f'~y{i}{j}', variables[j]])
                clauses.append([f'~y{i}{j}', f'~x{i}'])
                clauses.append([f'y{i}{j}', f'~x{j}'])
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(i + 1, cols):
                matrix[i][j] /= matrix[i][i]
            matrix[i][i] = 1
            for j in range(rows):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_circuit(n)
    num_clauses = len(clauses)
    
    # Construct the incidence matrix
    incidence_matrix = [[0] * (num_clauses + 1) for _ in range(len(variables))]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var.startswith('x'):
                index = int(var[1:])
                incidence_matrix[index][i] = 1
            else:
                index = len(variables) + int(var[2:])
                incidence_matrix[index][i] = -1
    
    rank = gaussian_elimination(incidence_matrix)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= 1.5 * math.log(n, 2)
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank} > {1.5 * math.log(n, 2)}"
    
    return {
        "metric_name": "Brauer Group Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")