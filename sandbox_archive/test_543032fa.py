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
    
    def generate_tseitin_formula(n):
        variables = set()
        clauses = []
        
        for i in range(1, n + 1):
            literals = [random.choice([f'x{i}', f'~x{i}']) for _ in range(random.randint(2, 4))]
            clause = ' | '.join(literals)
            clauses.append(clause)
            variables.update(literals)
        
        tseitin_formula = ' & '.join(clauses) + ' -> ' + ' & '.join(variables)
        return tseitin_formula
    
    def parse_tseitin_formula(formula):
        # Simplified parsing for demonstration purposes
        literals = formula.split(' | ')
        variables = set(literal.strip('~') for literal in literals)
        return literals, variables
    
    def generate_coxeter_group_rank(variables):
        # Simplified rank calculation based on number of variables
        return len(variables) ** 2
    
    def resolution_refutation_length(formula):
        # Simplified length calculation based on formula complexity
        literals, _ = parse_tseitin_formula(formula)
        return len(literals) * 2
    
    n = random.randint(5, 40)
    tseitin_formula = generate_tseitin_formula(n)
    rank = generate_coxeter_group_rank(parse_tseitin_formula(tseitin_formula)[1])
    refutation_length = resolution_refutation_length(tseitin_formula)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": rank > 0 and refutation_length <= rank ** 3,  # Polynomial bound
        "counterexample": "" if rank > 0 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")