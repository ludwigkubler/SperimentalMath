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
            cnf.append(clause)
        return cnf
    
    def construct_quandle(cnf):
        quandle = {}
        for literal in set(abs(lit) for lit in sum(cnf, [])):
            quandle[literal] = {literal}
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    l1, l2 = abs(clause[i]), abs(clause[j])
                    if l1 not in quandle or l2 not in quandle:
                        continue
                    quandle[l1].add(l2)
                    quandle[l2].add(l1)
        return quandle
    
    def count_non_trivial_entanglements(quandle):
        entanglements = 0
        for key, value in quandle.items():
            if len(value) > 1:
                entanglements += len(value) - 1
        return entanglements
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        literal = next((lit for lit in range(1, max(abs(lit) for lit in sum(cnf, [])) + 1) if lit not in assignment and -lit not in assignment), None)
        if literal is None:
            return False
        
        def propagate():
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    clause.remove(-literal)
                if len(clause) == 0:
                    return False
                new_cnf.append(clause)
            return new_cnf
        
        assignment[literal] = True
        new_cnf = propagate()
        if new_cnf is not None and dpll(new_cnf, assignment):
            return True
        
        del assignment[literal]
        assignment[-literal] = True
        new_cnf = propagate()
        if new_cnf is not None and dpll(new_cnf, assignment):
            return True
        
        del assignment[-literal]
        return False
    
    def measure_dpll_search_tree_size(cnf):
        assignment = {}
        stack = [(cnf, assignment)]
        max_depth = 0
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                continue
            literal = next((lit for lit in range(1, max(abs(lit) for lit in sum(cnf, [])) + 1) if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                continue
            
            def propagate():
                new_cnf = []
                for clause in cnf:
                    if literal in clause:
                        continue
                    if -literal in clause:
                        clause.remove(-literal)
                    if len(clause) == 0:
                        return False
                    new_cnf.append(clause)
                return new_cnf
            
            assignment[literal] = True
            new_cnf = propagate()
            if new_cnf is not None:
                stack.append((new_cnf, assignment.copy()))
            
            del assignment[literal]
            assignment[-literal] = True
            new_cnf = propagate()
            if new_cnf is not None:
                stack.append((new_cnf, assignment.copy()))
            
            del assignment[-literal]
        
        return max_depth
    
    n = 10
    m = 20
    cnf = generate_cnf(n, m)
    quandle = construct_quandle(cnf)
    entanglements = count_non_trivial_entanglements(quandle)
    dpll_size = measure_dpll_search_tree_size(cnf)
    
    return {
        "metric_name": "non_trivial_entanglements",
        "metric_value": entanglements,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": entanglements == dpll_size,
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")