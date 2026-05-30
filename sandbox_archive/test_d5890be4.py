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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frobenius_norm(cnf):
        n = len(cnf)
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    Q[var][var] += 1
                else:
                    Q[0][var] -= 1
                    Q[var][0] -= 1
        trace = sum(Q[i][i] for i in range(n))
        det = determinant(Q)
        return math.sqrt(trace**2 + det**2)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix)
        return det
    
    def resolution_length(cnf):
        n = len(cnf)
        clauses = set(tuple(clause) for clause in cnf)
        resolvents = []
        
        def resolve(lit, other_lit):
            if lit + other_lit == 0:
                return tuple(sorted([abs(x) for x in set(lit for clause in clauses if lit in clause or -lit in clause)]))
            else:
                return None
        
        while True:
            new_resolvents = []
            for lit1, lit2 in itertools.combinations(clauses, 2):
                resolvent = resolve(lit1[0], lit2[0])
                if resolvent and resolvent not in clauses and resolvent not in new_resolvents:
                    new_resolvents.append(resolvent)
            if not new_resolvents:
                break
            resolvents.extend(new_resolvents)
            clauses.update(new_resolvents)
        
        return len(resolvents)
    
    n = random.randint(5, 40)
    m = random.randint(n // 2, n)
    cnf = generate_cnf(n, m)
    
    Q_norm = frobenius_norm(cnf)
    t_star = resolution_length(cnf)
    
    if Q_norm == 0 or t_star == 0:
        return {
            "metric_name": "log(Q(φ)^2/n) vs log(t*(φ))",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Frobenius norm or resolution length is zero"
        }
    
    metric_value = math.log(Q_norm**2 / n)
    log_t_star = math.log(t_star)
    
    return {
        "metric_name": "log(Q(φ)^2/n) vs log(t*(φ))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(metric_value - log_t_star) < 0.5,  # Arbitrary threshold for correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.4f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold\" first_failing_seed={first_failing_seed + 1}")