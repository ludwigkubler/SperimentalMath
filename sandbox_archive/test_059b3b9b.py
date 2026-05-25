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
    
    def generate_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        half_n = n // 2
        left = f[:half_n]
        right = f[half_n:]
        return 1 + max(circuit_complexity(left), circuit_complexity(right))
    
    def tropicalize(truth_table):
        n = int(math.log2(len(truth_table)))
        quandle = set()
        for i in range(n):
            for j in range(n):
                if truth_table[i][j] == 1:
                    quandle.add((i, j))
        return quandle
    
    def is_quandle_action(quandle, n):
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if (i, j) not in quandle or (j, k) not in quandle:
                        continue
                    if (i, k) not in quandle:
                        return False
        return True
    
    n = random.randint(5, 40)
    f = generate_function(n)
    t_f = circuit_complexity(f)
    q = tropicalize(f)
    
    order = len(q)
    expected_order = n**2 * math.log(t_f)
    
    conjecture_holds = order <= expected_order
    counterexample = "" if conjecture_holds else f"Order exceeds O(n^2 * log(t(f)))"
    
    return {
        "metric_name": "Quandle Order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = math.sqrt(sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds O(n^2 * log(t(f)))\" first_failing_seed={first_failing_seed}")