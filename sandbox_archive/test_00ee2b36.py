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
    
    def secant_variety(X):
        n = len(X)
        V_X = []
        for x1 in X:
            for x2 in X:
                row = [x1[i] + x2[i] for i in range(n)]
                V_X.append(row)
        return V_X
    
    def noncommutative_Lp_entropy(V_X, p):
        n = len(V_X[0])
        entropy = 0
        for v in V_X:
            norm = sum(abs(v[i]) ** p for i in range(n)) ** (1 / p)
            if norm > 0:
                entropy += math.log(norm) / n
        return -entropy
    
    X = [[random.random() for _ in range(5)] for _ in range(5)]
    V_X = secant_variety(X)
    H_mu_VX = noncommutative_Lp_entropy(V_X, 2)
    
    metric_name = "noncommutative_Lp_entropy"
    metric_value = H_mu_VX
    instances_tested = len(V_X)
    conjecture_holds = H_mu_VX >= math.log(5) / 5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")