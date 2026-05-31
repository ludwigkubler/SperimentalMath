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
    
    def tseitin_formula(n):
        # Generate a random Tseitin formula with n variables
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for _ in range(n - 1):
            new_var = f'x{n + _}'
            clauses.append([new_var, random.choice(literals), random.choice(literals)])
            literals.append(new_var)
        return clauses
    
    def resolution(clauses):
        # Implement a simple resolution algorithm to find the proof width
        seen_clauses = set()
        while True:
            new_clauses = []
            for clause1 in clauses:
                if clause1 not in seen_clauses:
                    seen_clauses.add(clause1)
                    for clause2 in clauses:
                        if clause2 not in seen_clauses and any(-l in clause2 for l in clause1):
                            new_clause = [l for l in clause1 + clause2 if l != -next(l for l in clause1 if -l in clause2)]
                            if len(new_clause) == 0:
                                return len(clauses)
                            new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                return len(clauses)
            clauses.extend(new_clauses)
    
    def coxeter_group(n):
        # Generate the Coxeter group for a given n
        reflections = [[i, i + 1] for i in range(n - 1)]
        generators = {tuple(reflection): Fraction(1) for reflection in reflections}
        
        def multiply(g1, g2):
            result = {}
            for r1, v1 in g1.items():
                for r2, v2 in g2.items():
                    product = tuple(sorted(r1 + r2))
                    if product in result:
                        result[product] += v1 * v2
                    else:
                        result[product] = v1 * v2
            return result
        
        def normalize(g):
            total = sum(v for v in g.values())
            return {r: Fraction(v, total) for r, v in g.items()}
        
        def power(g, k):
            if k == 0:
                return {(): Fraction(1)}
            elif k % 2 == 0:
                half_power = power(g, k // 2)
                return normalize(multiply(half_power, half_power))
            else:
                return multiply(power(g, k - 1), g)
        
        max_reflections = n * (n - 1) // 2
        max_group_size = sum(2 ** i for i in range(max_reflections + 1))
        group_elements = []
        for r in range(1 << max_reflections):
            element = {}
            for i in range(max_reflections):
                if r & (1 << i):
                    element[tuple(sorted(reflections[i]))] = Fraction(1)
            normalized_element = normalize(element)
            if len(normalized_element) <= max_group_size:
                group_elements.append(normalized_element)
        
        return group_elements
    
    def min_reflections(group):
        # Find the minimal number of reflections required to generate all group elements
        n = len(group[0])
        reflections = [[i, i + 1] for i in range(n - 1)]
        generators = {tuple(reflection): Fraction(1) for reflection in reflections}
        
        def multiply(g1, g2):
            result = {}
            for r1, v1 in g1.items():
                for r2, v2 in g2.items():
                    product = tuple(sorted(r1 + r2))
                    if product in result:
                        result[product] += v1 * v2
                    else:
                        result[product] = v1 * v2
            return result
        
        def normalize(g):
            total = sum(v for v in g.values())
            return {r: Fraction(v, total) for r, v in g.items()}
        
        def power(g, k):
            if k == 0:
                return {(): Fraction(1)}
            elif k % 2 == 0:
                half_power = power(g, k // 2)
                return normalize(multiply(half_power, half_power))
            else:
                return multiply(power(g, k - 1), g)
        
        def generate_elements(reflection):
            element = {}
            for r in reflection:
                if r not in element:
                    element[r] = Fraction(1)
            return normalize(element)
        
        min_reflects = n
        for i in range(n * (n - 1) // 2 + 1):
            group_subset = power(generators, i)
            if len(group_subset) >= len(group):
                min_reflects = i
                break
        
        return min_reflects
    
    results = []
    n_max = 0
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        formula = tseitin_formula(n)
        proof_width = resolution(formula)
        group_elements = coxeter_group(n)
        min_reflects = min_reflections(group_elements)
        results.append((n, min_reflects, proof_width))
    
    if not results:
        return {
            "metric_name": "resolution_proof_width_over_min_reflections_squared",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [w / (r ** 2) for _, r, w in results]
    conjecture_holds = all(0.9 <= x / (r ** 2) <= 1.1 for _, r, w in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width_over_min_reflections_squared",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")