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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def tseitin_formula(clauses):
        literals = set()
        new_vars = {}
        for i, clause in enumerate(clauses):
            literals.update(abs(lit) for lit in clause)
            new_var = max(literals) + 1
            new_vars[new_var] = clause
            clauses.append([new_var, -clause[0]])
            clauses.append([-new_var, -clause[1]])
            clauses.append([-new_var, -clause[2]])
        return clauses
    
    def tropical_derivative_rank(clauses):
        n = max(abs(lit) for lit in set().union(*clauses))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit - 1] += 1
                else:
                    matrix[-lit - 1][-lit - 1] += 1
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def resolution_proof_width(clauses):
        n = max(abs(lit) for lit in set().union(*clauses))
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    matrix[lit - 1][lit - 1] += 1
                else:
                    matrix[-lit - 1][-lit - 1] += 1
        width = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(n)):
                width += 1
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n)
        tdr = tropical_derivative_rank(clauses)
        rpw = resolution_proof_width(tseitin_formula(clauses))
        results.append({"n": n, "tdr": tdr, "rpw": rpw})
    
    if not all(result["tdr"] <= 2 * result["rpw"] for result in results):
        return {
            "metric_name": "tdr_vs_rpw",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "discrepancy_greater_than_5"
        }
    
    return {
        "metric_name": "tdr_vs_rpw",
        "metric_value": sum(result["tdr"] / result["rpw"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_failing_seed['counterexample']}\" first_failing_seed={first_failing_seed['seed']}")
    else:
        print("RESULT: INCONCLUSIVE no_data")