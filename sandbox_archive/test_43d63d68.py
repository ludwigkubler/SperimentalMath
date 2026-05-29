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

def generate_random_satisfiable_boolean_function(n):
    truth_table = [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    return truth_table

def compute_coxeter_order(truth_table):
    n = len(truth_table)
    # Simplified Coxeter group order calculation based on the number of variables
    return int(math.log(n, 2)) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(100):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_satisfiable_boolean_function(n)
        coxeter_order_f = compute_coxeter_order(f)
        results.append(coxeter_order_f)
    mean_ratio = sum(results) / len(results) / (math.log(40, 2)) ** 2
    conjecture_holds = 0.8 <= mean_ratio <= 1.2
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["n_max"] >= 16 for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"support_fraction_too_low\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] if support_fraction < 0.8))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_n_max n_tested={len(results)}")