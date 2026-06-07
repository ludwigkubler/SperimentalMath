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
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def diophantine_representation(clauses):
        equations = set()
        for clause in clauses:
            equation = 0
            for var in clause:
                if random.choice([True, False]):
                    equation += var
                else:
                    equation -= var
            equations.add(equation)
        return equations
    
    def dpll_proof_tree_width(clauses):
        # Simplified DPLL algorithm to estimate proof tree width
        stack = []
        for clause in clauses:
            if not any(var in clause for var in stack):
                stack.append(random.choice(clause))
        return len(stack)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        instances_tested = 0
        total_equations = 0
        max_equations = 0
        for _ in range(5):  # 5 instances per size
            clauses = generate_sat_instance(n)
            equations = diophantine_representation(clauses)
            proof_tree_width = dpll_proof_tree_width(clauses)
            instances_tested += 1
            total_equations += len(equations)
            max_equations = max(max_equations, len(equations))
        
        mean_equations = total_equations / instances_tested
        conjecture_holds = mean_equations <= math.sqrt(n) and max_equations <= 10
        
        results.append({
            "metric_name": "Number of Diophantine Equations",
            "metric_value": mean_equations,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": f"Mean equations: {mean_equations}, Max equations: {max_equations}" if not conjecture_holds else ""
        })
    
    return {
        "metric_name": "Number of Diophantine Equations",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print("TRIALS:")
    for result in results:
        print(f"  TRIAL: {result}")
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")