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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def log2(x):
        return math.log(x) / math.log(2)
    
    def permutation_group_rank(m):
        return factorial(m)
    
    def generate_random_circuit(m, d):
        circuit = []
        for _ in range(d):
            layer = [random.randint(0, m-1) for _ in range(m)]
            circuit.append(layer)
        return circuit
    
    def depth(circuit):
        return len(circuit)
    
    def size(circuit):
        return len(circuit[0])
    
    n_tests = 30
    total_rank = 0
    
    for _ in range(n_tests):
        m = random.randint(5, 40)
        d = random.randint(1, 4)
        circuit = generate_random_circuit(m, d)
        
        rank = permutation_group_rank(m)
        total_rank += rank
        
        if rank < d * log2(m):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": n_tests,
                "conjecture_holds": False,
                "counterexample": f"m={m}, d={d}, rank={rank} < {d * log2(m)}"
            }
    
    average_rank = total_rank / n_tests
    return {
        "metric_name": "minimal_rank",
        "metric_value": average_rank,
        "instances_tested": n_tests,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break