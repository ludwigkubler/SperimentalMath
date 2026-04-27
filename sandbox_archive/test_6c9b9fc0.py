# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def walsh_hadamard_transform(f):
        n = len(f)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[i][j] = (-1)**(i & j)
        F = [0] * n
        for k in range(n):
            sum_val = 0
            for i in range(n):
                sum_val += f[i] * T[i][k]
            F[k] = sum_val / math.sqrt(n)
        return F
    
    def max_correlation(f):
        F = walsh_hadamard_transform(f)
        eps = max(abs(x) for x in F)
        return eps
    
    def generate_design(m, n):
        design = []
        while len(design) < m:
            candidate = [random.choice([0, 1]) for _ in range(n)]
            if all(candidate != row for row in design):
                design.append(candidate)
        return design
    
    def min_hamming_distance(matrix):
        min_dist = float('inf')
        n = len(matrix[0])
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                dist = sum(1 for x, y in zip(matrix[i], matrix[j]) if x != y)
                min_dist = min(min_dist, dist)
        return min_dist
    
    def and_of_c_parities(design, c):
        n = len(design[0])
        m = len(design)
        parities = []
        for comb in itertools.combinations(range(n), c):
            parity = [sum(design[i][j] for j in comb) % 2 for i in range(m)]
            parities.append(parity)
        return parities
    
    def nw_distinction(design, predicate, parity):
        n = len(design[0])
        m = len(design)
        count_0 = 0
        count_1 = 0
        for i in range(2**n):
            seed = [int(x) for x in bin(i)[2:].zfill(n)]
            if predicate(seed) == parity[i]:
                count_1 += 1
            else:
                count_0 += 1
        return abs(count_0 - count_1)
    
    l_values = [3, 4, 5]
    m_values = range(4, 9)
    c_values = [1, 2, 3]
    n_max = 20
    
    results = []
    for l in l_values:
        a = l - 1
        d_star = l - a
        for m in m_values:
            design = generate_design(m, n_max)
            d_D = min_hamming_distance(design)
            for c in c_values:
                parities = and_of_c_parities(design, c)
                for parity in parities:
                    eps = max_correlation(parity)
                    RHS = c * eps * 2**(-(d_D - 2 * (l - d_star)) / 2)
                    advantage = nw_distinction(design, lambda x: sum(x) % 2 == parity[0], parity)
                    results.append({
                        "metric_name": "advantage",
                        "metric_value": advantage,
                        "instances_tested": 1,
                        "conjecture_holds": advantage <= RHS,
                        "counterexample": "" if advantage <= RHS else f"adv={advantage}, RHS={RHS}"
                    })
    
    mean_adv = sum(result["metric_value"] for result in results) / len(results)
    std_adv = math.sqrt(sum((result["metric_value"] - mean_adv)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_advantage": mean_adv,
        "std_advantage": std_adv,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_adv = sum(result["mean_advantage"] for result in results) / len(results)
    std_adv = math.sqrt(sum((result["mean_advantage"] - mean_adv)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.99) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_adv} std={std_adv} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.99)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")