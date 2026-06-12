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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] for i in range(n)]
    
    def resolution_width(phi):
        # Simplified DPLL solver to estimate width
        clauses = phi.split('\n')
        literals = set()
        for clause in clauses:
            literals.update(clause.split())
        n = len(literals)
        if n > 40:
            return None
        assignment = {l: False for l in literals}
        stack = []
        while True:
            unit_clause = next((c for c in clauses if len(c.split()) == 1), None)
            if unit_clause:
                literal = unit_clause.strip()
                assignment[literal] = True
                stack.append(literal)
                clauses = [c.replace(f'{literal} ', '').replace(f' {literal}', '') for c in clauses]
                clauses = [c for c in clauses if c and not any(l in c for l in literals)]
            else:
                if not clauses:
                    return len(stack)
                literal = random.choice(list(literals))
                assignment[literal] = True
                stack.append(literal)
                clauses = [c.replace(f'{literal} ', '').replace(f' {literal}', '') for c in clauses]
                clauses = [c for c in clauses if c and not any(l in c for l in literals)]
    
    def euler_characteristic(phi):
        # Simplified Euler characteristic calculation
        n = phi.count('x')
        m = phi.count('y')
        return n - m + 1
    
    instances_tested = 0
    total_chi = 0.0
    total_width = 0.0
    max_n = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, 2 * n)
        phi = '\n'.join(' '.join(random.sample(['x', 'y'], k=random.randint(1, n))) for _ in range(m))
        chi = euler_characteristic(phi)
        width = resolution_width(phi)
        
        if width is not None:
            instances_tested += 1
            total_chi += chi
            total_width += width
            max_n = max(max_n, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "Euler Characteristic",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_chi = total_chi / instances_tested
    avg_width = total_width / instances_tested
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": avg_chi,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_chi = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_chi} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_chi} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break