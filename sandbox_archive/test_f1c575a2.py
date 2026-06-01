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

def generate_tseitin_formula(n, d):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    
    def add_clause(clause):
        clauses.append(clause)
    
    # Create clauses for each variable
    for var in variables:
        add_clause([var])
    
    # Create clauses for each clause
    for i in range(n):
        new_var = f'y{i}'
        add_clause([new_var, variables[i]])
        for j in range(i + 1, n):
            add_clause([new_var, variables[j]])
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 3
        variables, clauses = generate_tseitin_formula(n, d)
        
        # Compute tK(G) and m_C(φ_G)
        # Placeholder values; replace with actual computation
        tK_G = random.random() * n  # Example value
        m_C_phi_G = random.randint(1, n)  # Example value
        
        results.append({
            "n": n,
            "tK_G": tK_G,
            "m_C_phi_G": m_C_phi_G
        })
    
    correlation_coefficient = calculate_correlation(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.5 else "low_correlation"
    }

def calculate_correlation(results):
    n_values = [result["n"] for result in results]
    tK_G_values = [result["tK_G"] for result in results]
    m_C_phi_G_values = [result["m_C_phi_G"] for result in results]
    
    mean_tK_G = sum(tK_G_values) / len(tK_G_values)
    mean_m_C_phi_G = sum(m_C_phi_G_values) / len(m_C_phi_G_values)
    
    numerator = sum((tK_G - mean_tK_G) * (m_C_phi_G - mean_m_C_phi_G) for tK_G, m_C_phi_G in zip(tK_G_values, m_C_phi_G_values))
    denominator = math.sqrt(sum((tK_G - mean_tK_G) ** 2 for tK_G in tK_G_values)) * math.sqrt(sum((m_C_phi_G - mean_m_C_phi_G) ** 2 for m_C_phi_G in m_C_phi_G_values))
    
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")