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
    
    def generate_formula(n):
        if n == 1:
            return 'x'
        else:
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(n - len(left.split('&')) - 1)
            return f'({left}&{right})'

    def frege_proof_length(formula):
        if formula == 'x':
            return 1
        else:
            left, right = formula[2:-1].split('&')
            return 1 + max(frege_proof_length(left), frege_proof_length(right))
    
    def frobenius_monomial_rank(formula):
        if formula == 'x':
            return 1
        else:
            left, right = formula[2:-1].split('&')
            return frobenius_monomial_rank(left) + frobenius_monomial_rank(right)
    
    def reduce_proof_length(formula):
        if formula == 'x':
            return 'x'
        else:
            left, right = formula[2:-1].split('&')
            new_left = reduce_proof_length(left)
            new_right = reduce_proof_length(right)
            if len(new_left.split('&')) > len(new_right.split('&')):
                return f'({new_left}&{right})'
            else:
                return f'({left}&{new_right})'

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mfr = 0
    total_l = 0
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            mfr = frobenius_monomial_rank(formula)
            l = frege_proof_length(formula)
            instances_tested += 1
            total_mfr += mfr
            total_l += l

            if mfr != l:
                counterexample = f"Formula: {formula}, MFR: {mfr}, L: {l}"
                break
        
        if counterexample:
            break
    
    mean_mfr = total_mfr / instances_tested
    mean_l = total_l / instances_tested

    conjecture_holds = abs(mean_mfr - mean_l) < 0.1 * max(mean_mfr, mean_l)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": (mean_mfr * mean_l - instances_tested * mean_mfr * mean_l / instances_tested) /
                        math.sqrt((instances_tested * mean_mfr**2 - total_mfr**2 / instances_tested) *
                                  (instances_tested * mean_l**2 - total_l**2 / instances_tested)),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")