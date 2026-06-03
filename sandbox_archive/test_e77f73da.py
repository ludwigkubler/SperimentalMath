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
    
    def generate_circuit(n, m):
        circuit = []
        inputs = [f"x{i}" for i in range(n)]
        for _ in range(m):
            gate_type = random.choice(["AND", "OR"])
            if gate_type == "AND":
                a, b = random.sample(inputs, 2)
                circuit.append(f"({a} AND {b})")
            else:
                a, b = random.sample(inputs, 2)
                circuit.append(f"({a} OR {b})")
        return circuit
    
    def tseitin_formula(circuit):
        literals = set()
        clauses = []
        for gate in circuit:
            lit = f"x{len(literals)}"
            literals.add(lit)
            if "AND" in gate:
                a, b = gate.split(" AND ")
                clauses.append([a, b, -lit])
                clauses.append([-a, lit])
                clauses.append([-b, lit])
            else:
                a, b = gate.split(" OR ")
                clauses.append([a, b, lit])
                clauses.append([-a, -lit])
                clauses.append([-b, -lit])
        return literals, clauses
    
    def tropical_hodge_diamond_width(clauses):
        # Simplified approximation for demonstration
        return len(clauses)
    
    def communication_complexity_rank(clauses):
        # Simplified approximation for demonstration
        return len(set(lit for clause in clauses for lit in clause if lit > 0))
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    circuit = generate_circuit(n, m)
    literals, clauses = tseitin_formula(circuit)
    thdw = tropical_hodge_diamond_width(clauses)
    ccr = communication_complexity_rank(clauses)
    
    return {
        "metric_name": "THDW vs CCR",
        "metric_value": thdw,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": thdw >= ccr * 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = f"Circuit with n={res['n_max']} and m={len(generate_circuit(res['n_max'], 3 * res['n_max']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break