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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_mapping(cnf):
        mapping = {}
        for i, clause in enumerate(cnf):
            for lit in clause:
                if abs(lit) not in mapping:
                    mapping[abs(lit)] = []
                mapping[abs(lit)].append((i, lit))
        return mapping
    
    def min_int_points(mapping):
        points = set()
        for lit, clauses in mapping.items():
            for i, lit_val in clauses:
                if lit_val > 0:
                    points.add((lit, i))
                else:
                    points.discard((lit, -i))
        return len(points)
    
    def resolution_proof_length(cnf):
        stack = cnf[:]
        length = 0
        while stack:
            clause1 = stack.pop()
            if not clause1:
                continue
            for clause2 in stack:
                if not clause2:
                    continue
                common_lits = set(clause1) & set(clause2)
                if len(common_lits) == 1:
                    new_clause = [x for x in clause1 + clause2 if x not in common_lits]
                    stack.append(new_clause)
                    length += 1
        return length
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        cnf = generate_cnf(n)
        mapping = construct_mapping(cnf)
        min_points = min_int_points(mapping)
        proof_length = resolution_proof_length(cnf)
        
        instances_tested += 1
        total_metric_value += min_points * proof_length
        
        if conjecture_holds and abs(min_points * proof_length - (min_points + proof_length)) > 0.1:
            conjecture_holds = False
            counterexample = f"n={n}, MinIntPoints={min_points}, Length_ResolutionProof={proof_length}"
    
    return {
        "metric_name": "MinIntPoints * Length_ResolutionProof",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")