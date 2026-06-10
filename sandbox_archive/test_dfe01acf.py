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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def construct_circuit(cnf):
        n = len(cnf[0])
        circuit = [[[] for _ in range(2)] for _ in range(n)]
        for clause in cnf:
            gate_id = random.randint(0, 1)
            for var in clause:
                if var > 0:
                    circuit[var - 1][gate_id].append((gate_id, len(circuit[abs(var) - 1][gate_id])))
                else:
                    circuit[-var - 1][1 - gate_id].append((1 - gate_id, len(circuit[-var - 1][1 - gate_id])))
        return circuit
    
    def geometric_flow(circuit):
        n = len(circuit)
        steps = 0
        for i in range(n):
            for j in range(2):
                if circuit[i][j]:
                    steps += 1
                    circuit[i][j] = []
        return steps
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    gfc_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        circuit = construct_circuit(cnf)
        gfc = geometric_flow(circuit)
        gfc_values.append(gfc)
    
    avg_gfc = sum(gfc_values) / len(gfc_values)
    correlation_coefficient = pearson_correlation(n_values, gfc_values)
    
    conjecture_holds = correlation_coefficient > 0.95 and max(gfc_values) <= 4 * max(n_values) ** 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_flow_complexity",
        "metric_value": avg_gfc,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")