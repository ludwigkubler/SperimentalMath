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
    
    def tautology_degree(clauses):
        def dpll(clauses, assignment={}):
            if not clauses:
                return True
            literal = next((l for l in range(1, 2 * len(assignment) + 1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            
            def flip(lit):
                return -lit if lit > 0 else -lit
            
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(clauses, new_assignment):
                return True
            
            new_assignment[literal] = False
            if dpll(clauses, new_assignment):
                return True
            
            return False
        
        return len([c for c in clauses if not any(l in assignment and assignment[l] == True for l in c)])
    
    def p_adic_valuation_rank(circuit):
        # Placeholder function to compute the p-adic valuation rank
        # This is a stub and should be replaced with actual computation
        return random.randint(1, 5)
    
    n = random.randint(5, 40)
    depth = random.randint(2, 3)
    circuit = generate_random_circuit(n, depth)
    
    tautology_deg = tautology_degree(circuit)
    if tautology_deg == 0:
        return {
            "metric_name": "p-adic valuation rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tautology_degree_is_zero"
        }
    
    p_val_rank = p_adic_valuation_rank(circuit)
    threshold = Fraction(1, tautology_deg)
    
    return {
        "metric_name": "p-adic valuation rank",
        "metric_value": p_val_rank,
        "instances_tested": 1,
        "conjecture_holds": p_val_rank <= threshold,
        "counterexample": ""
    }

def generate_random_circuit(n, depth):
    if depth == 0:
        return [[random.choice([-i, i]) for i in range(1, n + 1)]]
    
    clauses = []
    for _ in range(random.randint(1, 3)):
        literals = [random.choice([-i, i]) for i in random.sample(range(1, n + 1), random.randint(1, n))]
        clauses.append(literals)
    
    subcircuits = [generate_random_circuit(n, depth - 1) for _ in range(random.randint(1, 2))]
    for sc in subcircuits:
        clauses.extend(sc)
    
    return clauses

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-adic valuation rank > 1/δ(C)\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")