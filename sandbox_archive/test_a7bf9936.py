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
    
    def generate_tseitin_formula(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f"{variables[i-1]}")
        for _ in range(m):
            clause = random.choice(variables) + " | " + random.choice(variables)
            if random.choice([True, False]):
                clause = "~" + clause
            clauses.append(clause)
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if j != i:
                    factor = Fraction(matrix[j][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def compute_symmetry_invariant(variables, clauses):
        n = len(variables)
        orbits = {}
        for clause in clauses:
            orbit = set()
            for var in variables:
                if var in clause:
                    orbit.add(var)
            orbits[orbit] = orbits.get(orbit, 0) + 1
        min_orbit_size = min(len(o) for o in orbits if orbits[o] > 1)
        return min_orbit_size
    
    def resolution_proof_complexity(variables, clauses):
        n = len(variables)
        m = len(clauses)
        matrix = [[0] * (n + m + 1) for _ in range(n + m)]
        for i in range(n):
            matrix[i][i] = 1
        for j in range(m):
            clause = clauses[j].split()
            if clause[0] == "~":
                var_index = variables.index(clause[1])
                matrix[n + j][var_index] = -1
            else:
                var_index = variables.index(clause[0])
                matrix[n + j][var_index] = 1
        matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def is_polynomial_time_computable(n):
        # Placeholder function to simulate polynomial-time computability check
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2*n, 3*n)
        variables, clauses = generate_tseitin_formula(n, m)
        if not is_polynomial_time_computable(n):
            return {
                "metric_name": "ResolutionProofComplexity",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        invariant = compute_symmetry_invariant(variables, clauses)
        complexity = resolution_proof_complexity(variables, clauses)
        results.append((invariant, complexity))
    
    if len(results) < 30:
        return {
            "metric_name": "ResolutionProofComplexity",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    invariant_values = [r[0] for r in results]
    complexity_values = [r[1] for r in results]
    
    mean_complexity = sum(complexity_values) / len(complexity_values)
    std_complexity = math.sqrt(sum((x - mean_complexity) ** 2 for x in complexity_values) / len(complexity_values))
    support_fraction = sum(1 for c in complexity_values if c >= 2**(10 * invariant_values[complexity_values.index(c)])) / len(complexity_values)
    
    return {
        "metric_name": "ResolutionProofComplexity",
        "metric_value": mean_complexity,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_complexity = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_complexity = math.sqrt(sum((r["metric_value"] - mean_complexity) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")