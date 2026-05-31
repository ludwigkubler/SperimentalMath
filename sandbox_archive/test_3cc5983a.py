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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                literals.reverse()
            cnf.append(literals)
        return cnf
    
    def construct_quiver(cnf):
        variables = set(abs(lit) for lit in sum(cnf, []))
        quiver = {var: set() for var in variables}
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    quiver[abs(clause[i])].add(abs(clause[j]))
                    quiver[abs(clause[j])].add(abs(clause[i]))
        return quiver
    
    def is_automorphism(quiver, perm):
        n = len(quiver)
        for i in range(n):
            for j in range(i + 1, n):
                if (quiver[i+1] != {perm[quiver[j+1][k]-1] for k in quiver[j+1]}):
                    return False
        return True
    
    def find_automorphism_group(quiver):
        n = len(quiver)
        automorphisms = set()
        for perm in itertools.permutations(range(1, n + 1)):
            if is_automorphism(quiver, perm):
                automorphisms.add(tuple(sorted(perm)))
        return automorphisms
    
    def dpll_path_length(cnf):
        stack = []
        assignment = [0] * (len(cnf) + 1)
        def solve(i):
            if i == len(cnf) + 1:
                return True
            for val in [True, False]:
                assignment[i] = val
                satisfied = all(any(lit <= 0 and not assignment[abs(lit)] or lit > 0 and assignment[abs(lit)] for lit in clause) for clause in cnf)
                if satisfied:
                    if solve(i + 1):
                        return True
            assignment[i] = 0
            return False
        return len(solve(1))
    
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    quiver = construct_quiver(cnf)
    automorphism_group = find_automorphism_group(quiver)
    dpll_length = dpll_path_length(cnf)
    
    return {
        "metric_name": "Aut(Q)",
        "metric_value": len(automorphism_group),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if len(automorphism_group) >= dpll_length else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_aut_q = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_aut_q} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")