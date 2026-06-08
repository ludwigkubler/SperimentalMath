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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([f"~{variables[i-1]}", variables[i]])
            clauses.append([f"{variables[i-1]}", f"~{variables[i]}"])
        return variables, clauses
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for x in range(1, p):
            if (x * x) % p == a:
                return True
        return False
    
    def max_quadratic_residues_in_ap(n):
        residues = set()
        for i in range(1, n+1):
            for j in range(i, n+1):
                d = math.gcd(j - i, n)
                residues.update([((j - i) * k) % n for k in range(d)])
        return len(residues)
    
    def resolution_width(clauses):
        assignment = {}
        queue = clauses[:]
        while queue:
            clause = queue.pop(0)
            if not any(var[1:] in assignment and (assignment[var[1:]] == var[0] or assignment[var[1:]] == '~' + var[0]) for var in clause):
                unit_clause = next((var for var in clause if var[1:] not in assignment), None)
                if unit_clause:
                    assignment[unit_clause[1:]] = unit_clause[0]
                    queue.extend([c for c in clauses if any(var in c and (assignment[var[1:]] == var[0] or assignment[var[1:]] == '~' + var[0]) for var in c)])
                else:
                    return len(assignment)
        return len(assignment)
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    qr_count = max_quadratic_residues_in_ap(n)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= qr_count + 3 and width >= qr_count - 3,
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
        print("RESULT: INCONCLUSIVE reason=unreachable")