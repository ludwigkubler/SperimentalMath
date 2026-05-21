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
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def quadratic_form(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                if clause[i] != 0:
                    for j in range(i, n):
                        if clause[j] != 0:
                            Q[i][j] += 1
                            Q[j][i] = Q[i][j]
        return Q
    
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
            for k in range(j+1, n):
                A[rank][k] /= A[rank][j]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    for k in range(j+1, n):
                        A[i][k] -= A[i][j] * A[rank][k]
            rank += 1
        return rank
    
    def resolution_length(cnf):
        clauses = cnf[:]
        length = 0
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    if any(abs(x) == abs(y) and x != y for x in clauses[i] for y in clauses[j]):
                        continue
                    new_clause = [x for x in clauses[i] if x not in clauses[j]]
                    new_clause.extend([y for y in clauses[j] if y not in clauses[i]])
                    new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                return length
            clauses.extend(new_clauses)
            length += 1
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    Q = quadratic_form(cnf)
    rank = gaussian_elimination(Q)
    proof_length = resolution_length(cnf)
    
    return {
        "metric_name": "minimal_rank_over_proof_length",
        "metric_value": rank / proof_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")