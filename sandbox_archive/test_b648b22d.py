# auto-injected by SEC sandbox
import itertools
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from collections import defaultdict

def generate_random_unsat_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        if len(set(clause)) == 2:
            clauses.append(clause)
    return clauses

def evaluate_polynomial(poly, assignment):
    result = 1
    for var in poly:
        if var > 0:
            result *= (1 - assignment[var-1])
        else:
            result *= (1 + assignment[-var-1])
    return result % 2

def frobenius_trace_defect(poly, n):
    count = 0
    for a in range(3**n):
        assignment = [(a // (3**(i))) % 3 for i in range(n)]
        if evaluate_polynomial(poly, assignment) ** 3 != evaluate_polynomial(poly, assignment):
            count += 1
    return count

def enumerate_circuits(n, max_gates):
    gates = ['AND', 'OR', 'NOT', 'XOR']
    circuits = [[]]
    for _ in range(max_gates):
        new_circuits = []
        for circuit in circuits:
            for gate in gates:
                new_circuit = [gate] + circuit
                if len(new_circuit) <= n:
                    new_circuits.append(new_circuit)
        circuits.extend(new_circuits)
    return circuits

def build_truth_table(circuit, variables):
    truth_table = {}
    for assignment in product([0, 1], repeat=len(variables)):
        inputs = {variables[i]: assignment[i] for i in range(len(variables))}
        result = evaluate_circuit(circuit, inputs)
        truth_table[assignment] = result
    return truth_table

def evaluate_circuit(circuit, inputs):
    if len(circuit) == 1:
        var = circuit[0]
        return inputs[var]
    gate = circuit[0]
    args = circuit[1:]
    if gate == 'AND':
        return all(evaluate_circuit(arg, inputs) for arg in args)
    elif gate == 'OR':
        return any(evaluate_circuit(arg, inputs) for arg in args)
    elif gate == 'NOT':
        return not evaluate_circuit(args[0], inputs)
    elif gate == 'XOR':
        return sum(evaluate_circuit(arg, inputs) for arg in args) % 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    results = []
    
    for n in n_values:
        for _ in range(50):
            clauses = generate_random_unsat_3cnf(n)
            poly = defaultdict(int)
            for clause in clauses:
                monomial = 1
                for var in clause:
                    if var > 0:
                        monomial *= (1 - var)
                    else:
                        monomial *= (1 + var)
                poly[tuple(sorted(clause))] += monomial % 2
            
            d_3 = frobenius_trace_defect(poly, n)
            
            max_gates = min(12, n)
            circuits = enumerate_circuits(n, max_gates)
            for circuit in circuits:
                truth_table = build_truth_table(circuit, list(range(1, n+1)))
                if set(truth_table.keys()) == {tuple(sorted(clause)) for clause in clauses}:
                    S_hat = len(circuit) + 1
                    break
            
            slack = math.log2(S_hat) - (0.25 * d_3 / 3**(n/2))
            results.append({
                "metric_name": "slack",
                "metric_value": slack,
                "instances_tested": 1,
                "conjecture_holds": slack > 0,
                "counterexample": ""
            })
    
    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "n_values": n_values,
        "results": results,
        "mean_slack": mean_slack,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
    
    mean_slack = sum(result["mean_slack"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.95) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_slack} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = min(result["seed"] for result in results if result["support_fraction"] < 0.95)
        print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={first_failing_seed}")