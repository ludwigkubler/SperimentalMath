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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
        return variables, clauses
    
    def boolean_lattice(clauses):
        lattice = set()
        for clause in clauses:
            lattice.add(tuple(sorted(clause.split(' | '))))
        return lattice
    
    def min_rank_k_theory(lattice):
        n = len(lattice)
        if n == 0:
            return 0
        rank = 1
        while True:
            found_new_clause = False
            for clause in lattice:
                if all(var not in new_clause for var in clause) and any(var in new_clause for var in clause):
                    new_clause = tuple(sorted(set(new_clause + clause)))
                    lattice.add(new_clause)
                    found_new_clause = True
            if not found_new_clause:
                break
            rank += 1
        return rank
    
    def communication_complexity_rank(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        rank = 1
        while True:
            found_new_clause = False
            for clause in clauses:
                new_clause = tuple(sorted(set(clause + ('~' + var for var in clause))))
                if all(var not in new_clause for var in clause) and any(var in new_clause for var in clause):
                    lattice.add(new_clause)
                    found_new_clause = True
            if not found_new_clause:
                break
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    lattice = boolean_lattice(clauses)
    min_rank_k = min_rank_k_theory(lattice)
    if min_rank_k == 0:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    comm_complexity = communication_complexity_rank(clauses)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(comm_complexity - math.log(min_rank_k)) <= 0.1 * math.log(min_rank_k),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")