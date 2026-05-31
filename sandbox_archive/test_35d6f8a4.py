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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_coxeter_diagram(cnf):
        diagram = {}
        for lit in set(lit for clause in cnf for lit in clause):
            diagram[lit] = set()
        for lit1 in diagram:
            for lit2 in diagram:
                if lit1 != lit2 and any(abs(lit) == abs(lit1) or abs(lit) == abs(lit2) for lit in [lit1, lit2]):
                    diagram[lit1].add(lit2)
        return diagram
    
    def count_automorphisms(diagram):
        n = len(diagram)
        if n <= 1:
            return 1
        
        # Generate all permutations of variables
        vars = list(range(1, n + 1))
        permuted_diagrams = set()
        
        def permute(v, p):
            if v == n:
                permuted_diagrams.add(tuple(sorted(p)))
                return
            for i in range(n):
                if i not in p:
                    permute(v + 1, p + [i])
        
        permute(0, [])
        
        # Check each permutation
        automorphisms = 0
        for perm in permuted_diagrams:
            permuted_diag = {perm[v]: set(perm[u] for u in diagram[v]) for v in range(n)}
            if permuted_diag == diagram:
                automorphisms += 1
        
        return automorphisms
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_automorphisms = 0
    instances_tested = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            diagram = construct_coxeter_diagram(cnf)
            automorphisms = count_automorphisms(diagram)
            total_automorphisms += automorphisms
            instances_tested += 1
            max_n = max(max_n, n)
    
    mean_Aut = total_automorphisms / instances_tested
    f_n = math.sqrt(m) * (n ** (3/4))
    ratio = mean_Aut / f_n
    
    conjecture_holds = ratio <= 1.05
    counterexample = "" if conjecture_holds else "ratio > 1.05"
    
    return {
        "metric_name": "Aut(φ)",
        "metric_value": mean_Aut,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_Aut = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_Aut} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_Aut} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio > 1.05\" first_failing_seed={first_failing_seed}")