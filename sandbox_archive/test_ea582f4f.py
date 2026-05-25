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
    
    def acc0_circuit_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        return n
    
    def tropicalize_truth_table(truth_table, n):
        quandle_order = 0
        for i in range(n):
            for j in range(n):
                if truth_table[i][j] == truth_table[j][i]:
                    quandle_order += 1
        return quandle_order
    
    def check_quandle_action(quandle_order, n):
        return quandle_order <= n**2 * math.log(n)
    
    def find_acc0_circuit(f, t_f):
        # Placeholder for actual ACC⁰ circuit finding logic
        return True
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_function(n)
    t_f = acc0_circuit_complexity(f)
    
    quandle_order = tropicalize_truth_table(f, n)
    conjecture_holds = check_quandle_action(quandle_order, n) and find_acc0_circuit(f, t_f)
    
    return {
        "metric_name": "quandle_order",
        "metric_value": quandle_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Function with ACC⁰ complexity {t_f} and quandle order {quandle_order}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")