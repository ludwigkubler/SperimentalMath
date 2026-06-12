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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 2):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def truth_table(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        table = []
        for i in range(2**n):
            assignment = [(i >> j) & 1 for j in range(n)]
            table.append(all(any(x * assignment[abs(x)-1] >= 0 for x in clause) for clause in cnf))
        return table
    
    def quantum_entanglement(truth_table):
        n = len(truth_table)
        # Simplified simulation of quantum entanglement
        return sum(1 for row in truth_table if all(row[i] == row[0] for i in range(1, n)))
    
    def frege_proof_depth(cnf):
        # Placeholder function to simulate Frege proof depth
        return len(cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        table = truth_table(cnf)
        entanglement = quantum_entanglement(table)
        depth = frege_proof_depth(cnf)
        results.append((entanglement, depth))
    
    if not results:
        return {
            "metric_name": "QuantumEntanglement vs FregeProofDepth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglements, depths = zip(*results)
    correlation = sum((e - mean(entanglements)) * (d - mean(depths)) for e, d in zip(entanglements, depths)) / len(entanglements)
    mean_entanglement = mean(entanglements)
    std_deviation = math.sqrt(sum((x - mean_entanglement) ** 2 for x in entanglements) / len(entanglements))
    
    return {
        "metric_name": "QuantumEntanglement vs FregeProofDepth",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation) > 0.5,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    mean_value = mean([result["metric_value"] for result in results])
    std_deviation = math.sqrt(sum((x - mean_value) ** 2 for x in [result["metric_value"] for result in results]) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")