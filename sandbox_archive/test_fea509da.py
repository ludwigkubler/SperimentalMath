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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] += factor * matrix[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = matrix[i][-1]
        for j in range(i+1, n):
            x[i] -= matrix[i][j] * x[j]
        x[i] /= matrix[i][i]
    
    return x

def random_cnf(n):
    clauses = []
    for _ in range(2**n // 3):  # Ensure satisfiability
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if len(set(abs(lit) for lit in clause)) == n:
            clauses.append(clause)
    return clauses

def cnf_to_circuit(cnf):
    # Simplified circuit construction using a lookup table
    n = max(abs(lit) for clause in cnf for lit in clause)
    truth_table = [[0] * (2**n) for _ in range(n)]
    
    def evaluate(variable, assignment):
        if variable > 1:
            return evaluate(-variable // 2, assignment) and evaluate(variable % 2, assignment)
        elif variable == 1:
            return assignment[0]
        else:
            return not assignment[0]
    
    for i in range(n):
        for j in range(2**n):
            truth_table[i][j] = evaluate(i + 1, [bool(j & (1 << k)) for k in range(n)])
    
    circuit = []
    for clause in cnf:
        gate = []
        for lit in clause:
            if lit > 0:
                gate.append(truth_table[lit - 1])
            else:
                gate.append([not x for x in truth_table[-lit - 1]])
        circuit.append(gate)
    
    return circuit

def monotone_width(circuit):
    n = len(circuit)
    dp = [[0] * (2**n) for _ in range(n)]
    
    def evaluate_gate(gate, assignment):
        return any(all(assignment[j] for j in gate[i]) for i in range(len(gate)))
    
    for i in range(n):
        for j in range(2**n):
            dp[i][j] = max(dp[i-1][k] if k & (1 << i) == 0 else dp[i-1][k] + evaluate_gate(circuit[i], [bool(j & (1 << k)) for k in range(n)]), default=0)
    
    return max(max(row) for row in dp)

def minimal_number_field_trace(cnf):
    # Simplified computation using a lookup table
    n = max(abs(lit) for clause in cnf for lit in clause)
    truth_table = [[0] * (2**n) for _ in range(n)]
    
    def evaluate(variable, assignment):
        if variable > 1:
            return evaluate(-variable // 2, assignment) and evaluate(variable % 2, assignment)
        elif variable == 1:
            return assignment[0]
        else:
            return not assignment[0]
    
    for i in range(n):
        for j in range(2**n):
            truth_table[i][j] = evaluate(i + 1, [bool(j & (1 << k)) for k in range(n)])
    
    trace = sum(truth_table[i][i] for i in range(n))
    return trace

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    mnt_phi_list = []
    circuit_phi_list = []
    
    for n in n_values:
        cnf = random_cnf(n)
        mnt_phi = minimal_number_field_trace(cnf)
        circuit = cnf_to_circuit(cnf)
        circuit_phi = monotone_width(circuit)
        
        if mnt_phi is not None and circuit_phi is not None:
            mnt_phi_list.append(mnt_phi)
            circuit_phi_list.append(circuit_phi)
    
    instances_tested = len(mnt_phi_list)
    n_max = max(n_values)
    
    if instances_tested == 0:
        return {
            "metric_name": "mnt_phi vs circuit_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric_value = sum(mnt_phi_list) / instances_tested
    mean_circuit_phi = sum(circuit_phi_list) / instances_tested
    
    total_metric_value = sum(mnt_phi_list)
    
    if instances_tested == 1:
        r_squared = 1.0
    else:
        numerator = instances_tested * total_metric_value**2 - sum(mnt_phi**2 for mnt_phi in mnt_phi_list) * sum(circuit_phi**2 for circuit_phi in circuit_phi_list)
        denominator = (instances_tested - 1) * sum((mnt_phi - mean_metric_value)**2 for mnt_phi in mnt_phi_list) * sum((circuit_phi - mean_circuit_phi)**2 for circuit_phi in circuit_phi_list)
        r_squared = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "mnt_phi vs circuit_phi",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r_squared >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_r_squared = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_squared < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")