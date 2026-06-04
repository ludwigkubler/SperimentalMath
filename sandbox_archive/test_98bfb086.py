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
    
    def generate_circuit(n, m):
        return [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
    
    def monotone_width(circuit):
        n = len(circuit[0])
        width = 0
        for i in range(n):
            if all(row[i] == row[0][i] for row in circuit):
                width += 1
        return width
    
    def automorphism_group(graph):
        n = len(graph)
        nodes = list(range(n))
        perms = []
        
        def is_valid_perm(perm):
            for i in range(n):
                if any(graph[i][j] != graph[perm[i]][perm[j]] for j in range(n)):
                    return False
            return True
        
        def permute(node, perm):
            new_perm = list(perm)
            new_perm[node] = perm[new_perm.index(nodes[node])]
            return new_perm
        
        def backtrack(start, current_perm):
            if start == n:
                perms.append(current_perm[:])
                return
            for node in nodes:
                if node not in current_perm:
                    next_perm = permute(node, current_perm)
                    if is_valid_perm(next_perm):
                        backtrack(start + 1, next_perm)
        
        backtrack(0, [])
        return perms
    
    def min_group_order(perms):
        return len(perms)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_order = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n, n)
            width = monotone_width(circuit)
            graph = [[circuit[i][j] == circuit[0][j] for j in range(n)] for i in range(n)]
            perms = automorphism_group(graph)
            order = min_group_order(perms)
            
            total_instances += 1
            total_order += order
            total_width += width
    
    mean_order = Fraction(total_order, total_instances)
    mean_width = Fraction(total_width, total_instances)
    
    correlation_coefficient = (total_order * total_width - total_instances * mean_order * mean_width) / \
                               ((total_order**2 - total_instances * mean_order**2) * 
                                (total_width**2 - total_instances * mean_width**2))**0.5
    
    conjecture_holds = correlation_coefficient > Fraction(7, 10)
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient} < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in itertools.product(range(5), repeat=3)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")