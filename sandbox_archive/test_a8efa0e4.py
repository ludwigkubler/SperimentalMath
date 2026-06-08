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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, 2 * n + 1))
        clauses = []
        
        for i in range(1, n + 1):
            clauses.append([variables[2 * i - 2], variables[2 * i - 1]])
            for j in range(i):
                clauses.append([-variables[2 * i - 2], -variables[2 * j]])
                clauses.append([-variables[2 * i - 1], variables[2 * j]])
        
        return clauses, variables
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for x in range(1, p):
            if (x * x) % p == a:
                return True
        return False
    
    def max_quadratic_residues(n):
        primes = [2] + [i for i in range(3, n + 1, 2) if all(i % p != 0 for p in range(3, int(math.sqrt(i)) + 1, 2))]
        residues = set()
        
        for p in primes:
            for a in range(p):
                if is_quadratic_residue(a, p):
                    residues.add((a, p))
        
        return len(residues)
    
    def resolution_width(clauses, variables):
        assignment = {var: False for var in variables}
        
        def dpll(clauses, assignment):
            unit_clauses = [c[0] for c in clauses if len(c) == 1]
            pure_symbols = {}
            
            while True:
                if not unit_clauses and not pure_symbols:
                    return len(assignment)
                
                if unit_clauses:
                    p = unit_clauses.pop()
                    assignment[p] = True
                    new_assignment = {var: assignment[var] for var in variables}
                    new_assignment[-p] = False
                    clauses = [c for c in clauses if not all(var in new_assignment and new_assignment[var] for var in c)]
                else:
                    p = next((k for k, v in pure_symbols.items() if v), None)
                    if p is None:
                        return len(assignment)
                    
                    assignment[p] = True
                    new_assignment = {var: assignment[var] for var in variables}
                    new_assignment[-p] = False
                    clauses = [c for c in clauses if not all(var in new_assignment and new_assignment[var] for var in c)]
        
        return dpll(clauses, assignment)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses, variables = generate_tseitin_formula(n)
    m_qr_pi = max_quadratic_residues(n)
    width = resolution_width(clauses, variables)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= m_qr_pi + 3 and width >= m_qr_pi - 3,
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
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")