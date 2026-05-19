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

def walsh_fourier_coefficient(F, S):
    n = len(F)
    sum_term = 0
    for i in range(2**n):
        term = (-1)**sum((i >> j) & 1 for j in range(n) if (j + 1) in S)
        sum_term += F[i] * term
    return Fraction(sum_term, 2**n)

def level_1_low_frequency_fraction(F):
    n = len(F)
    sum_level_1 = sum(walsh_fourier_coefficient(F, {j+1 for j in range(n) if (i >> j) & 1})**2 for i in range(1, n + 1))
    sum_level_2_and_above = sum(walsh_fourier_coefficient(F, {j+1 for j in range(n) if (i >> j) & 1})**2 for i in range(n + 1, 2**n))
    return Fraction(sum_level_1, sum_level_1 + sum_level_2_and_above)

def complexity_measure(lambda_F):
    if lambda_F >= 1/len(F):
        return -math.inf
    return -math.log2(max(lambda_F, 1/len(F)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [16, 24, 32, 40]
    s_values = [10, 20, 40, 80, 160]
    widths = range(2, 7)
    
    results_A = []
    for n in n_values:
        for s in s_values:
            for width in widths:
                F = [random.choice([0, 1]) for _ in range(2**n)]
                L_F = sum(F)
                mu_F = complexity_measure(level_1_low_frequency_fraction(F))
                results_A.append((L_F, mu_F))
    
    results_B = []
    for v in range(4, 9):
        k = math.floor(math.sqrt(v))
        F_v = [0] * (2**v)
        for i in range(v):
            for j in range(i+1, v):
                F_v[(1 << i) | (1 << j)] = 1
        mu_F_v = complexity_measure(level_1_low_frequency_fraction(F_v))
        results_B.append((mu_F_v, v))
    
    mean_mu_A = sum(mu_F for _, mu_F in results_A) / len(results_A)
    std_mu_A = math.sqrt(sum((mu_F - mean_mu_A)**2 for _, mu_F in results_A) / len(results_A))
    support_fraction_A = sum(1 for _, mu_F in results_A if mu_F <= 2 * math.log2(L_F + 2) + 4) / len(results_A)
    
    all_results_B = [mu_F_v >= v/8 for mu_F_v, _ in results_B]
    support_fraction_B = sum(all_results_B) / len(all_results_B)
    
    conjecture_holds_A = support_fraction_A == 1.0
    conjecture_holds_B = support_fraction_B == 1.0
    
    counterexample_A = "" if conjecture_holds_A else "random DNF with μ > 2·log₂(L+2)+4"
    counterexample_B = "" if conjecture_holds_B else "k-CLIQUE indicator F*_v with μ < v/8"
    
    return {
        "metric_name": "complexity_measure",
        "metric_value_A": mean_mu_A,
        "metric_value_B": support_fraction_B,
        "instances_tested_A": len(results_A),
        "instances_tested_B": len(results_B),
        "conjecture_holds_A": conjecture_holds_A,
        "conjecture_holds_B": conjecture_holds_B,
        "counterexample_A": counterexample_A,
        "counterexample_B": counterexample_B
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_mu_A = sum(trial["metric_value_A"] for trial in results) / len(results)
    std_mu_A = math.sqrt(sum((trial["metric_value_A"] - mean_mu_A)**2 for trial in results) / len(results))
    support_fraction_A = sum(1 for trial in results if trial["conjecture_holds_A"]) / len(results)
    
    all_results_B = [trial["conjecture_holds_B"] for trial in results]
    support_fraction_B = sum(all_results_B) / len(all_results_B)
    
    if support_fraction_A == 1.0 and support_fraction_B == 1.0:
        print(f"RESULT: SUPPORTED mean={mean_mu_A} std={std_mu_A} support_fraction={support_fraction_A}")
    elif not all_results_B:
        print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE indicator F*_v with μ < v/8\" first_failing_seed={seeds[all_results_B.index(False)]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")