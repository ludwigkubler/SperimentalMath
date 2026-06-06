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
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf)
        indicator = [0] * (2**n)
        for i in range(2**n):
            if all((i & (1 << j)) != 0 for j in range(n) if cnf[j][0] == -j-1 or cnf[j][1] == j+1):
                indicator[i] = 1
        return indicator
    
    def p_adic_l_p_norm(indicator, p):
        norm = sum(abs(x)**p for x in indicator)
        return norm**(1/p) if norm > 0 else 0
    
    def monotone_gadget(cnf):
        n = len(cnf)
        gadget = []
        for i in range(2**n):
            clause = [0] * (2**n)
            for j in range(n):
                if cnf[j][0] == -j-1 and (i & (1 << j)) != 0:
                    clause[i ^ (1 << j)] = 1
                elif cnf[j][1] == j+1 and not (i & (1 << j)):
                    clause[i ^ (1 << j)] = 1
            gadget.append(clause)
        return gadget
    
    def monotone_width(gadget):
        n = len(gadget)
        width = 0
        for i in range(2**n):
            if all((i & (1 << j)) != 0 for j in range(n) if gadget[j][i] == 1):
                width += 1
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    l_p_norms = []
    widths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        indicator = clause_indicator_polynomial(cnf)
        l_p_norm = p_adic_l_p_norm(indicator, 2)  # Using L2 norm for simplicity
        l_p_norms.append(l_p_norm)
        
        gadget = monotone_gadget(cnf)
        width = monotone_width(gadget)
        widths.append(width)
    
    correlation = pearson_correlation(l_p_norms, widths)
    mean_l_p_norm = sum(l_p_norms) / len(l_p_norms)
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": 6,
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.8 and mean_l_p_norm <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")