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
    
    def generate_random_sat_instance(n, d):
        clauses = []
        for _ in range(d):
            clause = [random.randint(1, n), -random.randint(1, n)]
            while clause[0] == -clause[1]:
                clause[1] = -random.randint(1, n)
            clauses.append(clause)
        return clauses
    
    def truth_table_to_diophantine(clauses):
        n = len(clauses) + 1
        binary = [str(random.choice([0, 1])) for _ in range(n)]
        if all(binary[j-1] == '1' or c * int(binary[abs(c)-1]) >= 0 for j, c in enumerate(clauses)):
            return sum(int(b) * (2 ** i) for i, b in enumerate(reversed(binary)))
        else:
            return None
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return covariance / (std_dev_x * std_dev_y)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(1, n)
        clauses = generate_random_sat_instance(n, d)
        diophantine_exponent = truth_table_to_diophantine(clauses)
        if diophantine_exponent is not None:
            results.append((d, diophantine_exponent))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    d_values = [d for d, _ in results]
    e_values = [e for _, e in results]
    correlation_coefficient = pearson_correlation(d_values, e_values)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(abs(e - math.log(n)**2 * d) <= 3 for d, e in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        all_results.append(trial_result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in all_results):
        mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
        support_fraction = sum(1 for r in all_results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(all_results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in all_results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_support")