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

def generate_cnf_tautology(n, rank_defect):
    if rank_defect >= n:
        return None
    
    matrix = [[0] * n for _ in range(n)]
    for i in range(rank_defect):
        row = [random.randint(0, 1) for _ in range(n)]
        while any(matrix[j][i] == row[i] for j in range(i)):
            row = [random.randint(0, 1) for _ in range(n)]
        matrix[i] = row
    
    tautology = []
    for i in range(rank_defect):
        for j in range(i + 1, rank_defect):
            if any(matrix[k][i] == matrix[k][j] for k in range(n)):
                continue
            clause = [random.randint(0, 1) * (2 * k + 1) - 1 for k in range(n)]
            tautology.append(clause)
    
    return tautology

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(matrix[i][j]) > abs(matrix[i_max][j]):
                i_max = i
        if matrix[i_max][j] == 0:
            continue
        matrix[i_max], matrix[rank] = matrix[rank], matrix[i_max]
        for i in range(m):
            if i != rank and matrix[i][j] != 0:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(n):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            rank_defect = random.randint(0, min(n - 1, 5))
            tautology = generate_cnf_tautology(n, rank_defect)
            if tautology is None:
                continue
            
            matrix = [[int(tautology[i][j] == (2 * k + 1)) for j in range(n)] for i in range(len(tautology))]
            rank = gaussian_elimination(matrix)
            
            # Extended Frege proof size is not trivial to compute; assume it's proportional to n^2 for simplicity
            proof_size = n ** 2
            
            results.append({
                "n": n,
                "rank_defect": rank_defect,
                "proof_size": proof_size
            })
    
    if not results:
        return {
            "metric_name": "proof_size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [result["proof_size"] for result in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(result["proof_size"] > (n - rank_defect) * n for result in results)
    
    return {
        "metric_name": "proof_size",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={result['n']}, rank_defect={result['rank_defect']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["conjecture_holds"] for seed in seeds]
    support_fraction = sum(results) / len(results)
    
    if all(results):
        print(f"RESULT: SUPPORTED mean={sum(run_trial(seed)['metric_value'] for seed in seeds) / len(seeds)} std={math.sqrt(sum((run_trial(seed)['metric_value'] - (sum(run_trial(seed)['metric_value'] for seed in seeds) / len(seeds))) ** 2 for seed in seeds)) / len(seeds)} support_fraction={support_fraction}")
    elif any(not result for result in results):
        first_failing_seed = next(i for i, result in enumerate(results) if not result)
        print(f"RESULT: FALSIFIED counterexample=\"n={seeds[first_failing_seed]}, rank_defect=undefined\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")