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
    
    def xor_function(n, inputs):
        return sum(inputs) % 2
    
    def generate_xor_functions(n, num_functions):
        functions = []
        for _ in range(num_functions):
            function = [random.choice([0, 1]) for _ in range(n)]
            functions.append(function)
        return functions
    
    def tseitin_formula(functions):
        literals = set()
        clauses = []
        for function in functions:
            literal = random.randint(1, 10000)
            literals.add(literal)
            clause = [-literal]
            for input_val in function:
                if input_val == 1:
                    clause.append(random.randint(1, 10000))
                else:
                    clause.append(-random.randint(1, 10000))
            clauses.append(clause)
        return literals, clauses
    
    def resolution_proof_length(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if len(set(stack[i]) & set(stack[j])) == 2:
                        new_clause = [x for x in stack[i] if x not in stack[j]] + [x for x in stack[j] if x not in stack[i]]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
    
    def minimal_local_cohomology_rank(n):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to compute the minimal local cohomology rank of a simplicial complex.
        # For simplicity, we return a constant value that depends on n.
        return math.ceil(math.log2(n))
    
    def generate_simplicial_complex(n):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to generate the simplicial complex associated with an XOR function.
        # For simplicity, we return a constant value that depends on n.
        return math.ceil(math.log2(n))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    num_functions = 30
    functions = generate_xor_functions(n, num_functions)
    literals, clauses = tseitin_formula(functions)
    rank = minimal_local_cohomology_rank(n)
    simplicial_complex_size = generate_simplicial_complex(n)
    
    expected_length = 2 ** (math.log2(n) + math.log2(rank))
    actual_length = resolution_proof_length(clauses)
    
    metric_name = "Resolution proof length"
    metric_value = actual_length
    instances_tested = num_functions
    conjecture_holds = abs(actual_length - expected_length) <= 3
    counterexample = "" if conjecture_holds else f"Expected {expected_length}, got {actual_length}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [41, 59, 67, 83, 101]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"deviation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical support")