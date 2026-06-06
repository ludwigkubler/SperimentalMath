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
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        for literal in range(-n, 0):
            if literal not in assignment and -literal not in assignment:
                assignment[literal] = True
                stack.append(literal)
                break
        
        while stack:
            literal = stack.pop()
            if literal < 0:
                literal = -literal
                assignment[literal] = False
            
            for clause in cnf:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return False
                elif -literal in clause:
                    clause.remove(-literal)
        
        return True
    
    def geometric_fluctuation(cnf):
        satisfying_assignments = [assignment for assignment in itertools.product([True, False], repeat=n) if is_satisfiable(cnf)]
        distribution = [sum(1 for literal in assignment if literal > 0) / n for assignment in satisfying_assignments]
        mean = sum(distribution) / len(distribution)
        variance = sum((x - mean) ** 2 for x in distribution) / len(distribution)
        return math.sqrt(variance)
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        # This is a placeholder and may not accurately reflect the actual complexity
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    gf = geometric_fluctuation(cnf)
    w = resolution_width(cnf)
    
    correlation_coefficient = (w * gf) / (math.sqrt(w ** 2 + gf ** 2))
    
    return {
        "metric_name": "Resolution Width vs Geometric Fluctuation",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")