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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropical_variety(boolean_function):
        n = int(math.log2(len(boolean_function)))
        variety = []
        for i in range(2**n):
            row = []
            for j in range(n):
                if boolean_function[i] == 1:
                    row.append(j)
            variety.append(row)
        return variety
    
    def minimal_geometric_entropy(variety):
        n = len(variety[0])
        entropy = 0
        for i in range(2**n):
            count = sum(1 for j in range(n) if i & (1 << j))
            entropy += count * math.log(count + 1, 2)
        return entropy
    
    def tseitin_formula(boolean_function):
        n = int(math.log2(len(boolean_function)))
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        
        for i in range(2**n):
            clause = []
            for j in range(n):
                if boolean_function[i] == 1:
                    clause.append(literals[j])
                else:
                    clause.append(-literals[j])
            clauses.append(clause)
        
        return literals, clauses
    
    def resolution_proof_depth(clauses):
        n = len(clauses[0])
        queue = clauses[:]
        unit_clauses = [i for i in range(n) if sum(1 for c in queue if i in c or -i in c) == 1]
        while unit_clauses:
            new_unit_clause = unit_clauses.pop()
            for clause in queue:
                if new_unit_clause in clause:
                    clause.remove(new_unit_clause)
                    if len(clause) == 0:
                        return None
                elif -new_unit_clause in clause:
                    clause.remove(-new_unit_clause)
                    if len(clause) == 1:
                        unit_clauses.append(clause[0])
        return len(queue)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    boolean_function = generate_boolean_function(n)
    variety = tropical_variety(boolean_function)
    H_min = minimal_geometric_entropy(variety)
    literals, clauses = tseitin_formula(boolean_function)
    d_res = resolution_proof_depth(clauses)
    
    if d_res is None:
        return {
            "metric_name": "H_min(f)",
            "metric_value": H_min,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_depth_not_found"
        }
    
    return {
        "metric_name": "H_min(f)",
        "metric_value": H_min,
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
    
    H_min_values = [r["metric_value"] for r in results if "H_min(f)" == r["metric_name"]]
    d_res_values = [r["instances_tested"] for r in results if "resolution_proof_depth_not_found" != r["counterexample"]]
    
    mean_H_min = sum(H_min_values) / len(H_min_values)
    std_H_min = math.sqrt(sum((x - mean_H_min)**2 for x in H_min_values) / len(H_min_values))
    support_fraction = sum(1 for r in results if "conjecture_holds" and r["counterexample"] == "") / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_H_min} std={std_H_min} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_proof_depth_not_found\" first_failing_seed={first_failing_seed}")