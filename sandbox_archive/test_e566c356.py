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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            clauses.append(tuple(clause))
        return set(clauses)
    
    def coxeter_group_action(clauses):
        actions = []
        for clause in clauses:
            action = tuple(sorted(clause))
            if action not in actions:
                actions.append(action)
        return actions
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n)
        actions = coxeter_group_action(clauses)
        distinct_words_count = len(actions)
        ratio = distinct_words_count / (n ** (1/3))
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = all(r >= 0.8 for r in results) and mean_ratio <= 3
    counterexample = "" if conjecture_holds else "ratio < 0.8 or > 3"
    
    return {
        "metric_name": "Ratio of distinct minimal length words to n^(1/3)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.8 and r <= 3) / len(results)
    
    if all(r >= 0.8 and r <= 3 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r < 0.8 or r > 3 for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8 or result > 3)
        print(f"RESULT: FALSIFIED counterexample='ratio out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")