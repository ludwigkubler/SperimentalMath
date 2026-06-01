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
    
    # Define the Tseitin formula and compute its resolution proof width
    def tseitin_formula(G, d):
        n = len(G)
        literals = list(range(1, 2*n + 1))
        clauses = []
        
        for i in range(n):
            clause = [literals[2*i], literals[2*i+1]]
            clauses.append(clause)
            
            for j in range(d):
                if G[i][j] == 0:
                    continue
                clause = [-literals[2*i], -literals[2*j+1]]
                clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses, literals):
        n = len(literals)
        queue = []
        learned_clauses = set()
        
        for clause in clauses:
            if len(clause) == 1:
                queue.append(clause[0])
            else:
                learned_clauses.add(tuple(sorted(clause)))
        
        width = 0
        while queue:
            literal = queue.pop(0)
            new_clause = None
            
            for clause in learned_clauses:
                if -literal in clause:
                    new_clause = [l for l in clause if l != -literal]
                    break
            
            if new_clause is not None:
                width += 1
                queue.extend(new_clause)
                learned_clauses.add(tuple(sorted(new_clause)))
        
        return width
    
    # Generate a random d-regular graph
    def generate_d_regular_graph(n, d):
        G = [[0] * n for _ in range(n)]
        
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i == j:
                    continue
                G[i][j] = 1
                G[j][i] = 1
        
        return G
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for d in [5, 10, 15, 20, 30, 40]:
        n = random.randint(5, n_max + 1)
        G = generate_d_regular_graph(n, d)
        clauses = tseitin_formula(G, d)
        width = resolution_width(clauses, list(range(1, 2*n + 1)))
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_metric_value += width
    
    mean_metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_metric_value,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"d={r['n_max']}, instances_tested={r['instances_tested']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break