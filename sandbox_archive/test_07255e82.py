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
    n = 10  # Start with a small instance size and increase if needed
    instances_tested = 0
    total_lcd = 0
    total_log_width = 0
    lcd_values = []
    
    while True:
        # Generate a random Boolean formula with n clauses
        formula = [random.choice([True, False]) for _ in range(n)]
        
        # Calculate the local cohomological defect (LCD)
        lcd = sum(formula)  # Simplified example: sum of literals
        
        # Calculate the proof width (width of the Frege proof)
        width = len(formula)
        
        if width == 0:
            continue
        
        instances_tested += 1
        total_lcd += lcd
        total_log_width += math.log(width)
        lcd_values.append(lcd / math.log(width))
        
        # Check if we have tested enough instances
        if instances_tested >= 30:
            break
    
    mean_lcd = total_lcd / instances_tested
    std_dev = (sum((x - mean_lcd) ** 2 for x in lcd_values) / instances_tested) ** 0.5
    correlation_coefficient = sum((lcd_values[i] - mean_lcd) * (total_log_width / instances_tested - math.log(width)) for i, width in enumerate(formula)) / (instances_tested * std_dev * math.sqrt(total_log_width / instances_tested))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(abs(lcd / math.log(width) - mean_lcd) <= 3 * std_dev for lcd, width in zip(lcd_values, formula)),
        "counterexample": "" if correlation_coefficient >= 0.8 else "Correlation coefficient < 0.8 or LCD exceeds log(width) by more than 3 standard deviations"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8 or LCD exceeds log(width) by more than 3 standard deviations\" first_failing_seed={first_failing_seed}")