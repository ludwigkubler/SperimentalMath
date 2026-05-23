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
    
    def geometric_entanglement(n):
        # Simulate a quantum state with n qubits
        E = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    E[i][j] = 1 / (2 ** i)
                else:
                    E[i][j] = 1 / (2 ** (i + j))
        return E
    
    def decision_tree_width(E):
        # Simulate the construction of a monotone XOR circuit
        n = len(E)
        width = 0
        for i in range(n):
            for j in range(i, n):
                if E[i][j] > 0:
                    width += 1
        return width
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, mean_val):
        return math.sqrt(sum((x - mean_val) ** 2 for x in lst) / len(lst))
    
    n = random.randint(5, 40)
    E = geometric_entanglement(n)
    width = decision_tree_width(E)
    
    metric_name = "Decision Tree Width vs Geometric Entanglement"
    metric_value = width
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
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
    
    mean_value = mean([r["metric_value"] for r in results])
    std_value = std([r["metric_value"] for r in results], mean_value)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")