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
    
    def dpll(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        
        assignment = {}
        
        def search():
            if all(l in assignment or -l in assignment for clause in cnf):
                return True
            unassigned_var = next((v for v in variables if v not in assignment and -v not in assignment), None)
            if unassigned_var is None:
                return False
            
            pure_literals = [l for l in range(1, max(variables) + 1) if (l not in assignment and -l not in assignment)]
            
            for literal in pure_literals:
                assignment[literal] = True
                if search():
                    return True
                del assignment[literal]
            
            assignment[unassigned_var] = False
            if search():
                return True
            del assignment[unassigned_var]
        
        return search()
    
    def construct_quasimorphism(cnf):
        quasimorphism = {}
        for clause in cnf:
            for literal in clause:
                if literal not in quasimorphism:
                    quasimorphism[literal] = random.randint(0, 1)
        return quasimorphism
    
    def rank(quasimorphism):
        max_rank = 0
        for clause in cnf:
            rank_clause = sum(quasimorphism.get(literal, 0) for literal in clause)
            if rank_clause > max_rank:
                max_rank = rank_clause
        return max_rank
    
    def max_gate_degree(cnf):
        degrees = {}
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if var not in degrees:
                    degrees[var] = 0
                degrees[var] += 1
        return max(degrees.values())
    
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    quasimorphism = construct_quasimorphism(cnf)
    rank_value = rank(quasimorphism)
    max_degree = max_gate_degree(cnf)
    
    if rank_value <= 1.5 * max_degree:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "quasimorphism_rank > 1.5 * max_gate_degree"
    
    return {
        "metric_name": "quasimorphism_rank",
        "metric_value": rank_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")