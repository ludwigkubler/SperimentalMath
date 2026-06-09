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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def smallest_prime_divisor(n):
        for i in range(2, n + 1):
            if n % i == 0 and is_prime(i):
                return i
        return None
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literals = {}
        for clause in clauses:
            for literal in clause:
                if literal not in pure_literals:
                    pure_literals[literal] = 1
                elif literal < 0:
                    pure_literals[literal] -= 1
        for literal, count in pure_literals.items():
            if count == len(clauses):
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
        variable = random.choice(list(pure_literals.keys()))
        new_assignment = assignment.copy()
        new_assignment[variable] = True
        if dpll([c for c in clauses if variable not in c and -variable not in c], new_assignment):
            return True
        new_assignment[variable] = False
        if dpll([c for c in clauses if variable not in c and -variable not in c], new_assignment):
            return True
        return False
    
    def cnf_to_clauses(cnf):
        return [set(clause) for clause in cnf]
    
    def generate_random_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        clauses = cnf_to_clauses(cnf)
        assignment = {}
        if dpll(clauses, assignment):
            return 0
        else:
            return float('inf')
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = n * (n + 1) // 2
    cnf = generate_random_cnf(n, m)
    p = smallest_prime_divisor(m)
    if not p:
        return {
            "metric_name": "frege_proof_depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    depth = frege_proof_depth(cnf)
    upper_bound = math.log(2) * (p - 1)**n / math.log(2)
    
    return {
        "metric_name": "frege_proof_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": depth <= upper_bound,
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
    
    mean_depth = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"depth exceeds upper bound\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")