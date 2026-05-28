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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses

    def arithmetic_divergence(cnf):
        n = len(cnf[0])
        lattice_points = []
        for assignment in itertools.product([-1, 1], repeat=n):
            if all(assignment[i] * clause[i] >= 0 for clause in cnf):
                lattice_points.append(assignment)
        
        if not lattice_points:
            return float('inf')
        
        avg_distance = 0
        for i in range(len(lattice_points)):
            for j in range(i + 1, len(lattice_points)):
                distance = sum(abs(lattice_points[i][k] - lattice_points[j][k]) for k in range(n))
                avg_distance += distance
        
        avg_distance /= (len(lattice_points) * (len(lattice_points) - 1)) / 2
        return avg_distance

    def construct_xor_circuit(n, S):
        circuit = []
        for _ in range(S):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(gate)]
            circuit.append((gate, inputs))
        return circuit

    def evaluate_circuit(circuit, assignment):
        stack = list(assignment)
        for gate, inputs in reversed(circuit):
            if gate == 'AND':
                result = all(stack[i] for i in inputs)
            elif gate == 'OR':
                result = any(stack[i] for i in inputs)
            stack.append(result)
        return stack[-1]

    def arithmetic_divergence_circuit(circuit, n):
        assignments = list(itertools.product([0, 1], repeat=n))
        distances = []
        for assignment in assignments:
            output = evaluate_circuit(circuit, assignment)
            distance = sum(abs(assignment[i] - output) for i in range(n))
            distances.append(distance)
        
        avg_distance = sum(distances) / len(distances)
        return avg_distance

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    A_F = arithmetic_divergence(cnf)

    S = random.randint(1, 40)
    D = random.randint(1, 40)
    circuit = construct_xor_circuit(n, S)
    A_C = arithmetic_divergence_circuit(circuit, n)

    if A_F == float('inf'):
        return {
            "metric_name": "Arithmetic Divergence",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined for infinite arithmetic divergence"
        }

    ratio = A_C / (math.sqrt(S) + math.pow(D, 0.25))
    
    return {
        "metric_name": "Arithmetic Divergence",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio < 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*41, 2))  # Generate 30 prime-like seeds if none provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mapping undefined for infinite arithmetic divergence\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")