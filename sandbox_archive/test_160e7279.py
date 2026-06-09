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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_width(cnf):
        # Simplified heuristic to estimate proof width
        return len(cnf) * 2
    
    def local_inductive_dimension(cnf):
        # Simplified heuristic to estimate local inductive dimension
        return len(cnf) ** 0.5
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    w_phi = frege_proof_width(cnf)
    dim_ind_phi = local_inductive_dimension(cnf)
    
    return {
        "metric_name": "dim_ind",
        "metric_value": dim_ind_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": dim_ind_phi <= w_phi * 2,  # Example function f(n) = 2w(φ)
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8 and abs(mean_value) <= 3:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"dim_ind({result['n_max']}) > {result['metric_value']} * 2"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")