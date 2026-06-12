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
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def truth_table(cnf: list):
        n = max(abs(lit) for cl in cnf for lit in cl)
        tt = [[False] * (2 ** n) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for j in range(2 ** n):
                if all((j >> abs(lit) - 1) & 1 == 1 if lit > 0 else (j >> abs(lit) - 1) & 1 == 0 for lit in clause):
                    tt[i][j] = True
        return tt
    
    def quantum_entanglement(tt: list):
        n = len(tt[0])
        entangled_qubits = 0
        for i in range(n):
            if all(row[j] == row[j + 1] for j in range(0, n - 1, 2)):
                entangled_qubits += 1
        return entangled_qubits
    
    def frege_proof_depth(cnf: list):
        # Placeholder function; actual implementation needed
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            tt = truth_table(cnf)
            entanglement = quantum_entanglement(tt)
            depth = frege_proof_depth(cnf)
            results.append((entanglement, depth))
    
    if not results:
        return {
            "metric_name": "QuantumEntanglement",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglements = [r[0] for r in results]
    depths = [r[1] for r in results]
    correlation_coefficient = sum((entanglement - mean(entanglements)) * (depth - mean(depths)) for entanglement, depth in results) / (len(results) * stdev(entanglements) * stdev(depths))
    
    return {
        "metric_name": "QuantumEntanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,  # Arbitrary threshold
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def stdev(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = mean([r["metric_value"] for r in results])
        std_value = stdev([r["metric_value"] for r in results])
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")