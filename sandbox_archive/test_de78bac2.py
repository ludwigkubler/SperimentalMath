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
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next((l for l in sorted(assignment.keys(), key=abs) if l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                elif -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return None
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        pos, neg = propagate(lit), propagate(-lit)
        if pos is None or neg is None:
            return False
        return dpll(pos, assignment | {lit: True}) or dpll(neg, assignment | {-lit: True})
    
    def local_coherence(cnf):
        n = len(cnf[0])
        graph = [[0] * n for _ in range(n)]
        for clause in cnf:
            for l1 in clause:
                for l2 in clause:
                    if abs(l1) != abs(l2):
                        graph[abs(l1)-1][abs(l2)-1] += 1
        degree = [sum(row) for row in graph]
        return sum(degree) / (n * n)
    
    def dpll_path_length(cnf):
        stack = [(cnf, {})]
        path_length = 0
        while stack:
            cnf, assignment = stack.pop()
            if not cnf:
                return path_length
            literal = next((l for l in sorted(assignment.keys(), key=abs) if l not in assignment), None)
            pos, neg = propagate(literal), propagate(-literal)
            if pos is None or neg is None:
                continue
            stack.append((pos, assignment | {literal: True}))
            stack.append((neg, assignment | {-literal: True}))
            path_length += 1
        return float('inf')
    
    def propagate(lit):
        new_cnf = []
        for clause in cnf:
            if lit in clause:
                continue
            elif -lit in clause:
                clause.remove(-lit)
                if not clause:
                    return None
            else:
                new_cnf.append(clause)
        return new_cnf
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    local_coherence_value = local_coherence(cnf)
    dpll_path_length_value = dpll_path_length(cnf)
    
    return {
        "metric_name": "LocalCoherence vs DPLLPathLength",
        "metric_value": local_coherence_value * dpll_path_length_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if local_coherence_value == 0 or dpll_path_length_value == float('inf') else True,
        "counterexample": "" if local_coherence_value != 0 and dpll_path_length_value != float('inf') else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        mean_value = sum(result["metric_value"] for result in results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")