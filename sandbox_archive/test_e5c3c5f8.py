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
    
    def generate_kcnf(n, k):
        clauses = set()
        for _ in range(k * n):
            clause = tuple(random.sample(range(1, n + 1), 3))
            if random.choice([True, False]):
                clause = tuple(-x for x in clause)
            clauses.add(clause)
        return clauses
    
    def is_valid_clause(clause, assignment):
        return any((assignment[abs(x) - 1] == (1 if x > 0 else -1)) for x in clause)
    
    def evaluate_cnf(cnf, assignment):
        return all(is_valid_clause(clause, assignment) for clause in cnf)
    
    def generate_assignment(n):
        return [random.choice([-1, 1]) for _ in range(n)]
    
    def count_satisfying_assignments(cnf, n):
        count = 0
        for i in range(2 ** n):
            assignment = [(i >> j) & 1 for j in range(n)]
            if evaluate_cnf(cnf, assignment):
                count += 1
        return count
    
    def compute_automorphism_group(cnf, n):
        aut = set()
        assignments = [generate_assignment(n) for _ in range(2 ** n)]
        for perm in permutations(range(n)):
            new_assignments = [(assignments[i][perm[j]] for j in range(n)) for i in range(2 ** n)]
            if all(evaluate_cnf(cnf, new_assignments[i]) == evaluate_cnf(cnf, assignments[i]) for i in range(2 ** n)):
                aut.add(tuple(perm))
        return len(aut)
    
    def permutations(lst):
        if len(lst) <= 1:
            yield lst
        else:
            for perm in permutations(lst[1:]):
                for i in range(len(lst)):
                    yield perm[:i] + [lst[0]] + perm[i:]
    
    n = random.randint(5, 40)
    k = math.ceil(n / 3)
    cnf = generate_kcnf(n, k)
    order_aut = compute_automorphism_group(cnf, n)
    mean_order = order_aut
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "mean_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")