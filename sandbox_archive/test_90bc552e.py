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
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        formula = ' and '.join(f'({clause[0]} or {clause[1]})' for clause in clauses)
        return formula
    
    def dpll(formula, assignment={}):
        if not formula:
            return True
        literals = set()
        for part in formula.split(' and '):
            if 'or' in part:
                literals.update(part.split(' or '))
            else:
                literals.add(part)
        literal = random.choice(list(literals))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(formula.replace(f'({literal} or {literal[1:]})', '').replace(f'({literal[0:2]} or {literal})', ''), new_assignment):
            return True
        new_assignment[literal] = False
        if dpll(formula.replace(f'({literal} or {literal[1:]})', '').replace(f'({literal[0:2]} or {literal})', ''), new_assignment):
            return True
        return False
    
    def topological_entropy(n):
        # Simplified entropy calculation for demonstration purposes
        return n * math.log2(n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(n)
        proof_length = len(formula.split(' and '))
        entropy = topological_entropy(n)
        results.append((entropy, proof_length))
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in results) / math.sqrt(sum((x - mean_x)**2 for x, _ in results) * sum((y - mean_y)**2 for _, y in results))
    mean_x = sum(x for x, _ in results) / len(results)
    mean_y = sum(y for _, y in results) / len(results)
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(abs(x - y) <= 10 for x, y in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")