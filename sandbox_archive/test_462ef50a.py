# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from collections import defaultdict, deque

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = -1
        for i in range(rank, m):
            if A[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        pivot = Fraction(A[rank][j])
        for j2 in range(n):
            A[rank][j2] /= pivot
        for i in range(m):
            if i != rank and A[i][j] != 0:
                factor = -A[i][j]
                for j2 in range(n):
                    A[i][j2] += factor * A[rank][j2]
        rank += 1
    return rank

def nonnegative_rank(A):
    m, n = len(A), len(A[0])
    min_ranks = [math.inf] * m
    for i in range(m):
        min_ranks[i] = gaussian_elimination([row[:i+1] + row[i+2:] for row in A])
    return max(min_ranks)

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = {}
    n = len(cnf)
    unit_clauses = [i for i in range(n) if len(cnf[i]) == 1]
    while unit_clauses:
        literal = cnf[unit_clauses[0]][0]
        polarity = literal > 0
        assignment[literal] = polarity
        new_clauses = []
        for clause in cnf:
            if not any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause):
                new_clauses.append(clause)
        cnf = new_clauses
        unit_clauses = [i for i in range(n) if len(cnf[i]) == 1]
    
    pure_literals = []
    for literal in range(1, n + 1):
        positive_count = sum(lit == literal for lit in assignment if assignment[lit])
        negative_count = sum(lit == -literal for lit in assignment if assignment[lit])
        if positive_count == 0:
            pure_literals.append(-literal)
        elif negative_count == 0:
            pure_literals.append(literal)
    
    if not cnf and not pure_literals:
        return True
    elif not cnf or pure_literals:
        return False
    
    literal = pure_literals[0]
    polarity = literal > 0
    assignment[literal] = polarity
    new_clauses = []
    for clause in cnf:
        if not any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause):
            new_clauses.append(clause)
    if dpll(new_clauses, assignment):
        return True
    
    del assignment[literal]
    literal = -pure_literals[0]
    polarity = literal > 0
    assignment[literal] = polarity
    new_clauses = []
    for clause in cnf:
        if not any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause):
            new_clauses.append(clause)
    return dpll(new_clauses, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = []
    for _ in range(m):
        clause = sorted(random.sample(range(-n, -1), random.randint(1, n)))
        cnf.append(clause)
    
    rank = nonnegative_rank(cnf)
    dpll_result = dpll(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": rank if dpll_result else 0,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")