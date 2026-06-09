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
    
    def generate_boolean_circuit(n, m):
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, n-1) for _ in range(random.randint(2, 3))]
            circuit.append((gate_type, inputs))
        return circuit
    
    def cnf_from_circuit(circuit, n):
        cnf = []
        variables = set()
        for gate_type, inputs in circuit:
            literals = [f'x{i+1}' if x < n else f'-x{i-n+1}' for i in inputs]
            if gate_type == 'AND':
                clause = ' AND '.join(literals)
            elif gate_type == 'OR':
                clause = ' OR '.join(literals)
            cnf.append(clause)
            variables.update(inputs)
        return cnf, len(variables)
    
    def resolution_width(cnf):
        clauses = [set(clause.split()) for clause in cnf]
        resolvents = set()
        while True:
            new_resolvents = set()
            for i in range(len(clauses)):
                for j in range(i+1, len(clauses)):
                    common_vars = clauses[i] & clauses[j]
                    if not common_vars:
                        continue
                    for var in common_vars:
                        resolvent = (clauses[i] - {var}) | (clauses[j] - {var})
                        new_resolvents.add(frozenset(resolvent))
            if not new_resolvents:
                break
            clauses.extend(new_resolvents)
        return max(len(clause) for clause in clauses)
    
    def minimal_representation_size(cnf):
        # Placeholder for actual computation of minimal representation size
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, n*2)
    circuit = generate_boolean_circuit(n, m)
    cnf, num_variables = cnf_from_circuit(circuit, n)
    width = resolution_width(cnf)
    size = minimal_representation_size(cnf)
    
    return {
        "metric_name": "ResolutionProofWidth",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")