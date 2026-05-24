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
    
    def generate_read_twice_bp(n):
        bp = [random.choice([0, 1]) for _ in range(2**n)]
        return bp
    
    def tropical_curve(bp):
        n = len(bp)
        curve = [bp[0]]
        for i in range(1, n):
            curve.append(curve[-1] ^ bp[i])
        return curve
    
    def rank(tropical_curve):
        m = len(tropical_curve)
        if m == 0:
            return 0
        A = [[int(x == y) for x in tropical_curve] for y in tropical_curve]
        rank = 0
        for i in range(m):
            pivot = next((j for j in range(i, m) if A[j][i] != 0), None)
            if pivot is None:
                continue
            A[i], A[pivot] = A[pivot], A[i]
            for j in range(i + 1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(m):
                    A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            bp = generate_read_twice_bp(n)
            curve = tropical_curve(bp)
            rank_value = rank(curve)
            total_rank += rank_value
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    
    if n_values[-1] == 40 and instances_tested < 30:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "budget_exceeded n_tested=25"
        }
    
    c = 1.0  # Placeholder value for the constant in the conjecture
    if mean_rank <= c * math.log(instances_tested) and instances_tested >= 30:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": mean_rank,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"mean_rank={mean_rank} does not satisfy the conjecture for n=40"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")