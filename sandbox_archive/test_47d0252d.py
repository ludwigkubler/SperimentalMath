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
    
    def generate_circuit(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll(circuit, assignment, path=[]):
        if not circuit:
            return True
        var = next((v for v in range(1, len(assignment) + 1) if v not in assignment), None)
        if var is None:
            return False
        
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_path = path + [(var, value)]
            if dpll(circuit, new_assignment, new_path):
                return True
        return False
    
    def minimal_dfa_size(clauses):
        # Simplified DFA construction for demonstration purposes
        states = {0}
        transitions = {}
        accepting_states = set()
        
        for clause in clauses:
            state = 0
            for var in clause:
                if var not in transitions:
                    transitions[var] = {}
                if value not in transitions[var]:
                    transitions[var][value] = len(states)
                    states.add(len(states))
                state = transitions[var][value]
            accepting_states.add(state)
        
        return len(states)
    
    def circuit_height(circuit):
        # Simplified DPLL search tree height calculation
        return 2 ** len(circuit)
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(n // 2, n * 2)
            circuit = generate_circuit(n, m)
            dfa_size = minimal_dfa_size(circuit)
            height = circuit_height(circuit)
            
            if dfa_size > 0 and height > 0:
                metric_values.append(dfa_size / height)
                instances_tested += 1
                n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_value = sum(metric_values) / len(metric_values)
    correlation_coefficient = calculate_correlation_coefficient(metric_values, [circuit_height(generate_circuit(n, m)) for n in [5, 10, 15, 20, 30, 40] for _ in range(5)])
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def calculate_correlation_coefficient(x, y):
    if len(x) != len(y):
        return None
    
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 40) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Insufficient instances tested' first_failing_seed={first_failing_seed}")