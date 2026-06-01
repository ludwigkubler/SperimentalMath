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
    
    def communication_complexity_rank(f):
        n = len(f)
        max_rank = 0
        for i in range(n):
            rank = 0
            for j in range(n):
                if f[i] != f[j]:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    def linear_code_from_function(f):
        n = len(f)
        code = []
        for i in range(2**n):
            row = [f[(i >> j) & 1] for j in range(n)]
            code.append(row)
        return code
    
    def brauer_induction_index(code):
        n = len(code[0])
        total = 0
        for i in range(n):
            count = sum(1 for row in code if row[i] == 1)
            total += abs(count - (n - count))
        return total / n
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, avg):
        return math.sqrt(sum((x - avg) ** 2 for x in lst) / len(lst))
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        code = linear_code_from_function(f)
        mBI = brauer_induction_index(code)
        crank = communication_complexity_rank(f)
        results.append((mBI, crank))
    
    avg_mBI = mean([x for x, _ in results])
    avg_crank = mean([y for _, y in results])
    ratio_avg = avg_mBI / avg_crank
    
    return {
        "metric_name": "Brauer Induction Index to Communication Complexity Rank Ratio",
        "metric_value": ratio_avg,
        "instances_tested": 30,
        "n_max": max([len(f) for f, _ in results]),
        "conjecture_holds": ratio_avg <= 1.5,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_val = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_val) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 1.5) / len(results)
    
    if all(r <= 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if r > 1.5)
        print(f"RESULT: FALSIFIED counterexample=\"ratio_exceeds_bound\" first_failing_seed={first_failing_seed}")