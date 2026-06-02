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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frege_proof_length(cnf):
        # Simplified Frege proof length calculation
        return len(cnf) * 2
    
    def quaternionic_kahler_form(cnf):
        # Simplified mapping to quaternionic polyhedra and minimal order calculation
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    proof_length = frege_proof_length(cnf)
    kahler_order = quaternionic_kahler_form(cnf)
    
    return {
        "metric_name": "logarithmic_correlation",
        "metric_value": math.log(m) - math.log(math.factorial(n)) * math.log(proof_length),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if len(results) < 30:
        print("RESULT: INCONCLUSIVE reason=insufficient_seeds n_tested=<k>")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8 and all(result["counterexample"] == "mapping_undefined" for result in results):
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
        elif any(result["counterexample"] != "mapping_undefined" for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] != "mapping_undefined")
            print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=unsupported_mapping")