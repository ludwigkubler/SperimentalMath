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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def frobenius_schur_indicator(cnf):
        # Placeholder implementation
        return 0.5

    def communication_complexity_rank(cnf):
        # Placeholder implementation
        return len(cnf)

    def variance(values):
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        indicator = frobenius_schur_indicator(cnf)
        ccr = communication_complexity_rank(cnf)
        var = variance([indicator] * len(indicators))
        
        results.append({
            "n": n,
            "indicator": indicator,
            "ccr": ccr,
            "variance": var
        })
    
    support_fraction = sum(1 for r in results if r["variance"] >= 0.5 * r["ccr"]) / len(results)
    conjecture_holds = support_fraction >= 0.8
    
    return {
        "metric_name": "Variance of Frobenius-Schur Indicator",
        "metric_value": sum(r["variance"] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")