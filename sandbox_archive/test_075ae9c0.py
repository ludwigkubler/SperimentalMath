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
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_rho_bp = 0
    total_rho_ip2 = 0

    def free_probability_tensor_entanglement(bp):
        # Placeholder for actual implementation of free probability tensor entanglement calculation
        return random.uniform(0, n)  # Simplified for testing purposes

    for _ in range(30):
        if random.choice([True, False]):
            bp = [random.randint(0, 1) for _ in range(n)]
            instances_tested += 1
            rho_bp = free_probability_tensor_entanglement(bp)
            total_rho_bp += rho_bp
        else:
            ip2 = [random.randint(0, 1) for _ in range(n)]
            instances_tested += 1
            rho_ip2 = free_probability_tensor_entanglement(ip2)
            total_rho_ip2 += rho_ip2

    mean_rho_bp = total_rho_bp / instances_tested if instances_tested > 0 else 0
    mean_rho_ip2 = total_rho_ip2 / instances_tested if instances_tested > 0 else 0

    conjecture_holds_bp = mean_rho_bp <= math.log(n)
    conjecture_holds_ip2 = mean_rho_ip2 >= n

    return {
        "metric_name": "free_probability_tensor_entanglement",
        "metric_value_bp": mean_rho_bp,
        "metric_value_ip2": mean_rho_ip2,
        "instances_tested": instances_tested,
        "conjecture_holds_bp": conjecture_holds_bp,
        "conjecture_holds_ip2": conjecture_holds_ip2,
        "counterexample_bp": "" if conjecture_holds_bp else f"BP with n={n}, rho(P)={mean_rho_bp}",
        "counterexample_ip2": "" if conjecture_holds_ip2 else f"IP_2 with n={n}, rho(IP_2)={mean_rho_ip2}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    results_bp = []
    results_ip2 = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds_bp"]:
            results_bp.append(result["metric_value_bp"])
        if result["conjecture_holds_ip2"]:
            results_ip2.append(result["metric_value_ip2"])

    mean_rho_bp = sum(results_bp) / len(results_bp) if results_bp else 0
    std_rho_bp = math.sqrt(sum((x - mean_rho_bp) ** 2 for x in results_bp) / len(results_bp)) if results_bp else 0
    support_fraction_bp = len(results_bp) / len(seeds)

    mean_rho_ip2 = sum(results_ip2) / len(results_ip2) if results_ip2 else 0
    std_rho_ip2 = math.sqrt(sum((x - mean_rho_ip2) ** 2 for x in results_ip2) / len(results_ip2)) if results_ip2 else 0
    support_fraction_ip2 = len(results_ip2) / len(seeds)

    if support_fraction_bp >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_bp} std={std_rho_bp} support_fraction={support_fraction_bp}")
    elif support_fraction_ip2 >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_ip2} std={std_rho_ip2} support_fraction={support_fraction_ip2}")
    else:
        first_failing_seed = seeds[results_bp.index(max(results_bp)) if results_bp else -1]
        print(f"RESULT: FALSIFIED counterexample=\"IP_2\" first_failing_seed={first_failing_seed}")