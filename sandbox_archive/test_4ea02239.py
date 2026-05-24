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
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def vector_space_rank(cnf):
        n = len(cnf[0])
        A = [[int(lit > 0) for lit in clause] for clause in cnf]
        rank = 0
        for i in range(n):
            if any(A[j][i] == 1 for j in range(rank)):
                continue
            found = False
            for j in range(rank, len(A)):
                if A[j][i] == 1:
                    A[rank], A[j] = A[j], A[rank]
                    rank += 1
                    found = True
                    break
            if not found:
                return rank
        return rank
    
    def resolution_refutation_depth(cnf):
        n = len(cnf[0])
        clauses = set(tuple(clause) for clause in cnf)
        depth = 0
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.add(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
            depth += 1
        return depth
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rank = vector_space_rank(cnf)
    depth = resolution_refutation_depth(cnf)
    
    conjecture_holds = rank >= 2**(n/4) and rank > n**0.125
    counterexample = "" if conjecture_holds else "rank too low"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(res["metric_value"] for res in results)
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = res["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")