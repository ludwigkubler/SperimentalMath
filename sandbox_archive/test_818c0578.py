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
        clauses = []
        for _ in range(2**n):  # Generate a random CNF formula with n variables and 2^n clauses
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def diophantine_representation(clauses):
        equations = set()
        for clause in clauses:
            equation = []
            for var in clause:
                if var > 0:
                    equation.append(f"x{var} + ")
                else:
                    equation.append(f"-x{-var} + ")
            equation[-1] = equation[-1][:-3]
            equations.add(equation)
        return equations
    
    def dpll_proof_tree_width(clauses):
        # Simplified DPLL algorithm to estimate proof tree width
        if not clauses:
            return 0
        var = random.choice([abs(c) for c in set(sum(clauses, []))])
        pos_clauses = [c for c in clauses if var in c]
        neg_clauses = [c for c in clauses if -var in c]
        return max(dpll_proof_tree_width(pos_clauses), dpll_proof_tree_width(neg_clauses)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_equations = 0
        max_equations = 0
        
        while instances_tested < 30:
            clauses = generate_random_sat_instance(n)
            equations = diophantine_representation(clauses)
            proof_tree_width = dpll_proof_tree_width(clauses)
            
            if len(equations) > max_equations:
                max_equations = len(equations)
            
            total_equations += len(equations)
            instances_tested += 1
        
        results.append({
            "n": n,
            "mean_equations": total_equations / instances_tested,
            "max_equations": max_equations
        })
    
    mean_equations = sum(r["mean_equations"] for r in results) / len(results)
    max_equations = max(r["max_equations"] for r in results)
    
    conjecture_holds = all(r["mean_equations"] <= math.sqrt(r["n"]) for r in results) and max_equations <= 10
    counterexample = f"Mean equations: {mean_equations}, Max equations: {max_equations}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Number of Diophantine Equations",
        "metric_value": mean_equations,
        "instances_tested": 30 * len(n_values),
        "n_max": max([r["n"] for r in results]),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["max_equations"] for r in results) > 10:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")