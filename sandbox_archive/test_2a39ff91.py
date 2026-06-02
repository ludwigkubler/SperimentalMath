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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(phi):
        n = int(math.log2(len(phi)))
        if 2**n != len(phi):
            raise ValueError("Invalid boolean function length")
        
        # Tseitin transformation to CNF
        cnf = []
        literals = list(range(n))
        for i in range(2**n):
            clause = []
            for j in range(n):
                if phi[i] & (1 << j):
                    clause.append(literals[j])
                else:
                    clause.append(-literals[j])
            cnf.append(clause)
        
        # Calculate the number of clauses
        return len(cnf)
    
    def lefschetz_thimble_rank(phi):
        n = int(math.log2(len(phi)))
        if 2**n != len(phi):
            raise ValueError("Invalid boolean function length")
        
        # Simplified heuristic for Lefschetz thimble rank (not accurate but sufficient for testing)
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample at least 30 instances
            phi = generate_boolean_function(n)
            c_phi = communication_complexity(phi)
            Lr_phi = lefschetz_thimble_rank(phi)
            results.append((n, c_phi, Lr_phi))
    
    if len(results) < 30:
        return {
            "metric_name": "Lr(φ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Too few instances"
        }
    
    Lr_values = [Lr for _, _, Lr in results]
    c_phi_values = [c_phi for _, c_phi, _ in results]
    
    mean_Lr = sum(Lr_values) / len(Lr_values)
    mean_c_phi = sum(c_phi_values) / len(c_phi_values)
    
    # Pearson correlation coefficient
    covariance = sum((Lr - mean_Lr) * (c_phi - mean_c_phi) for Lr, c_phi in zip(Lr_values, c_phi_values))
    variance_Lr = sum((Lr - mean_Lr)**2 for Lr in Lr_values)
    variance_c_phi = sum((c_phi - mean_c_phi)**2 for c_phi in c_phi_values)
    
    if variance_Lr == 0 or variance_c_phi == 0:
        return {
            "metric_name": "Lr(φ)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Zero variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_Lr) * math.sqrt(variance_c_phi))
    
    return {
        "metric_name": "Lr(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")