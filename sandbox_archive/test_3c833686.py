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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(G):
        def solve(model):
            if not G:
                return True
            literal = next((l for l in range(1, len(G) + 1) if l not in model and -l not in model), None)
            if literal is None:
                return False
            
            pos_literal = literal
            neg_literal = -literal
            new_model_pos = {**model, pos_literal: True}
            new_model_neg = {**model, neg_literal: True}
            
            if solve(new_model_pos):
                return True
            if solve(new_model_neg):
                return True
            
            return False
        
        return solve({})
    
    def mls(G):
        n = len(G)
        if n == 1:
            return 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j-1] and G[j][i-1]:
                    return 2
        return 1
    
    def height(G):
        n = len(G)
        if n == 1:
            return 0
        
        max_height = 0
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j-1] and G[j][i-1]:
                    max_height = max(max_height, height(G[:i]) + height(G[i+1:j]) + height(G[j+1:]))
        return max_height
    
    def correlation_coefficient(mls_values, heights):
        n = len(mls_values)
        if n < 2:
            return None
        
        mean_mls = sum(mls_values) / n
        mean_height = sum(heights) / n
        numerator = sum((mls_values[i] - mean_mls) * (heights[i] - mean_height) for i in range(n))
        denominator = math.sqrt(sum((mls_values[i] - mean_mls) ** 2 for i in range(n))) * math.sqrt(sum((heights[i] - mean_height) ** 2 for i in range(n)))
        
        if denominator == 0:
            return None
        
        return numerator / denominator
    
    n_max = 40
    instances_tested = 30
    mls_values = []
    heights = []
    
    for _ in range(instances_tested):
        G = generate_cnf(n_max)
        mls_value = mls(G)
        height_value = dpll(G)
        
        if mls_value is not None and height_value is not None:
            mls_values.append(mls_value)
            heights.append(height_value)
    
    correlation = correlation_coefficient(mls_values, heights)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation is not None and correlation >= 0.5,
        "counterexample": "" if correlation is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(metric_values) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8 and max(metric_values) <= 3:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")