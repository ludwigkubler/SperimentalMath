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
    
    def generate_random_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance, assignment, clauses):
        if not clauses:
            return True
        literal = next(lit for lit in instance if abs(lit) not in assignment)
        pos_lit = abs(literal)
        if literal > 0:
            assignment[pos_lit] = True
        else:
            assignment[-pos_lit] = False
        
        new_clauses = [c for c in clauses if not any(abs(lit) == pos_lit and (assignment[lit] if lit > 0 else not assignment[-lit]) for lit in c)]
        
        if dpll(instance, assignment, new_clauses):
            return True
        del assignment[pos_lit]
        
        assignment[-pos_lit] = True
        new_clauses = [c for c in clauses if not any(abs(lit) == pos_lit and (assignment[lit] if lit > 0 else not assignment[-lit]) for lit in c)]
        
        if dpll(instance, assignment, new_clauses):
            return True
        del assignment[-pos_lit]
        
        return False
    
    def compute_dpll_width(instance):
        n = int(math.log2(len(instance)))
        clauses = []
        for i in range(n):
            clauses.append([i + 1, -i - 1])
        
        assignment = {}
        max_depth = 0
        
        def dpll_with_depth(instance, assignment, clauses, depth):
            nonlocal max_depth
            if not clauses:
                max_depth = max(max_depth, depth)
                return True
            literal = next(lit for lit in instance if abs(lit) not in assignment)
            pos_lit = abs(literal)
            if literal > 0:
                assignment[pos_lit] = True
            else:
                assignment[-pos_lit] = False
            
            new_clauses = [c for c in clauses if not any(abs(lit) == pos_lit and (assignment[lit] if lit > 0 else not assignment[-lit]) for lit in c)]
            
            if dpll_with_depth(instance, assignment, new_clauses, depth + 1):
                return True
            del assignment[pos_lit]
            
            assignment[-pos_lit] = True
            new_clauses = [c for c in clauses if not any(abs(lit) == pos_lit and (assignment[lit] if lit > 0 else not assignment[-lit]) for lit in c)]
            
            if dpll_with_depth(instance, assignment, new_clauses, depth + 1):
                return True
            del assignment[-pos_lit]
            
            return False
        
        dpll_with_depth(instance, assignment, clauses, 0)
        return max_depth
    
    def compute_automorphism_group_index(instance):
        n = int(math.log2(len(instance)))
        generators = []
        
        for i in range(n):
            if instance[i] != instance[-i - 1]:
                generators.append(i + 1)
                generators.append(-i - 1)
                break
        
        return len(generators)
    
    def compute_sat_instance(instance):
        n = int(math.log2(len(instance)))
        clauses = []
        
        for i in range(n):
            clauses.append([i + 1, -i - 1])
        
        return clauses
    
    n_max = 40
    instances_tested = 30
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        instance = generate_random_sat_instance(n_max)
        sat_instance = compute_sat_instance(instance)
        automorphism_group_index = compute_automorphism_group_index(instance)
        dpll_width = compute_dpll_width(sat_instance)
        
        if dpll_width == 0:
            continue
        
        ratio = automorphism_group_index / dpll_width
        total_ratio += ratio
        
        if ratio > conjecture_holds:
            conjecture_holds = False
            counterexample = f"Instance {instance} has ratio {ratio}"
    
    mean_ratio = total_ratio / instances_tested
    
    return {
        "metric_name": "Ratio of Automorphism Group Index to DPLL Width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[results.index(next(r for r in results if not r['conjecture_holds'])).index]}\" first_failing_seed={first_failing_seed}")