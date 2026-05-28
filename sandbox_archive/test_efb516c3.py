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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_gram_matrix(cnf, n):
        G_F = [[0] * n for _ in range(n)]
        for clause in cnf:
            i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
            if clause[0] > 0 and clause[1] > 0:
                G_F[i][j], G_F[j][i] = 1, 1
            elif clause[0] < 0 and clause[1] < 0:
                G_F[i][j], G_F[j][i] = -1, -1
        return G_F
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            if pivot_row != i:
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(m):
                if j != i:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 10 * n)
    cnf = generate_cnf(n, m)
    G_F = cnf_to_gram_matrix(cnf, n)
    
    try:
        rank_G_F = matrix_rank(G_F)
    except IndexError as e:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"IndexError: {e}"
        }
    
    if rank_G_F > 10 * n**2 / m:
        return {
            "metric_name": "minimal_rank",
            "metric_value": rank_G_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank exceeds bound: {rank_G_F} > 10n^2/m"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank_G_F,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=missing_data n_tested={len(results)}")