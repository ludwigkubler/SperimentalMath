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
    
    def xor_and_tree_width(cnf):
        # Placeholder implementation for XOR-AND tree width calculation
        return len(cnf)

    def tropicalized_group_order(n):
        # Placeholder implementation for minimal order of tropicalized classical group
        return 2 ** n

    instances_tested = 0
    total_order = 0
    total_width = 0

    for _ in range(100):  # At least 100 different instances
        n = random.randint(5, 40)
        cnf = [random.sample(range(n), k=random.randint(2, n)) for _ in range(random.randint(3, 6))]
        width = xor_and_tree_width(cnf)
        order = tropicalized_group_order(n)

        total_order += order
        total_width += width
        instances_tested += 1

    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    slope, intercept = linear_regression([mean_width] * instances_tested, [mean_order] * instances_tested)

    conjecture_holds = slope >= 0.7 and abs(slope) >= 0.9
    counterexample = "" if conjecture_holds else f"Mean order {mean_order}, mean width {mean_width}"

    return {
        "metric_name": "Proportionality Slope",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n

    return slope, intercept

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_slope = sum(res["metric_value"] for res in results) / len(results)
    std_slope = math.sqrt(sum((res["metric_value"] - mean_slope) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Slope below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")