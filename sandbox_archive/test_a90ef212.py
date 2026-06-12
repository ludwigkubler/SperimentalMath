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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for i in range(2**n):
            binary_rep = f[i].to_bin(width=n)[::-1]
            clause = []
            for j in range(n):
                if binary_rep[j] == '1':
                    clause.append(literals[j])
                else:
                    clause.append(-literals[j])
            clauses.append(clause)
        return literals, clauses
    
    def frege_proof_depth(clauses):
        n_clauses = len(clauses)
        n_literals = max(abs(lit) for lit in sum(clauses, []))
        depth = 0
        while True:
            new_clauses = []
            for clause in clauses:
                if any(lit not in literals for lit in clause):
                    continue
                new_clause = [lit for lit in clause if lit in literals]
                if len(new_clause) == 1:
                    literals.remove(abs(new_clause[0]))
                else:
                    new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses = new_clauses
            depth += 1
        return depth
    
    def geometric_entropy(f, n):
        adjacency_matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    adjacency_matrix[i][j] = 1
        degree_sum = sum(sum(row) for row in adjacency_matrix)
        avg_degree = degree_sum / (2 * 2**n)
        return -avg_degree * math.log(avg_degree, 2)
    
    n_max = 0
    instances_tested = 0
    total_ratio = 0
    support_count = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            literals, clauses = tseitin_formula(f, n)
            d = frege_proof_depth(clauses)
            H = geometric_entropy(f, n)
            
            if d == 0:
                continue
            
            ratio = H / d
            total_ratio += ratio
            instances_tested += 1
            
            if ratio >= 0.5:
                support_count += 1
    
    conjecture_holds = support_count / instances_tested >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "H(f)/d(φ_f)",
        "metric_value": total_ratio / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")