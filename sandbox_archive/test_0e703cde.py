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

def generate_ac0_circuit(n):
    if n == 1:
        return ["NOT"]
    else:
        left = generate_ac0_circuit(n // 2)
        right = generate_ac0_circuit(n - n // 2)
        return [random.choice(["AND", "OR"]) + "_" + str(n), left, right]

def evaluate_circuit(circuit, inputs):
    if isinstance(circuit, list) and circuit[0] == "NOT":
        return not evaluate_circuit(circuit[1], inputs)
    elif isinstance(circuit, list) and circuit[0] in ["AND", "OR"]:
        left = evaluate_circuit(circuit[1], inputs)
        right = evaluate_circuit(circuit[2], inputs)
        if circuit[0] == "AND":
            return left and right
        else:
            return left or right
    else:
        return inputs[circuit]

def generate_polynomial_system(circuit, n):
    def encode_gate(gate, inputs):
        if gate == "NOT":
            x = inputs.pop()
            return f"{x} - {1 - x}"
        elif gate.startswith("AND"):
            m = int(gate.split("_")[1])
            x = inputs.pop()
            y = inputs.pop()
            return f"{x} * {y} - {inputs[m]}"
        elif gate.startswith("OR"):
            m = int(gate.split("_")[1])
            x = inputs.pop()
            y = inputs.pop()
            return f"{x} + {y} - {inputs[m]} - 1"
    
    inputs = list(range(n))
    equations = []
    for gate in circuit:
        equations.append(encode_gate(gate, inputs))
    return equations

def solve_polynomial_system(equations):
    n = len(equations)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    for i, eq in enumerate(equations):
        terms = eq.split(" - ")
        for term in terms:
            if "x" in term:
                var = int(term[1:])
                A[i][var] += 1
            else:
                b[i] -= int(term)
    
    # Gaussian elimination with partial pivoting
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    
    return x

def count_connected_components(equations):
    solutions = set()
    for _ in range(100):  # Sample multiple points
        inputs = [random.choice([0, 1]) for _ in range(len(equations))]
        try:
            solution = solve_polynomial_system(generate_polynomial_system(equations, len(inputs)))
            solutions.add(tuple(solution))
        except Exception as e:
            return None
    
    # Check connected components
    visited = set()
    def dfs(solution):
        if solution in visited:
            return
        visited.add(solution)
        for i in range(len(solution)):
            new_solution = list(solution)
            new_solution[i] = 1 - new_solution[i]
            dfs(tuple(new_solution))
    
    for solution in solutions:
        if solution not in visited:
            dfs(solution)
    
    return len(visited)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    equations = generate_polynomial_system(circuit, n)
    
    if equations is None:
        return {
            "metric_name": "connected_components",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    components = count_connected_components(equations)
    if components is None:
        return {
            "metric_name": "connected_components",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "solver_failure"
        }
    
    size = len(circuit)
    log_size = math.log(size, 2) if size > 0 else 0
    
    return {
        "metric_name": "connected_components",
        "metric_value": components,
        "instances_tested": 1,
        "conjecture_holds": components >= log_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")