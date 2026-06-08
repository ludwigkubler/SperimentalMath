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
from math import log, sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def truth_table_to_diophantine(clauses):
        n = len(clauses[0])
        table = [[0] * (2**n) for _ in range(len(clauses))]
        
        for i, clause in enumerate(clauses):
            for j in range(2**n):
                binary = [int(x) for x in format(j, f'0{n}b')]
                if all(binary[j-1] == 1 or c * binary[abs(c)-1] >= 0 for c in clause):
                    table[i][j] = 1
        
        return table
    
    def min_diophantine_exponent(table):
        n = len(table)
        m = len(table[0])
        
        # Gaussian elimination
        for i in range(n):
            if table[i][i] == 0:
                for j in range(i+1, n):
                    if table[j][i] != 0:
                        table[i], table[j] = table[j], table[i]
                        break
            if table[i][i] == 0:
                return float('inf')
            
            for j in range(n):
                if i != j:
                    factor = table[j][i] / table[i][i]
                    for k in range(m):
                        table[j][k] -= factor * table[i][k]
        
        # Count non-zero rows
        rank = sum(1 for row in table if any(row))
        return rank
    
    def clause_depth(clauses):
        return max(len(clause) for clause in clauses)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_instance(n)
            table = truth_table_to_diophantine(clauses)
            e_phi = min_diophantine_exponent(table)
            d_phi = clause_depth(clauses)
            results.append((e_phi, d_phi))
    
    if not results:
        return {
            "metric_name": "min_diophantine_exponent",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    e_values = [e for e, _ in results]
    d_values = [d for _, d in results]
    
    mean_e = sum(e_values) / len(e_values)
    std_e = (sum((x - mean_e)**2 for x in e_values) / len(e_values))**0.5
    
    correlation_coefficient = sum((e - mean_e) * (d - mean_d) for e, d in zip(e_values, d_values)) / (len(results) * std_e * sqrt(sum((d - mean_d)**2 for d in d_values)))
    
    return {
        "metric_name": "min_diophantine_exponent",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and all(abs(e - log(n)**2 * d) <= 3 for e, d in zip(e_values, d_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")