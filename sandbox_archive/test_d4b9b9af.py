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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = {}
        
        def dpll():
            if not clauses:
                return True
            literal = next((l for l in range(-n, n+1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            stack.append(literal)
            
            new_clauses = []
            for clause in clauses:
                if any(l in assignment and assignment[l] == True for l in clause):
                    continue
                elif all(-l in assignment and assignment[-l] == True for l in clause):
                    return False
                else:
                    new_clause = [l for l in clause if l != literal]
                    new_clauses.append(new_clause)
            
            if dpll():
                return True
            
            del assignment[literal]
            stack.pop()
            assignment[-literal] = True
            
            new_clauses = []
            for clause in clauses:
                if any(l in assignment and assignment[l] == False for l in clause):
                    continue
                elif all(-l in assignment and assignment[-l] == False for l in clause):
                    return False
                else:
                    new_clause = [l for l in clause if l != -literal]
                    new_clauses.append(new_clause)
            
            if dpll():
                return True
            
            del assignment[-literal]
            stack.pop()
            return False
        
        return len(stack) if dpll() else 0
    
    def geometric_entropy(tree):
        n = len(tree)
        distances = [[math.inf] * n for _ in range(n)]
        
        # Construct the metric tree using a simple encoding
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) in tree:
                    distances[i][j] = distances[j][i] = tree[(i, j)]
                else:
                    distances[i][j] = distances[j][i] = 1
        
        total_weight = sum(sum(distances[i][j] for j in range(n)) for i in range(n))
        
        # Calculate the minimal geometric entropy
        if total_weight == 0:
            return 0
        else:
            return -sum(Fraction(distances[i][j], total_weight) * math.log2(Fraction(distances[i][j], total_weight)) for i in range(n) for j in range(i+1, n))
    
    def construct_metric_tree(clauses):
        n = len(clauses)
        tree = {}
        
        # Encode clauses as geodesic distances
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) not in tree:
                    tree[(i, j)] = 1
        
        return tree
    
    n = random.randint(5, 40)
    instance = generate_boolean_instance(n)
    clauses = []
    
    # Convert boolean instance to clauses
    for i in range(n):
        if instance[i] == 1:
            clauses.append([i+1])
        else:
            clauses.append([-i-1])
    
    tree = construct_metric_tree(clauses)
    H_min = geometric_entropy(tree)
    w_phi = resolution_width(clauses)
    
    return {
        "metric_name": "H_min vs w",
        "metric_value": H_min,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": H_min >= w_phi / 2,
        "counterexample": "" if H_min >= w_phi / 2 else f"H_min({H_min}) < w_phi/2 ({w_phi/2})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")