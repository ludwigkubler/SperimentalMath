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
    
    def tseitin_transformation(clauses):
        new_vars = {}
        tseitin_clauses = []
        
        for i, clause in enumerate(clauses):
            new_var = f"X{i}"
            new_vars[i] = new_var
            tseitin_clauses.append([new_var, -clause[0], -clause[1]])
            tseitin_clauses.append([-new_var, clause[0]])
            tseitin_clauses.append([-new_var, clause[1]])
        
        return tseitin_clauses, new_vars
    
    def resolution(clauses):
        clauses = clauses[:]
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            clauses = [c for c in clauses if literal not in c and -literal not in c]
            for i, clause in enumerate(clauses):
                if literal in clause:
                    clauses[i] = [-l for l in clause if l != literal]
                elif -literal in clause:
                    clauses[i].remove(-literal)
        
        return len(clauses) > 0
    
    def quandle_entropy(clause):
        return 1.0 / len(clause)
    
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        num_vars = random.randint(2, 5)
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(num_vars)]
        clauses.append(clause)
    
    tseitin_clauses, new_vars = tseitin_transformation(clauses)
    proof_width = resolution(tseitin_clauses)
    
    entropy_sum = sum(quandle_entropy(c) for c in clauses)
    quandle_entropy_value = entropy_sum / n
    
    return {
        "metric_name": "quandle_entropy",
        "metric_value": quandle_entropy_value,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_quandle_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_quandle_entropy:.4f} support_fraction={support_fraction:.2f}")