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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_curve(f):
        n = len(f)
        T_f = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    T_f[i][j] = 0
                else:
                    T_f[i][j] = math.inf
        return T_f
    
    def minimal_local_index(T_f):
        n = len(T_f) - 1
        mli = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if T_f[i][j] < math.inf:
                    mli += 1
        return mli
    
    def communication_complexity(f):
        # Simplified model: C(f) = n * log2(n)
        n = len(f)
        return n * math.log2(n)
    
    n_max = 40
    instances_tested = 30
    total_mli = 0
    total_Cf = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        T_f = compute_tropical_curve(f)
        mli = minimal_local_index(T_f)
        Cf = communication_complexity(f)
        
        total_mli += mli
        total_Cf += Cf
    
    mean_mli = total_mli / instances_tested
    mean_Cf = total_Cf / instances_tested
    support_fraction = sum(abs(mli - Cf) <= 3 for mli, Cf in zip(total_mli, total_Cf)) / instances_tested
    
    if any(abs(mli - Cf) > 10 for mli, Cf in zip(total_mli, total_Cf)):
        return {
            "metric_name": "mli_vs_Cf",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "C(f) and mli(f) differ by more than 10 for some f"
        }
    
    if support_fraction < 25 / 30:
        return {
            "metric_name": "mli_vs_Cf",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Less than 25/30 seeds support the conjecture"
        }
    
    return {
        "metric_name": "mli_vs_Cf",
        "metric_value": mean_mli / mean_Cf,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - 1) > 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if abs(r["metric_value"] - 1) > 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"mli(f) and C(f) differ by more than 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")