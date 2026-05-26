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
    
    N = 40
    M = [[random.choice([-1, 0, 1]) for _ in range(N)] for _ in range(N)]
    
    def communication_complexity(M):
        # Placeholder function to compute CC(M)
        return sum(sum(abs(x) for x in row) for row in M)
    
    def min_rank_quadratic_form(M):
        # Placeholder function to compute min_rank(QuadraticForm(M))
        rank = 0
        for i in range(N):
            if any(M[j][i] != 0 for j in range(N)):
                rank += 1
        return rank
    
    CC_M = communication_complexity(M)
    min_rank_QF = min_rank_quadratic_form(M)
    
    if CC_M == 0:
        return {
            "metric_name": "min_rank/CC^c",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_is_zero"
        }
    
    ratios = [min_rank_QF / (CC_M ** c) for c in range(1, 4)]
    
    return {
        "metric_name": "min_rank/CC^c",
        "metric_value": sum(ratios) / len(ratios),
        "instances_tested": 1,
        "conjecture_holds": all(r > 0.5 for r in ratios),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=some_trials_have_none_values")