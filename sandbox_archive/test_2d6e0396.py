# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([f'~{variables[i-1]}', f'{variables[i]}'])
        return clauses
    
    def resolution_proof_depth(clauses):
        # Simplified DPLL solver
        clauses = set(tuple(c) for c in clauses)
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [lit for lit in clause1 + clause2 if lit not in set(clause1) & set(clause2)]
                        if len(new_clause) == 0:
                            return None
                        new_clauses.append(tuple(sorted(new_clause)))
            if all(len(c) == 1 for c in clauses):
                return max(len(c) for c in clauses)
            clauses.update(set(new_clauses))
    
    def l_function(n):
        # Simplified L-function calculation (logarithmic growth)
        return Fraction(2**n, n)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = tseitin_formula(n)
            depth = resolution_proof_depth(formula)
            if depth is None:
                continue
            instances_tested += 1
            L_n = l_function(n)
            c_k = Fraction(1, n)  # Simplified constant
            if depth < c_k * L_n:
                conjecture_holds = False
                counterexample = f"Tseitin formula with n={n} has D_F < c_k * L(n)"
                break
    
    return {
        "metric_name": "Resolution Proof Depth vs. L-Function",
        "metric_value": instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")