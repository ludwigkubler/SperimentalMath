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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        cc = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    cc += 1
        return cc
    
    def quasi_morphism_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        while True:
            found = False
            for i in range(2**n):
                if f[i] == 1:
                    found = True
                    break
            if not found:
                return rank
            rank += 1
            f = [f[i] ^ f[2*i] for i in range(2**(n-1))]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(30):
            f = generate_boolean_function(n)
            cc = communication_complexity(f)
            r = quasi_morphism_rank(f)
            results.append((n, cc, r))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(n for n, _, _ in results)
    instances_tested = len(results)
    
    cc_values = [cc for _, cc, _ in results]
    r_values = [r for _, _, r in results]
    
    mean_cc = sum(cc_values) / instances_tested
    mean_r = sum(r_values) / instances_tested
    
    correlation_coefficient = (sum((cc - mean_cc) * (r - mean_r) for cc, r in zip(cc_values, r_values)) /
                                math.sqrt(sum((cc - mean_cc)**2 for cc in cc_values) *
                                          sum((r - mean_r)**2 for r in r_values)))
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(abs(cc - r) <= 10 for cc, r in zip(cc_values, r_values))
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or |cc - r| > 10"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and all(abs(r["metric_value"] - 0.8) <= 10 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")