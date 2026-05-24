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
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        assignment = {i: None for i in range(1, n+1)}
        stack = []
        for clause in clauses:
            found_unassigned = False
            for literal in clause:
                if assignment[abs(literal)] == -literal:
                    return False
                elif assignment[abs(literal)] is None:
                    found_unassigned = True
                    stack.append((literal, assignment))
                    break
            if not found_unassigned:
                continue
            while stack and stack[-1][0] != literal:
                _, assignment = stack.pop()
                assignment[abs(stack[-1][0])] = None
            if stack:
                assignment[abs(literal)] = -literal
        return True
    
    def compute_symmetry_index(clauses):
        n = len(clauses)
        symmetries = 0
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if all((i in clause or -i in clause) == (j in clause or -j in clause) for clause in clauses):
                    symmetries += 1
        return symmetries
    
    def compute_circuit_complexity(clauses):
        # Placeholder for actual circuit complexity computation
        return len(clauses)
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    symmetry_index = compute_symmetry_index(clauses)
    circuit_complexity = compute_circuit_complexity(clauses)
    
    c = 1.5 ** n
    conjecture_holds = abs(symmetry_index - c) <= 1 and circuit_complexity > c
    
    return {
        "metric_name": "Symmetry Index vs Circuit Complexity",
        "metric_value": symmetry_index,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Symmetry index {symmetry_index} does not match expected value {c}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")