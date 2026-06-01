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
    
    def dpll(circuit):
        if not circuit:
            return True
        literal = next((l for l in range(1, len(circuit) + 1) if l not in [x[0] for x in circuit] and -l not in [x[0] for x in circuit]), None)
        if literal is None:
            return False
        def propagate(lit):
            new_circuit = []
            for clause in circuit:
                if lit in clause:
                    continue
                if -lit in clause:
                    clause.remove(-lit)
                    if not clause:
                        return False
                else:
                    new_clause = [x for x in clause if x != -lit]
                    if new_clause:
                        new_circuit.append(new_clause)
            return new_circuit
        if propagate(literal):
            if dpll(new_circuit):
                return True
        if propagate(-literal):
            if dpll(new_circuit):
                return True
        return False
    
    def monotone_complexity(circuit):
        return len([l for l in range(1, len(circuit) + 1) if any(l in clause or -l in clause for clause in circuit)])
    
    def integer_valued_quasi_crystal(circuit):
        n = len(circuit)
        lattice_points = []
        for i in range(n):
            for j in range(i + 1, n):
                if all((circuit[i][0] > 0 and circuit[j][0] < 0) or (circuit[i][0] < 0 and circuit[j][0] > 0) for clause in circuit):
                    lattice_points.append((i, j))
        return len(lattice_points)
    
    n = random.randint(5, 40)
    circuit = []
    for _ in range(n * (n - 1) // 2):
        if random.random() < 0.5:
            literal = random.randint(1, n)
        else:
            literal = -random.randint(1, n)
        clause = [literal]
        while random.random() < 0.8:
            if random.random() < 0.5:
                literal = random.randint(1, n)
            else:
                literal = -random.randint(1, n)
            if literal not in clause and -literal not in clause:
                clause.append(literal)
        circuit.append(clause)
    
    mc = monotone_complexity(circuit)
    o_qc = integer_valued_quasi_crystal(circuit)
    
    return {
        "metric_name": "Order of Integer-Valued Quasi-Crystal",
        "metric_value": o_qc,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(o_qc - mc) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(x) for x in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")