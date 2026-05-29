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
    
    def construct_automaton(f):
        n = int(math.log2(len(f)))
        states = list(range(2**(n+1)))
        transitions = {state: {} for state in states}
        accepting_states = set()
        
        for i in range(n + 1):
            for j in range(2**i):
                if f[j] == 0:
                    next_state = j
                else:
                    next_state = j + 2**i
                transitions[state][i, f[j]] = next_state
        
        accepting_states.add(2**(n+1) - 1)
        
        return states, transitions, accepting_states
    
    def calculate_generality(transitions):
        n = int(math.log2(len(next(iter(transitions.values())))))
        max_depth = 0
        visited = set()
        
        def dfs(state, depth):
            nonlocal max_depth
            if state in visited:
                return
            visited.add(state)
            for key, next_state in transitions[state].items():
                dfs(next_state, depth + 1)
            max_depth = max(max_depth, depth)
        
        dfs(0, 0)
        return max_depth
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        
        sum_diff_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        rho_numerator = n * sum_diff_squared
        rho_denominator = (n * (n**2 - 1)) / 6
        
        return 1 - (rho_numerator / rho_denominator)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        states, transitions, accepting_states = construct_automaton(f)
        g_f = calculate_generality(transitions)
        
        c1 = 1
        c2 = 1 / math.log(n) ** 2
        
        results.append({
            "n": n,
            "g_f": g_f,
            "lower_bound": c1 * 2**n,
            "upper_bound": c2 * 2**n / math.log(n) ** 2
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    g_f_values = [result["g_f"] for result in results]
    lower_bounds = [result["lower_bound"] for result in results]
    upper_bounds = [result["upper_bound"] for result in results]
    
    rho_gf_lb = spearman_rank_correlation(g_f_values, lower_bounds)
    rho_gf_ub = spearman_rank_correlation(g_f_values, upper_bounds)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": (rho_gf_lb + rho_gf_ub) / 2,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": rho_gf_lb >= 0.8 and rho_gf_ub >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")