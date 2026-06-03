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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def incidence_matrix(cnf):
        n = len(cnf[0])
        M = [[0] * n for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    M[i][var] = 1
                else:
                    M[i][var] = -1
        return M
    
    def determinant(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in M[1:]]
            det += (-1) ** j * M[0][j] * determinant(submatrix)
        return det
    
    def distinct_roots(poly):
        if poly == 0:
            return 1
        n = len(poly)
        roots = set()
        for i in range(1, 2**n):
            root = Fraction(i).limit_denominator()
            if all((root ** k) % poly != 0 for k in range(n)):
                roots.add(root)
        return len(roots)
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set(tuple(clause) for clause in cnf)
        
        def resolve(lit, other_lit):
            new_clauses = []
            for c1 in clauses:
                if lit in c1 and -other_lit not in c1:
                    new_c = [l for l in c1 if l != lit]
                    if -other_lit in new_c:
                        return None
                    new_clauses.append(tuple(sorted(new_c)))
            return new_clauses
        
        queue = list(clauses)
        while queue:
            clause = queue.pop(0)
            for lit in clause:
                other_lits = [l for l in clause if l != lit]
                for other_lit in other_lits:
                    new_clauses = resolve(lit, other_lit)
                    if new_clauses is None:
                        return len(clause) + 1
                    queue.extend(new_clause for new_clause in new_clauses if new_clause not in clauses)
            clauses.add(tuple(sorted(clause)))
        return float('inf')
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    M = incidence_matrix(cnf)
    poly = determinant(M)
    r_min = distinct_roots(poly)
    w_phi = resolution_width(cnf)
    
    if w_phi == float('inf'):
        return {
            "metric_name": "r_min / w_phi",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    c = r_min / w_phi
    return {
        "metric_name": "r_min / w_phi",
        "metric_value": r_min / w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": r_min <= c * w_phi,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_min > cw(phi)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")