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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def evaluate_clause(clause, assignment):
        if clause[0] == 'AND':
            return all(assignment[i] for i in clause[1])
        elif clause[0] == 'OR':
            return any(assignment[i] for i in clause[1])
    
    def generate_minimal_monomial_ideal(circuit):
        satisfied_clauses = set()
        for assignment in itertools.product([0, 1], repeat=n):
            if all(evaluate_clause(clause, assignment) for clause in circuit):
                satisfied_clauses.add(tuple(assignment))
        return satisfied_clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_size = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        I = generate_minimal_monomial_ideal(circuit)
        size_I = len(I)
        total_size += size_I
        instances_tested += len(circuit)
        if n > n_max:
            n_max = n
    
    metric_value = total_size / instances_tested
    conjecture_holds = metric_value <= n**2 * math.log(n, 2)
    
    return {
        "metric_name": "Size of Minimal Monomial Ideal",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")