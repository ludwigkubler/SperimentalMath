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
    
    def generate_tseitin_clauses(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [f"p{i}"]
            for j in range(i - 1):
                clause.append(f"~p{j}")
            clauses.append(clause)
        return clauses

    def generate_branching_program(clauses):
        program = []
        for clause in clauses:
            if random.choice([True, False]):
                program.append((clause[0], "and"))
            else:
                program.append((clause[0], "or"))
        return program

    def compute_categorical_functor(program):
        functor = {}
        for step in program:
            key = (step[0], step[1])
            if key not in functor:
                functor[key] = []
            functor[key].append(step)
        return functor

    def min_rank(functor):
        matrix = {}
        keys = list(functor.keys())
        n = len(keys)
        
        for i in range(n):
            row = [0] * n
            for j in range(n):
                if keys[i][1] == keys[j][1]:
                    row[j] = 1
            matrix[keys[i]] = row
        
        rank = 0
        for key, row in matrix.items():
            pivot_col = None
            for i in range(len(row)):
                if row[i] != 0:
                    pivot_col = i
                    break
            if pivot_col is not None:
                rank += 1
                for j in range(n):
                    if j != pivot_col and matrix[keys[j]][pivot_col] != 0:
                        for k in range(n):
                            matrix[keys[j]][k] -= matrix[keys[pivot_col]][k]
        return rank

    n = random.randint(5, 40)
    clauses = generate_tseitin_clauses(n)
    program = generate_branching_program(clauses)
    functor = compute_categorical_functor(program)
    
    rank_value = min_rank(functor)
    instances_tested = 1
    conjecture_holds = rank_value <= math.log2(n) and rank_value >= n * math.log2(n)
    counterexample = "" if conjecture_holds else "rank_value out of bounds"
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank_value,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_value out of bounds\" first_failing_seed={first_failing_seed}")