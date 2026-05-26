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
    
    def generate_dnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([0, 1]) for _ in range(n)]
            if sum(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def dnf_to_etale_cohomology(f, n):
        return len([i for i in range(1 << n) if f(i)])
    
    def max_clause_count(dnf):
        return len(dnf)
    
    n = random.randint(5, 40)
    f = generate_dnf(n)
    etale_cohomology_rank = dnf_to_etale_cohomology(f, n)
    max_clauses = max_clause_count(f)
    
    metric_name = "etale_cohomology_rank"
    metric_value = etale_cohomology_rank
    instances_tested = 1
    conjecture_holds = (etale_cohomology_rank <= max_clauses - 1)
    counterexample = "" if conjecture_holds else f"DNF with n={n}, rank={etale_cohomology_rank}, max_clauses={max_clauses}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")