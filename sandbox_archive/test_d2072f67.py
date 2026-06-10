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
            if all(v == 0 for v in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def cnf_to_category(cnf):
        variables = set(abs(lit) for lit in sum(cnf, []))
        morphisms = {}
        for var in variables:
            morphisms[var] = {var: 1}
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    lit_i, lit_j = clause[i], clause[j]
                    abs_lit_i, abs_lit_j = abs(lit_i), abs(lit_j)
                    if (abs_lit_i, abs_lit_j) not in morphisms:
                        morphisms[(abs_lit_i, abs_lit_j)] = {}
                    if (abs_lit_j, abs_lit_i) not in morphisms:
                        morphisms[(abs_lit_j, abs_lit_i)] = {}
                    morphisms[(abs_lit_i, abs_lit_j)][(abs_lit_j, abs_lit_i)] = 1
        return morphisms
    
    def count_morphisms(morphisms):
        return sum(sum(v.values()) for v in morphisms.values())
    
    def circuit_size(cnf):
        return len(cnf) * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        category = cnf_to_category(cnf)
        morphisms_count = count_morphisms(category)
        circuit_size_value = circuit_size(cnf)
        results.append((n, morphisms_count, circuit_size_value))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    morphisms_values = [r[1] for r in results]
    circuit_size_values = [r[2] for r in results]
    mean_morphisms = sum(morphisms_values) / len(morphisms_values)
    mean_circuit_size = sum(circuit_size_values) / len(circuit_size_values)
    
    correlation_coefficient = sum((m - mean_morphisms) * (c - mean_circuit_size) for m, c in zip(morphisms_values, circuit_size_values)) / (len(results) * math.sqrt(sum((m - mean_morphisms)**2 for m in morphisms_values) * sum((c - mean_circuit_size)**2 for c in circuit_size_values)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")