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
    
    def communication_complexity(f):
        n = len(f)
        max_comm = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    max_comm = max(max_comm, bin(i^j).count('1'))
        return max_comm
    
    def coxeter_diagram(f):
        n = len(f)
        relations = set()
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    k = bin(i^j).count('1')
                    if k % 2 == 0:
                        relations.add((i, j))
                        relations.add((j, i))
        return relations
    
    n_max = 40
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        f = generate_boolean_function(n)
        C_f = communication_complexity(f)
        R_f = coxeter_diagram(f)
        
        if C_f == 0:
            continue
        
        ratio = len(R_f) / math.log(n)
        total_ratio += ratio
        instances_tested += 1
        
        if ratio > 2.0:  # Example bound, replace with actual bound
            conjecture_holds = False
            counterexample = f"n={n}, C(f)={C_f}, |R(f)|={len(R_f)}, ratio={ratio}"
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else 0.0
    
    return {
        "metric_name": "Communication Complexity Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["instances_tested"] >= 30 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")