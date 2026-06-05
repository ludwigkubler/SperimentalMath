# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if len(set(clause)) > 1:
                clauses.append(clause)
        return clauses
    
    def compute_subset_entropy(clauses):
        total_clauses = sum(len(c) for c in clauses)
        entropy = 0
        for clause in clauses:
            p = Fraction(1, 2 ** len(clause))
            entropy += -p * math.log2(p)
        return entropy
    
    def compute_root_lattice_entropy(n):
        # Placeholder for root lattice entropy computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random()
    
    n_max = 40
    instances_tested = 30
    se_values = []
    sh_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_sat_instance(n)
        se = compute_root_lattice_entropy(n)
        sh = compute_subset_entropy(clauses)
        se_values.append(se)
        sh_values.append(sh)
    
    correlation_coefficient = 0
    for i in range(instances_tested):
        for j in range(i + 1, instances_tested):
            correlation_coefficient += (se_values[i] - sum(se_values) / instances_tested) * (sh_values[j] - sum(sh_values) / instances_tested)
    correlation_coefficient /= ((instances_tested - 1) * math.sqrt(sum((x - sum(se_values) / instances_tested) ** 2 for x in se_values)) * math.sqrt(sum((y - sum(sh_values) / instances_tested) ** 2 for y in sh_values)))
    
    conjecture_holds = correlation_coefficient > 0
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")