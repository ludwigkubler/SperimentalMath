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
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses

    def is_clause_satisfied(clause, assignment):
        return any(assignment[abs(lit) - 1] == lit for lit in clause)

    def evaluate_circuit(circuit, assignment):
        stack = []
        for gate in circuit:
            if isinstance(gate, int):
                stack.append(assignment[gate - 1])
            else:
                a, b = stack.pop(), stack.pop()
                if gate == 'AND':
                    stack.append(a and b)
                elif gate == 'OR':
                    stack.append(a or b)
        return stack[-1]

    def find_circuit_size(n):
        clauses = generate_3cnf(n)
        assignment = [random.choice([True, False]) for _ in range(n)]
        
        # Convert 3-CNF to circuit
        circuit = []
        for clause in clauses:
            subcircuit = []
            for lit in clause:
                if lit > 0:
                    subcircuit.append(lit)
                else:
                    subcircuit.append(('NOT', -lit))
            circuit.append(subcircuit)
        
        # Evaluate circuit and find size
        size = 0
        for gate in circuit:
            if isinstance(gate, list):
                size += len(gate) + 1
            else:
                size += 1
        
        return size

    n = random.randint(10, 40)
    circuit_size = find_circuit_size(n)
    
    metric_name = "circuit_size"
    metric_value = circuit_size
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "circuit_size_too_large"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")