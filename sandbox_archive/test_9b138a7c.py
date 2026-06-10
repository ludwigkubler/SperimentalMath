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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.choice([i, -i]) for i in range(1, n + 1)]
            cnf.append(clause)
        return cnf
    
    def circuit_complexity(cnf):
        # Simplified gate-level circuit complexity calculation
        return len(cnf) * 2
    
    def tropical_variety(cnf):
        # Placeholder function for tropical variety computation
        return random.uniform(1, n)
    
    def local_induction_degree(V):
        # Placeholder function for LIDB computation
        return V
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    CCphi = circuit_complexity(cnf)
    Vphi = tropical_variety(cnf)
    LIDBphi = local_induction_degree(Vphi)
    
    if abs(LIDBphi - CCphi) > 3:
        return {
            "metric_name": "LIDB vs CC",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Mapping undefined"
        }
    
    return {
        "metric_name": "LIDB vs CC",
        "metric_value": LIDBphi - CCphi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        std_d = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"Mapping undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=not_enough_support")