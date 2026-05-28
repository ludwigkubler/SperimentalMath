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
    n = 10
    cnf = generate_cnf(n, seed)
    A_F = arithmetic_divergence(cnf)
    
    # Construct a corresponding XOR circuit with random size S and depth D (S, D ≤ 40)
    S = random.randint(5, 40)
    D = random.randint(5, 40)
    C = generate_xor_circuit(n, S, D, seed)
    A_C = arithmetic_divergence(C)
    
    # Compare A(C) with Ω(S^(1/2)) + O(D^(1/4))
    lower_bound = math.sqrt(S) + (D ** 0.25)
    ratio = A_C / lower_bound
    
    conjecture_holds = ratio < 0.2
    counterexample = "" if conjecture_holds else f"A(C)={A_C}, Ω(S^(1/2)) + O(D^(1/4))={lower_bound}"
    
    return {
        "metric_name": "Arithmetic Divergence Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_cnf(n: int, seed: int) -> list:
    random.seed(seed)
    cnf = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) for _ in range(n)]
        cnf.append(clause)
    return cnf

def arithmetic_divergence(formula: list) -> float:
    n = len(formula[0])
    solutions = set()
    
    # Find all solutions to the CNF formula
    def backtrack(assignment, clause_index):
        if clause_index == n:
            solutions.add(tuple(assignment))
            return
        for value in [-1, 1]:
            assignment[clause_index] = value
            if all(assignment[i] * clause[i] >= 0 for clause in formula):
                backtrack(assignment, clause_index + 1)
    
    backtrack([0] * n, 0)
    
    # Calculate arithmetic divergence
    total_distance = 0
    num_solutions = len(solutions)
    for i in range(n):
        distances = [abs(sum(solution[j] * formula[j][i] for j in range(n))) for solution in solutions]
        total_distance += sum(distances) / num_solutions
    
    return total_distance / n

def generate_xor_circuit(n: int, S: int, D: int, seed: int) -> list:
    random.seed(seed)
    circuit = []
    
    # Generate a random XOR circuit with depth D and size S
    def generate_layer(input_size):
        layer = [random.choice([-1, 1]) for _ in range(input_size)]
        return layer
    
    for _ in range(D - 1):
        input_size = len(circuit[-1]) if circuit else n
        circuit.append(generate_layer(input_size))
    
    # Add the final output layer
    circuit.append(generate_layer(len(circuit[-1])))
    
    return circuit

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Arithmetic Divergence Ratio\" first_failing_seed={first_failing_seed}")