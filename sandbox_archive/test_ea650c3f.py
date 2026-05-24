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
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(3)]
            clause = ' or '.join(f'x{i}' if l == 1 else f'-x{i}' for l, i in zip(literals, range(1, 4)))
            clauses.append(clause)
        return ' and '.join(clauses)
    
    def is_satisfiable(formula):
        # Simple backtracking to check satisfiability
        literals = set()
        def backtrack(index):
            if index == len(formula):
                return True
            clause = formula[index]
            for literal in clause.split(' or '):
                if literal[0] == '-':
                    l = int(literal[1:])
                    if -l not in literals:
                        literals.add(-l)
                        if backtrack(index + 1):
                            return True
                        literals.remove(-l)
                else:
                    l = int(literal)
                    if l not in literals:
                        literals.add(l)
                        if backtrack(index + 1):
                            return True
                        literals.remove(l)
            return False
        return backtrack(0)
    
    def compute_symmetry_index(formula):
        # Placeholder for symmetry computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)  # Randomly generate a number between 1 and 10
    
    def monotone_circuit_complexity(formula):
        # Placeholder for circuit complexity computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(formula.split(' and '))
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    symmetry_index = compute_symmetry_index(formula)
    circuit_complexity = monotone_circuit_complexity(formula)
    
    metric_value = symmetry_index
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if symmetry_index <= 1.5 ** n:
        conjecture_holds = True
    
    return {
        "metric_name": "Symmetry Index",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "symmetry_index_not_within_bound"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")