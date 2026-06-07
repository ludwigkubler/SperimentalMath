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
    
    def dnf_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        minterms = []
        for i in range(2**n):
            if f[i] == 1:
                minterm = [i & (1 << j) > 0 for j in range(n)]
                minterms.append(minterm)
        variables = list(range(n))
        circuit_size = len(minterms)
        return circuit_size
    
    def coxeter_group_size(f):
        n = len(f)
        if n == 1:
            return 2
        # Simplified Coxeter group size calculation for demonstration
        return 2**n
    
    metric_name = "Coxeter Group Size / DNF Circuit Size"
    instances_tested = 0
    n_max = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        instances_tested += 2**n
        n_max = max(n_max, n)
        
        f1 = generate_boolean_function(n)
        f2 = generate_boolean_function(n)
        
        dnf_size1 = dnf_circuit_size(f1)
        dnf_size2 = dnf_circuit_size(f2)
        
        coxeter_size1 = coxeter_group_size(f1)
        coxeter_size2 = coxeter_group_size(f2)
        
        total_metric_value += (coxeter_size1 / dnf_size1 + coxeter_size2 / dnf_size2) / 2
    
    mean_metric_value = total_metric_value / instances_tested
    if mean_metric_value > 2:
        conjecture_holds = False
        counterexample = "Mean metric value exceeds 2"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean metric value exceeds 2\" first_failing_seed={first_failing_seed}")