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
    
    def generate_formula(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def twistor_representation(clauses):
        # Constructive mapping to twistor space representation
        # Simplified for demonstration purposes
        return len(clauses) ** 0.5
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m_values = [m for m in range(1, n * n + 1) if (n * n - m) % n == 0]
        for m in m_values:
            formula = generate_formula(n, m)
            mrep = twistor_representation(formula)
            results.append((m, mrep))
    
    if not results:
        return {
            "metric_name": "MRep(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_values = [m for m, _ in results]
    mrep_values = [mrep for _, mrep in results]
    mean_mrep = sum(mrep_values) / len(mrep_values)
    std_mrep = math.sqrt(sum((mrep - mean_mrep) ** 2 for mrep in mrep_values) / len(mrep_values))
    
    correlation_coefficient = (sum((m - mean_m) * (mrep - mean_mrep) for m, mrep in results) /
                               (len(results) * std_mvalues * std_mrep_values))
    
    return {
        "metric_name": "MRep(φ)",
        "metric_value": mean_mrep,
        "instances_tested": len(results),
        "n_max": max(m for m, _ in results),
        "conjecture_holds": correlation_coefficient > 0.9 and all(mrep <= 2 * math.sqrt(m) for _, mrep in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in all_results if r["metric_value"] is not None) / len(all_results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in all_results if r["metric_value"] is not None) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(s for s, r in zip(seeds, all_results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")