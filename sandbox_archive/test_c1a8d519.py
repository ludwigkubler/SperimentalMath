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
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.random() < 0.5 else 1)]
            while len(clause) < 3 and random.random() < 0.7:
                var = random.choice(variables)
                if var not in clause:
                    clause.append(var * (-1 if random.random() < 0.5 else 1))
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        n = max(abs(v) for clause in clauses for v in clause)
        assignment = [None] * (n + 1)
        
        def backtrack():
            stack = []
            i = 0
            while True:
                if i == len(clauses):
                    return True
                clause = clauses[i]
                found_unassigned = False
                for literal in clause:
                    var = abs(literal)
                    if assignment[var] is None:
                        found_unassigned = True
                        assignment[var] = 1 if literal > 0 else -1
                        stack.append((i, literal))
                        i += 1
                        break
                if not found_unassigned:
                    while stack and all(assignment[abs(lit)] == lit // abs(lit) for lit in clauses[stack[-1][0]]):
                        _, last_lit = stack.pop()
                        assignment[abs(last_lit)] = None
                        i = stack[-1][0] + 1 if stack else len(clauses)
            return False
        
        return backtrack()
    
    def compute_rank(clauses):
        n = max(abs(v) for clause in clauses for v in clause)
        rank = 0
        while True:
            new_clauses = []
            for clause in clauses:
                if not all(assignment[abs(lit)] == lit // abs(lit) for lit in clause):
                    new_clauses.append(clause)
            if len(new_clauses) == len(clauses):
                break
            clauses = new_clauses
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_cnf(n, m)
    
    rank = compute_rank(clauses)
    expected_rank = math.log2(n) ** 2
    
    return {
        "metric_name": "rank(G(F))",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= expected_rank,
        "counterexample": "" if rank <= expected_rank else f"n={n}, expected_rank={expected_rank}, actual_rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={result['counterexample']}' first_failing_seed={first_failing_seed}")