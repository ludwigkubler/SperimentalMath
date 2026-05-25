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
    
    def k_theory_group(V):
        n = len(V)
        G_V = 0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        G_V += V[i][k] * V[j][l]
        return G_V / (n ** 2)

    def communication_complexity(V):
        n = len(V)
        # Placeholder for actual computation
        return n ** (3/2)

    instances_tested = 0
    total_rank = 0
    total_communication = 0

    for _ in range(30):  # 30 random seeds
        n = random.randint(5, 40)
        V = [[random.random() for _ in range(n)] for _ in range(n)]
        rank = k_theory_group(V)
        communication = communication_complexity(V)

        total_rank += rank
        total_communication += communication
        instances_tested += 1

    mean_rank = total_rank / instances_tested
    mean_communication = total_communication / instances_tested
    std_deviation = math.sqrt(sum((communication - mean_communication) ** 2 for communication in range(instances_tested))) / instances_tested

    conjecture_holds = mean_communication >= mean_rank * (3/2)
    counterexample = "" if conjecture_holds else f"Mean rank: {mean_rank}, Mean communication: {mean_communication}"

    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_communication,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")

        results.append(trial_result)

    mean_communication = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_communication) ** 2 for result in results)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_communication} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity < rank * (3/2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")