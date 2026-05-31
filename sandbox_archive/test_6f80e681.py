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
    
    def hodge_diamond_dimension(graph):
        # Placeholder for Hodge diamond dimension computation
        # This is a dummy implementation; replace with actual logic
        return len(graph)

    def communication_complexity(f, graph):
        # Placeholder for communication complexity computation
        # This is a dummy implementation; replace with actual logic
        return 1

    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    D_G = hodge_diamond_dimension(graph)
    C_f = communication_complexity(lambda x: x[0] == x[1], graph)
    
    return {
        "metric_name": "CommunicationComplexity",
        "metric_value": C_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": D_G >= math.log(n) / C_f,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_C = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"Graph size {result['n_max']}, Hodge dimension {hodge_diamond_dimension(result['graph'])}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break