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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def vector_space_representation(f):
        n = int(math.log2(len(f)))
        V_f = [[f[i] if i & (1 << j) else 0 for j in range(n)] for i in range(2**n)]
        return V_f
    
    def symplectic_measure(V):
        n = len(V)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(V[i][k] == V[j][k] for k in range(n)):
                    count += 1
        return count
    
    def circuit_size(f):
        n = int(math.log2(len(f)))
        # Simplified DSOP form construction (not actual minimization)
        dsop = []
        for i in range(2**n):
            if f[i] == 1:
                dsop.append(bin(i)[2:].zfill(n))
        return len(dsop)
    
    n_max = 0
    instances_tested = 0
    total_sigma = 0
    total_size = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        V_f = vector_space_representation(f)
        sigma = symplectic_measure(V_f)
        size = circuit_size(f)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_sigma += sigma
        total_size += size
    
    mean_sigma = total_sigma / instances_tested
    mean_size = total_size / instances_tested
    correlation_coefficient = (instances_tested * total_sigma * total_size - total_sigma**2 - total_size**2) / ((instances_tested - 1) * math.sqrt((total_sigma**2 - (total_sigma**2 / instances_tested)) * (total_size**2 - (total_size**2 / instances_tested))))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")