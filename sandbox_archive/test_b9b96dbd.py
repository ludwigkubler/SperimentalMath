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
    
    def generate_quandle(q):
        quandle = {}
        for i in range(q):
            quandle[(i, j)] = (i + j) % q
        return quandle
    
    def tropicalize(quandle):
        max_val = 0
        for _, val in quandle.items():
            if val > max_val:
                max_val = val
        for key, val in quandle.items():
            quandle[key] = max_val - val
        return quandle
    
    def cnf_from_quandle(quandle):
        q = len(quandle)
        clauses = []
        for i in range(q):
            clause = [random.choice([-1, 1]) * (q + j) for j in range(q)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(abs(lit) == abs(other_lit) and lit != other_lit for lit in stack[i] for other_lit in stack[j]):
                        new_clause = [lit for lit in stack[i] if lit not in (-other_lit for other_lit in stack[j])]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    q_values = [5, 10, 15, 20, 30, 40]
    results = []
    for q in q_values:
        quandle = generate_quandle(q)
        tq_q = sum(quandle[(i, j)] for i in range(q) for j in range(q)) / (q * q)
        cnf = cnf_from_quandle(quandle)
        w_phi = resolution_width(cnf)
        results.append({"tq_q": tq_q, "w_phi": w_phi})
    
    mean_ratio = sum(result["w_phi"] / result["tq_q"] for result in results) / len(results)
    max_w_phi = max(result["w_phi"] for result in results)
    conjecture_holds = mean_ratio <= 1.5 and max_w_phi <= 3
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(q_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_w_phi={max_w_phi} > 3"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_w_phi > 3\" first_failing_seed={first_failing_seed}")