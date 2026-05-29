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
    
    def generate_3cnf(n, clause_density):
        m = int(clause_density * n * (n - 1) / 2)
        clauses = set()
        while len(clauses) < m:
            u, v = random.sample(range(1, n + 1), 2)
            polarity_u = random.choice([True, False])
            polarity_v = random.choice([True, False])
            clause = (u if polarity_u else -u, v if polarity_v else -v)
            clauses.add(clause)
        return clauses
    
    def resolution_refutation_size(clauses):
        # Simplified version of resolution refutation size calculation
        return len(clauses) * 2
    
    def minimal_local_homology_rank(clauses):
        # Placeholder for local homology rank calculation
        return len(clauses)
    
    n_values = [10, 15, 20, 25]
    results = []
    
    for n in n_values:
        for _ in range(30):  # Ensure at least 30 instances per seed
            clauses = generate_3cnf(n, random.choice([0.5, 1, 2]))
            t_F = resolution_refutation_size(clauses)
            f_n = minimal_local_homology_rank(clauses)
            results.append((n, math.log2(f_n), t_F))
    
    if not results:
        return {
            "metric_name": "log2_f(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result[0] for result in results)
    if n_max < 16:
        return {
            "metric_name": "log2_f(n)",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    log2_f_n_values = [result[1] for result in results]
    t_F_values = [result[2] for result in results]
    
    mean_log2_f_n = sum(log2_f_n_values) / len(log2_f_n_values)
    std_log2_f_n = math.sqrt(sum((x - mean_log2_f_n) ** 2 for x in log2_f_n_values) / len(log2_f_n_values))
    correlation_coefficient = sum((log2_f_n_values[i] - mean_log2_f_n) * (t_F_values[i] - mean_t_F) for i in range(len(log2_f_n_values))) / (len(log2_f_n_values) * std_log2_f_n * std_t_F)
    
    return {
        "metric_name": "log2_f(n)",
        "metric_value": mean_log2_f_n,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.8 and max(log2_f_n_values) <= max(t_F_values),
        "counterexample": "" if correlation_coefficient > 0.8 and max(log2_f_n_values) <= max(t_F_values) else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "correlation_too_low" for r in results):
        print("RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")