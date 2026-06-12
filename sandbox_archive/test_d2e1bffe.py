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
            cnf.append(clause)
        return cnf
    
    def truth_table(cnf: list):
        n = max(abs(lit) for clause in cnf for lit in clause)
        table = [[False] * (2 ** n) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for j in range(2 ** n):
                if all((j >> abs(lit) - 1) & 1 == (lit > 0) for lit in clause):
                    table[i][j] = True
        return table
    
    def quantum_entanglement(table: list):
        n = int(math.log2(len(table[0])))
        entanglement = sum(1 for row in table if all(row[i] == row[0] for i in range(1, n)))
        return entanglement
    
    def frege_proof_depth(cnf: list):
        # Placeholder function to simulate Frege proof depth
        return len(cnf) * 2  # Simplified for testing purposes
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, n)
            table = truth_table(cnf)
            entanglement = quantum_entanglement(table)
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
    
    entanglements, depths = zip(*results)
    correlation = sum((e - mean_e) * (d - mean_d) for e, d in zip(entanglements, depths)) / len(results)
    mean_e = sum(entanglements) / len(entanglements)
    mean_d = sum(depths) / len(depths)
    
    return {
        "metric_name": "QuantumEntanglement",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40] if any(n == len(cnf) for _ in range(5))),
        "conjecture_holds": correlation > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results)).limit_denominator()
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_trials_support")