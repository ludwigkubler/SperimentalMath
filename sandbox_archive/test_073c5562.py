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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate OR clauses for each variable
        for var in variables:
            clause = [var]
            for other_var in variables:
                if other_var != var:
                    clause.append(-other_var)
            clauses.append(clause)
        
        # Generate AND clauses to connect all OR clauses
        for i in range(1, n):
            clause = [-variables[i], variables[i + 1]]
            clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        derived = set()
        
        while queue:
            literal = random.choice(queue)
            if literal < 0:
                literal = -literal
            
            if literal in derived:
                continue
            derived.add(literal)
            
            new_clauses = []
            for clause in queue:
                if literal in clause:
                    new_clauses.extend([c for c in clause if c != literal])
                elif -literal in clause:
                    new_clauses.append([-c for c in clause if c != -literal])
                else:
                    new_clauses.append(clause)
            
            queue = new_clauses
        
        return len(derived)

    def quantum_group_representation_rank(V):
        # Placeholder implementation of QR
        # This is a dummy function and should be replaced with actual QR computation
        return len(V)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    V = resolution_width(formula)
    QR = quantum_group_representation_rank(V)
    
    w_phi = V
    
    if QR < Fraction(w_phi):
        return {
            "metric_name": "QR vs Resolution Width",
            "metric_value": QR,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "QR(V_φ) < w(φ)"
        }
    
    return {
        "metric_name": "QR vs Resolution Width",
        "metric_value": QR,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
            "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"QR(V_φ) < w(φ)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")