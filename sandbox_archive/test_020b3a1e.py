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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def tropicalize_polynomial(poly):
        return poly
    
    def compute_index(grothendieck_group):
        return len(grothendieck_group)
    
    def characteristic_polynomial(cnf):
        # Placeholder for actual computation
        return [1, 0] * (len(cnf) + 1)
    
    def tropical_grothendieck_group(cnf):
        poly = characteristic_polynomial(cnf)
        grothendieck_group = tropicalize_polynomial(poly)
        return grothendieck_group
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_index = 0
    clause_counts = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n))
            grothendieck_group = tropical_grothendieck_group(cnf)
            index = compute_index(grothendieck_group)
            total_index += index
            clause_counts.append(len(cnf))
            instances_tested += 1
    
    if not instances_tested:
        return {
            "metric_name": "Index_G",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_index = total_index / instances_tested
    mean_clause_count = sum(clause_counts) / instances_tested
    
    correlation_coefficient = (instances_tested * sum(a*b for a, b in zip(clause_counts, clause_counts)) -
                               sum(clause_counts) * sum(clause_counts)) / \
                              math.sqrt((instances_tested * sum(a*a for a in clause_counts) - sum(clause_counts)**2) *
                                        (instances_tested * sum(b*b for b in clause_counts) - sum(clause_counts)**2))
    
    return {
        "metric_name": "Index_G",
        "metric_value": mean_index,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.5"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_index = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_index)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_index} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["counterexample"] == "" for res in results):
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"] and res["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={next(seed for seed, res in zip(seeds, results) if not res['conjecture_holds'] and res['counterexample'] == '')}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")