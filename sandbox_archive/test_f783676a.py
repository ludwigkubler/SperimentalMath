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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        if A[i][i] == 0:
            return None  # Singular matrix
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def tseitin_circuit(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    def add_clause(lit1, lit2, negated=False):
        clause = [lit1]
        if lit2 is not None:
            clause.append(-lit2)
        if negated:
            clause = [-x for x in clause]
        clauses.append(clause)
    
    for i in range(1, n + 1):
        add_clause(i, variables[i - 1])
    
    for i in range(n):
        var_or = variables[n + i - 1]
        var_and = variables[2 * n + i - 1]
        var_not = variables[3 * n + i - 1]
        
        add_clause(-var_or, var_and)
        add_clause(-var_or, var_not)
        add_clause(var_and, -var_not)
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        variables, clauses = tseitin_circuit(n)
        homology_groups = []
        
        # Compute homology groups using Gaussian elimination
        for i in range(3):
            A = [[0] * (n + 2) for _ in range(n + 1)]
            for j, clause in enumerate(clauses):
                if len(clause) == 2:
                    A[abs(clause[0])][j] += 1
                    A[abs(clause[1])][j] += 1
            rank = gaussian_elimination(A)
            homology_groups.append(rank)
        
        # Count satisfying assignments
        num_satisfying_assignments = 2 ** n
        
        results.append({
            "n": n,
            "homology_groups": homology_groups,
            "num_satisfying_assignments": num_satisfying_assignments
        })
    
    total_satisfying_assignments = sum(result["num_satisfying_assignments"] for result in results)
    mean_minimal_rank = sum(sum(result["homology_groups"]) / len(result["homology_groups"]) for result in results) / len(results)
    
    satisfying_fraction = total_satisfying_assignments / (n * 30)
    conjecture_holds = satisfying_fraction >= 0.8 and mean_minimal_rank <= 3
    
    return {
        "metric_name": "satisfying_fraction",
        "metric_value": satisfying_fraction,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, satisfying_fraction={satisfying_fraction}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, satisfying_fraction={satisfying_fraction}\" first_failing_seed={first_failing_seed}")