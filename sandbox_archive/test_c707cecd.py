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
    
    def frege_proof_length(phi):
        # Simplified Frege proof length calculation for demonstration purposes
        return len(phi.split()) * 2
    
    def kahler_einstein_metrics_count(n):
        # Simulated Kähler-Einstein metrics count for demonstration purposes
        return n // 5 + 1
    
    def is_cnf_formula(phi):
        # Simplified CNF formula check
        return "or" in phi and "and" in phi
    
    def property_p(phi):
        # Simplified property P check
        return len(phi.split()) > 10
    
    def property_q(phi):
        # Simplified property Q check
        return frege_proof_length(phi) >= math.log(len(phi.split()), 2)
    
    trials = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 5 instances per size
            phi = " ".join(random.choices(["or", "and"], k=n))
            m_phi = kahler_einstein_metrics_count(n)
            f_phi = frege_proof_length(phi)
            
            trials.append({
                "phi": phi,
                "m_phi": m_phi,
                "f_phi": f_phi
            })
    
    correlation_coefficient = 0.0
    for i in range(len(trials)):
        for j in range(i + 1, len(trials)):
            x_i, y_i = trials[i]["m_phi"], trials[j]["m_phi"]
            x_j, y_j = trials[i]["f_phi"], trials[j]["f_phi"]
            correlation_coefficient += (x_i - mean_m) * (y_i - mean_f) + (x_j - mean_m) * (y_j - mean_f)
    
    correlation_coefficient /= len(trials) ** 2
    
    conjecture_holds = False
    counterexample = ""
    
    for trial in trials:
        if property_p(trial["phi"]):
            if not property_q(trial["phi"]) or trial["f_phi"] < math.log(len(trial["phi"].split()), 2):
                conjecture_holds = False
                counterexample = f"property Q failed for phi: {trial['phi']}"
                break
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(trials),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"property Q failed\" first_failing_seed={first_failing_seed}")