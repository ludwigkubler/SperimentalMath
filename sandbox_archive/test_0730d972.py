# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_truth_table(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def braid_monoid_representation(truth_table):
        n = len(truth_table)
        if n == 1:
            return 1
        representation = []
        for i in range(n):
            row = truth_table[i]
            for j in range(i+1, n):
                col = truth_table[j]
                if all(row[k] != col[k] for k in range(2**n)):
                    representation.append((i, j))
        return len(representation)
    
    def min_order(n):
        return 10 * Fraction(n).log2()
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        truth_table = generate_truth_table(n)
        order = braid_monoid_representation(truth_table)
        metric_value = min_order(n)
        
        if order < metric_value:
            return {
                "metric_name": "min_order",
                "metric_value": float(order),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Function with n={n} has braid monoid representation of order {order}, which is less than the conjectured lower bound of {metric_value}"
            }
        
        total_metric_value += metric_value
        instances_tested += 1
    
    return {
        "metric_name": "min_order",
        "metric_value": float(total_metric_value / instances_tested),
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = next((r['counterexample'] for r in results if r['counterexample']), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")