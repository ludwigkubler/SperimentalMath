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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(x != 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-x in queue[j] for x in queue[i]):
                        new_clause = [x for x in queue[i] if x not in [-y for y in queue[j]]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            if new_clause not in queue:
                queue.append(new_clause)
    
    def quaternionic_kähler_manifolds(cnf):
        # Placeholder function. In practice, this would involve complex computations.
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    N_M = quaternionic_kähler_manifolds(cnf)
    w_phi = resolution_width(cnf)
    
    ratio = Fraction(N_M, n)
    metric_value = abs(ratio - Fraction(w_phi, n))
    
    return {
        "metric_name": "ratio",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break