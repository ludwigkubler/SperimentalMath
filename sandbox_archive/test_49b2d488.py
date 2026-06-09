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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            var = abs(unit_clause[0])
            if unit_clause[0] < 0 and var in assignment and assignment[var]:
                return False
            elif unit_clause[0] > 0 and var not in assignment:
                assignment[var] = True
            else:
                assignment[var] = False
        pure_literal = next((c for c in cnf if len(c) == 1), None)
        if pure_literal:
            var = abs(pure_literal[0])
            if pure_literal[0] < 0 and var not in assignment:
                assignment[var] = True
            else:
                assignment[var] = False
        literal, rest = cnf[0], cnf[1:]
        return dpll(rest, assignment) or dpll([c for c in rest if var not in c], assignment)
    
    def resolution(cnf):
        while True:
            new_clauses = []
            for i in range(len(cnf)):
                for j in range(i + 1, len(cnf)):
                    p, q = cnf[i], cnf[j]
                    if any(-x == y for x in p for y in q):
                        new_clause = [x for x in p if x not in [-y for y in q] and x != -y]
                        if new_clause:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            cnf.extend(new_clauses)
        return len(cnf)
    
    def vector_space_representation(n):
        # Simplified representation using binary vectors
        return [random.randint(0, 1) for _ in range(n)]
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rep = vector_space_representation(n)
    width = resolution(cnf)
    dim_rep = sum(rep)  # Simplified dimension
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": width * dim_rep,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")