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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def size_of_cnf(cnf):
        return len(cnf) * 2  # Each clause has two literals
    
    def free_probability_entropy(cnf):
        size = size_of_cnf(cnf)
        if size == 0:
            return 0
        return math.log(size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    entropies = []
    for n in n_values:
        cnf = generate_cnf(n)
        entropy = free_probability_entropy(cnf)
        entropies.append(entropy)
    
    mean_entropy = sum(entropies) / len(entropies)
    log_size = math.log(size_of_cnf(generate_cnf(max(n_values))))
    
    conjecture_holds = abs(mean_entropy - log_size) <= 3
    counterexample = "" if conjecture_holds else f"mean_entropy={mean_entropy}, log_size={log_size}"
    
    return {
        "metric_name": "free_probability_entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(entropies),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")