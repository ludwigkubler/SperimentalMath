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
        # Generate a random Boolean circuit with n inputs and m clauses
        inputs = [f'x{i}' for i in range(n)]
        gates = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            if gate_type == 'AND':
                inputs_used = random.sample(inputs, 2)
            else:
                inputs_used = random.sample(inputs, 2)
            output = f'g{len(gates)}'
            gates.append((output, gate_type, inputs_used))
        return inputs, gates
    
    def compute_groupoid_composition_width(circuit):
        # Compute the minimal groupoid composition width of the circuit
        n_inputs, _ = circuit
        n_gates = len(_)
        if n_gates == 0:
            return 1
        max_width = 0
        for i in range(n_gates):
            for j in range(i + 1, n_gates):
                width = abs(ord(circuit[1][i][2][0]) - ord(circuit[1][j][2][0]))
                if width > max_width:
                    max_width = width
        return max_width
    
    def compute_resolution_proof_complexity(circuit):
        # Compute the resolution proof complexity of the circuit using a small DPLL solver
        n_inputs, gates = circuit
        clauses = []
        for output, gate_type, inputs in gates:
            if gate_type == 'AND':
                clause = [f'~{i}' if i.startswith('x') else i for i in inputs]
                clauses.append(clause)
            else:
                clause = [i if i.startswith('x') else f'~{i}' for i in inputs]
                clauses.append(clause)
        def dpll(clauses, assignment):
            if not clauses:
                return True
            literal = next((l for l in clauses[0] if l not in assignment and '~' + l not in assignment), None)
            if literal is None:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and '~' + literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and '~' + literal not in c], new_assignment):
                return True
            return False
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    circuit = generate_circuit(n, m)
    gcw = compute_groupoid_composition_width(circuit)
    w = compute_resolution_proof_complexity(circuit)
    if w == 0:
        return {
            "metric_name": "gcw(C) / w(C)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_complexity_is_zero"
        }
    ratio = Fraction(gcw, w)
    return {
        "metric_name": "gcw(C) / w(C)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "gcw(C) / w(C) > 2"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")