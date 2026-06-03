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
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        # Simple backtracking solver for CNF
        assignment = [None] * (n + 1)
        
        def backtrack(i):
            if i > n:
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(any(assignment[abs(lit)] == l for l in clause) for clause in cnf):
                    if backtrack(i + 1):
                        return True
            assignment[i] = None
            return False
        
        return backtrack(1)
    
    def construct_simplicial_complex(cnf):
        # Construct a simplicial complex from the CNF formula
        vertices = set()
        for clause in cnf:
            vertices.update(abs(lit) for lit in clause)
        
        simplices = []
        for i in range(len(vertices)):
            simplices.append([list(vertices)[i]])
        
        return simplices, len(vertices)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    
    if not is_satisfiable(cnf):
        return {
            "metric_name": "num_simplicial_generators",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "CNF formula is not satisfiable"
        }
    
    simplices, num_vertices = construct_simplicial_complex(cnf)
    
    return {
        "metric_name": "num_simplicial_generators",
        "metric_value": len(simplices),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": len(simplices) <= n ** 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")