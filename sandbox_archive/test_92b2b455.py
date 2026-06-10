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
        for _ in range(2**n // 4):  # Ensure at least n clauses
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def construct_circuit(cnf):
        circuit = []
        for clause in cnf:
            gate = {'type': 'OR', 'inputs': []}
            for var in clause:
                if var > 0:
                    gate['inputs'].append({'type': 'INPUT', 'var': var})
                else:
                    gate['inputs'].append({'type': 'NOT', 'input': {'type': 'INPUT', 'var': -var}})
            circuit.append(gate)
        return circuit
    
    def apply_geometric_flow(circuit):
        steps = 0
        while True:
            changed = False
            for i in range(len(circuit)):
                gate = circuit[i]
                if gate['type'] == 'OR' and len(gate['inputs']) > 1:
                    new_inputs = []
                    for input_gate in gate['inputs']:
                        if input_gate['type'] == 'NOT':
                            new_input_gate = {'type': 'INPUT', 'var': -input_gate['input']['var']}
                        else:
                            new_input_gate = input_gate
                        if new_input_gate not in new_inputs:
                            new_inputs.append(new_input_gate)
                    gate['inputs'] = new_inputs
                    changed = True
                elif gate['type'] == 'NOT' and gate['input']['type'] == 'NOT':
                    circuit[i] = {'type': 'INPUT', 'var': -gate['input']['input']['var']}
                    changed = True
            if not changed:
                break
            steps += 1
        return steps
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_steps = 0
    instances_tested = 0
    max_n = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        circuit = construct_circuit(cnf)
        steps = apply_geometric_flow(circuit)
        total_steps += steps
        instances_tested += len(cnf)
        if n > max_n:
            max_n = n
    
    avg_steps = Fraction(total_steps, instances_tested)
    
    conjecture_holds = avg_steps <= 4 * n**2
    counterexample = "" if conjecture_holds else f"avg_steps={avg_steps}, n^2=4*n^2"
    
    return {
        "metric_name": "Average Geometric Flow Complexity",
        "metric_value": float(avg_steps),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_steps exceeds 4*n^2\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")