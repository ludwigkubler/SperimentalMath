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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance):
        if not instance:
            return 0
        if len(set(instance)) == 1:
            return 0
        var = random.choice(range(len(instance)))
        pos_clauses = [i for i in range(len(instance)) if instance[i] == 1]
        neg_clauses = [i for i in range(len(instance)) if instance[i] == 0]
        if len(pos_clauses) > len(neg_clauses):
            return 1 + dpll([instance[i] for i in pos_clauses])
        else:
            return 1 + dpll([instance[i] for i in neg_clauses])
    
    def p_adic_valuation_complexity(instance):
        valuations = set()
        for clause in instance:
            valuation = sum(2**i if bit == 1 else 0 for i, bit in enumerate(clause))
            valuations.add(valuation)
        return len(valuations)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_instance(n)
        dpll_path_length = dpll(instance)
        p_val_complexity = p_adic_valuation_complexity(instance)
        results.append({
            "n": n,
            "dpll_path_length": dpll_path_length,
            "p_val_complexity": p_val_complexity
        })
    
    if not results:
        return {
            "metric_name": "p-adic valuation complexity / DPLL path length ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_dpll_path_length = sum(r["dpll_path_length"] for r in results) / len(results)
    mean_p_val_complexity = sum(r["p_val_complexity"] for r in results) / len(results)
    ratio = mean_p_val_complexity / mean_dpll_path_length
    
    return {
        "metric_name": "p-adic valuation complexity / DPLL path length ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(ratio - math.log(len(results))) < 2 * math.log(len(results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=NOT_APPLICABLE support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")