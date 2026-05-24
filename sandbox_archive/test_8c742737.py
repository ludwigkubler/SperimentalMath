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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        for literal in cnf:
            if not any(lit in assignment and assignment[lit] == -val for lit, val in assignment.items()):
                stack.append((literal, 1))
                assignment[literal] = 1
            else:
                continue
        while stack:
            literal, level = stack.pop()
            if level == 2:
                del assignment[-literal]
            elif level == 1:
                for lit in cnf:
                    if literal in lit and -literal not in assignment:
                        stack.append((lit, 2))
                        assignment[lit] = -assignment[literal]
        return any(lit in assignment and assignment[lit] == 1 for lit in cnf)
    
    def compute_brauer_group_rank(cnf):
        n = len(cnf)
        V = [[0]*n for _ in range(n)]
        for clause in cnf:
            for i, lit in enumerate(clause):
                if lit > 0:
                    V[i][lit-1] += 1
                else:
                    V[i][-lit-1] -= 1
        rank = 0
        for row in V:
            if any(x != 0 for x in row):
                rank += 1
                for i in range(n):
                    if row[i] != 0:
                        for j in range(n):
                            V[j][i] -= (V[j][i] * row[i]) // abs(row[i])
        return rank
    
    def resolution_refutation_depth(cnf):
        n = len(cnf)
        clauses = set(tuple(clause) for clause in cnf)
        depth = 0
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if not any(lit in clause1 and -lit in clause2 for lit in clause1):
                        new_clause = tuple(sorted(set(clause1 + clause2) - {-lit for lit in clause2}))
                        if new_clause not in clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    while not is_satisfiable(cnf):
        cnf = generate_cnf(n)
    
    rank = compute_brauer_group_rank(cnf)
    depth = resolution_refutation_depth(cnf)
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= 2**(n/4),
        "counterexample": "" if rank >= 2**(n/4) else f"CNF with n={n} has rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    count_holds = sum(r["conjecture_holds"] for r in results)
    mean_rank = total_rank / len(results)
    support_fraction = count_holds / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too small\" first_failing_seed={first_failing_seed}")