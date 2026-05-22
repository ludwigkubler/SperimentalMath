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
    
    n = 40
    quasigroup = [[random.randint(1, n) for _ in range(n)] for _ in range(n)]
    tropicalized_quasigroup = [[max(quasigroup[i][j], quasigroup[j][i]) for j in range(n)] for i in range(n)]
    
    def ac0_circuit_size(quasigroup):
        # Placeholder function to compute AC0 circuit size
        return len(quasigroup) * len(quasigroup[0])
    
    tropical_rank = sum(1 for row in tropicalized_quasigroup if any(row[j] != 0 for j in range(n)))
    ac0_circuit_size_value = ac0_circuit_size(quasigroup)
    
    metric_name = "Tropicalized Rank / AC0 Circuit Size"
    metric_value = tropical_rank / ac0_circuit_size_value
    instances_tested = 1
    conjecture_holds = metric_value >= 0.7
    counterexample = "" if conjecture_holds else f"Tropical rank {tropical_rank} is not at least 0.7 * AC0 circuit size {ac0_circuit_size_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Tropical rank is not at least 0.7 * AC0 circuit size\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")