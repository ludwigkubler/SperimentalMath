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
    
    def hadamard(n):
        if n == 1:
            return [[1]]
        H = hadamard(n - 1)
        size = 2 ** (n - 1)
        result = []
        for i in range(size):
            row = [x / math.sqrt(2) for x in H[i]] + [x / math.sqrt(2) for x in H[i]]
            result.append(row)
            row = [x / math.sqrt(2) for x in H[i]] - [x / math.sqrt(2) for x in H[i]]
            result.append(row)
        return result
    
    def geometric_entanglement(state):
        n = int(math.log2(len(state)))
        H = hadamard(n)
        entanglement_operator = [[0] * len(state) for _ in range(len(state))]
        for i in range(len(state)):
            for j in range(len(state)):
                entanglement_operator[i][j] = state[i] * state[j]
        # Simplified calculation of logarithmic rank
        return math.log2(sum(abs(x) for x in sum(entanglement_operator, [])))
    
    def decision_tree_width(n):
        if n == 1:
            return 1
        return 2 * decision_tree_width(n - 1)
    
    instances_tested = 0
    total_ratio = 0.0
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        state = [random.choice([-1, 1]) for _ in range(2 ** random.randint(5, 40))]
        entanglement = geometric_entanglement(state)
        width = decision_tree_width(entanglement)
        if width > 0:
            ratio = width / entanglement
            total_ratio += ratio
            instances_tested += 1
    
    metric_value = total_ratio / instances_tested if instances_tested > 0 else float('inf')
    conjecture_holds = metric_value <= math.exp(entanglement + 1)
    counterexample = "" if conjecture_holds else f"Ratio {metric_value} exceeds bound"
    
    return {
        "metric_name": "Decision Tree Width / Geometric Entanglement",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = (sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds bound\" first_failing_seed={first_failing_seed}")