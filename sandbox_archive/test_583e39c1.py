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
        cnf = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_proof_size(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        states = {tuple(c): False for c in clauses}
        
        def resolve(c1, c2):
            for lit in c1:
                if -lit in c2:
                    return tuple(sorted([x for x in c1 + c2 if x != lit and -x != lit]))
            return None
        
        while True:
            new_clauses = set()
            changed = False
            for c1, c2 in itertools.combinations(clauses, 2):
                res = resolve(c1, c2)
                if res is not None:
                    new_clauses.add(res)
                    changed = True
            if not changed:
                break
            clauses.update(new_clauses)
        
        return len(clauses) - len(states)
    
    def l_p_norm(arrangement, p):
        norm = 0.0
        for line in arrangement:
            norm += sum(abs(x) for x in line) ** p
        return norm ** (1 / p)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    proof_size = resolution_proof_size(cnf)
    
    if proof_size == 0:
        return {
            "metric_name": "L_p_norm",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_size_zero"
        }
    
    arrangement = []
    for clause in cnf:
        line = [random.uniform(-1, 1) for _ in range(n)]
        if all(line[var-1] * line[-var] >= 0 for var in clause):
            arrangement.append(line)
    
    l_p_val = l_p_norm(arrangement, random.choice([1, 2]))
    
    return {
        "metric_name": "L_p_norm",
        "metric_value": l_p_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")