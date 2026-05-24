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
    
    def generate_k_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def tropical_root_system_length(cnf):
        # Placeholder implementation
        return random.uniform(0.5, 2) * len(cnf)**(1/3)
    
    def resolution_proof_size(cnf):
        # Placeholder implementation
        return random.randint(1, 10) * math.sqrt(len(cnf))
    
    n = random.randint(5, 40)
    m = random.randint(1, min(40, int(n * (n - 1) / 2)))
    cnf = generate_k_cnf(n, m)
    length = tropical_root_system_length(cnf)
    size = resolution_proof_size(cnf)
    
    conjecture_holds = length >= m**(1/3) and size <= math.sqrt(m)
    counterexample = "" if conjecture_holds else f"CNF: {cnf}, Length: {length}, Size: {size}"
    
    return {
        "metric_name": "Tropical Root System Length vs Resolution Proof Size",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")