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
    
    def monodromy_group_order(f):
        n = len(f)
        if n == 1:
            return 1
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                M[i][j] = f[(i ^ j) % n]
        order = 1
        while True:
            found = False
            for i in range(2**n):
                if any(M[i][j] != M[j][i] for j in range(2**n)):
                    break
            else:
                return order
            for i in range(2**n):
                if any(M[i][j] != 0 for j in range(2**n)):
                    found = True
                    for j in range(2**n):
                        M[j][:] = [M[(i ^ j) % n][k] for k in range(2**n)]
                    break
            if not found:
                return order
            order += 1
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            rank += sum(1 for j in range(i+1, n) if f[i] != f[j])
        return rank
    
    c = 0.5  # Example constant, adjust as needed
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        order = monodromy_group_order(f)
        rank = communication_complexity_rank(f)
        
        if order < math.ceil(n**c * math.log(n)):
            conjecture_holds = False
            counterexample = "Monodromy group order too small"
        if rank != n**c * math.log(n):
            conjecture_holds = False
            counterexample = "Communication complexity rank incorrect"
    
    return {
        "metric_name": "monodromy_group_order",
        "metric_value": sum(monodromy_group_order(generate_boolean_function(random.randint(5, 40))) for _ in range(10)) / 10,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break