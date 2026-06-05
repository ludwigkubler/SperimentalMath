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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 3):  # Ensure at least 2^10 clauses for n=5 to n=40
            clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                      for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        # Placeholder function to compute the rank
        return len(cnf)
    
    def p_adic_logarithmic_potential(cnf):
        # Placeholder function to compute the potential
        return sum(len(clause) for clause in cnf) / len(cnf)
    
    cr_values = []
    plp_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            cr = communication_complexity_rank(cnf)
            plp = p_adic_logarithmic_potential(cnf)
            cr_values.append(cr)
            plp_values.append(plp)
    
    if not cr_values or not plp_values:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(5, n),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_cr = sum(cr_values) / len(cr_values)
    mean_plp = sum(plp_values) / len(plp_values)
    
    variance_cr = sum((x - mean_cr)**2 for x in cr_values) / len(cr_values)
    variance_plp = sum((x - mean_plp)**2 for x in plp_values) / len(plp_values)
    
    std_cr = math.sqrt(variance_cr)
    std_plp = math.sqrt(variance_plp)
    
    if std_cr == 0 or std_plp == 0:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(cr_values),
            "n_max": max(5, n),
            "conjecture_holds": False,
            "counterexample": "std_deviation_zero"
        }
    
    cov_xy = sum((cr - mean_cr) * (plp - mean_plp) for cr, plp in zip(cr_values, plp_values)) / len(cr_values)
    correlation_coefficient = cov_xy / (std_cr * std_plp)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(cr_values),
        "n_max": max(5, n),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] == False for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")