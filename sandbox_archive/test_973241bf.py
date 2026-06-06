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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def evaluate_formula(formula):
        if formula == '0':
            return 0
        elif formula == '1':
            return 1
        else:
            left, operator, right = formula.split()
            if operator == '&':
                return evaluate_formula(left) & evaluate_formula(right)
            elif operator == '|':
                return evaluate_formula(left) | evaluate_formula(right)
    
    def concept_lattice(formula):
        variables = set()
        for char in formula:
            if char.isalpha():
                variables.add(char)
        
        n = len(variables)
        lattice = [[0] * (1 << n) for _ in range(1 << n)]
        
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i & (1 << k)) == (j & (1 << k)) for k in variables):
                    lattice[i][j] = 1
        
        return lattice
    
    def frege_proof_width(formula):
        stack = []
        depth = 0
        max_depth = 0
        
        for char in formula:
            if char.isalpha():
                stack.append(char)
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack[-1] != '(':
                    stack.pop()
                stack.pop()
                depth -= 1
            else:  # '&' or '|'
                stack.pop()
                depth += 1
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    def min_formal_concepts(lattice):
        n = len(lattice)
        count = 0
        
        for i in range(1 << n):
            if all(lattice[i][j] == lattice[j][i] for j in range(1 << n)):
                count += 1
        
        return count
    
    def generate_random_formula(n):
        formula = generate_boolean_formula(n)
        while evaluate_formula(formula) == 0:
            formula = generate_boolean_formula(n)
        return formula
    
    instances_tested = 0
    total_concept_count = 0
    total_proof_width = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_random_formula(n)
        
        lattice = concept_lattice(formula)
        concept_count = min_formal_concepts(lattice)
        proof_width = frege_proof_width(formula)
        
        total_concept_count += concept_count
        total_proof_width += proof_width
        instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Min Formal Concepts / Proof Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_concept_count = total_concept_count / instances_tested
    mean_proof_width = total_proof_width / instances_tested
    
    if abs(mean_concept_count - mean_proof_width) > 0.1 * mean_concept_count:
        return {
            "metric_name": "Min Formal Concepts / Proof Width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Outlier in concept count or proof width"
        }
    
    return {
        "metric_name": "Min Formal Concepts / Proof Width",
        "metric_value": mean_concept_count / mean_proof_width,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")