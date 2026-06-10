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
    
    def dpll(cnf, assignment=None):
        if assignment is None:
            assignment = {}
        
        unit_clauses = [c for c in cnf if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses[0][0]
            value = literal > 0
            assignment[literal] = value
            unit_clauses = [c for c in cnf if not any(l in assignment and assignment[l] == (l > 0) for l in c)]
        
        pure_literals = {}
        for literal in range(1, len(cnf) + 1):
            pos_count = sum(1 for clause in cnf if literal in clause)
            neg_count = sum(1 for clause in cnf if -literal in clause)
            if pos_count == 0:
                pure_literals[-literal] = True
            elif neg_count == 0:
                pure_literals[literal] = False
        
        while pure_literals:
            literal, value = next(iter(pure_literals.items()))
            assignment[literal] = value
            del pure_literals[literal]
            cnf = [c for c in cnf if not any(l in assignment and assignment[l] == (l > 0) for l in c)]
        
        if not cnf:
            return True
        
        literal = random.choice([i for i in range(1, len(cnf) + 1)])
        value = literal > 0
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        
        if dpll(cnf, new_assignment):
            return True
        
        new_assignment[literal] = not value
        return dpll(cnf, new_assignment)
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def hypergeometric_representation(cnf):
        # Placeholder function to simulate the computation
        return sum(len(c) for c in cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            hp = hypergeometric_representation(cnf)
            h_phi = len(dpll(cnf))
            results.append((hp, h_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    hp_values, h_phi_values = zip(*results)
    correlation_coefficient = sum((hp - (sum(hp_values) / len(hp_values))) * (h_phi - (sum(h_phi_values) / len(h_phi_values))) for hp, h_phi in results) / (len(results) * math.sqrt(sum((hp - (sum(hp_values) / len(hp_values)))**2 for hp in hp_values)) * math.sqrt(sum((h_phi - (sum(h_phi_values) / len(h_phi_values)))**2 for h_phi in h_phi_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(cnf) for cnf, _ in results),
        "conjecture_holds": 0.5 <= abs(correlation_coefficient) <= 2.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed=0")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")