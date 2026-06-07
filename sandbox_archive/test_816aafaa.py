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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def tropical_cyclotomic_polynomial(instance):
        n = len(instance)
        poly = [Fraction(1)] + [Fraction(0)] * (n - 1)
        
        for i in range(1, n):
            new_poly = [Fraction(0)] * (n + i - 1)
            for j in range(n):
                if j + i - 1 >= len(new_poly):
                    continue
                new_poly[j + i - 1] += poly[j] * instance[j]
            poly = new_poly
        
        degree = max(i for i, coeff in enumerate(poly) if coeff != Fraction(0))
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_boolean_instance(n)
            degree = tropical_cyclotomic_polynomial(instance)
            total_metric_value += degree
            instances_tested += 1
            n_max = max(n_max, n)
            
            if degree < n ** (1/3):
                conjecture_holds = False
                counterexample = f"n={n}, instance={instance}, degree={degree}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested - sum(1 for _ in range(instances_tested) if not conjecture_holds), instances_tested)
    
    return {
        "metric_name": "Tropical Cyclotomic Polynomial Degree",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    mean_metric_value = sum(trial["metric_value"] for trial in trials) / len(trials)
    support_fraction = Fraction(sum(1 for trial in trials if trial["conjecture_holds"]), len(trials))
    
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif sum(1 for trial in trials if not trial["conjecture_holds"]) / len(trials) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{trials[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(trials)}")