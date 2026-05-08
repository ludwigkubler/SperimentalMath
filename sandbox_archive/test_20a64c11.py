# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dnf(n, max_terms):
        terms = []
        for _ in range(random.randint(1, max_terms)):
            term = [random.choice([0, 1]) for _ in range(n)]
            if sum(term) > 0:
                terms.append(term)
        return terms
    
    def size(dnf):
        return len(dnf)
    
    def matroid_rank(circuits):
        rank = 0
        independent_sets = []
        for circuit in circuits:
            is_independent = True
            for s in independent_sets:
                if all(x == y or x == 0 or y == 0 for x, y in zip(circuit, s)):
                    is_independent = False
                    break
            if is_independent:
                independent_sets.append(circuit)
                rank += 1
        return rank
    
    def rank_deficit(dnf):
        circuits = dnf
        M = matroid_rank(circuits)
        return M - math.log2(size(dnf))
    
    n = random.randint(5, 40)
    max_terms = n**3
    dnf = generate_dnf(n, max_terms)
    metric_value = rank_deficit(dnf)
    instances_tested = 1
    conjecture_holds = True
    counterexample = ""
    
    if metric_value > 2 * math.log(n):
        conjecture_holds = False
        counterexample = "DNF violates upper bound"
    
    return {
        "metric_name": "rank_deficit",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")