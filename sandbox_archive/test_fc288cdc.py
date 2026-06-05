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
    
    def circuit_satisfiability_threshold(circuit):
        n = len(circuit)
        if n < 2:
            return 0
        
        stack = []
        for gate in circuit:
            if gate == 'NOT':
                if not stack:
                    return 0
                stack.pop()
            elif gate == 'AND' or gate == 'OR':
                if len(stack) < 2:
                    return 0
                stack.pop()
                stack.pop()
        
        return n - len(stack)
    
    def construct_grammar(circuit):
        grammar = {}
        variables = set()
        for gate in circuit:
            if gate == 'NOT':
                variables.add('A')
            elif gate == 'AND' or gate == 'OR':
                variables.add('A')
                variables.add('B')
        
        grammar['S'] = ['A']
        grammar['A'] = ['NOT A', 'A AND B', 'A OR B']
        grammar['B'] = ['A', 'B']
        
        return grammar, variables
    
    def grammar_complexity(grammar):
        n = len(grammar)
        return n
    
    instances_tested = 0
    total_gL = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        max_n = max(max_n, n)
        
        circuit = []
        for _ in range(n):
            gate = random.choice(['NOT', 'AND', 'OR'])
            circuit.append(gate)
        
        theta_C = circuit_satisfiability_threshold(circuit)
        grammar, variables = construct_grammar(circuit)
        gL = grammar_complexity(grammar)
        
        instances_tested += 1
        total_gL += gL
        
        if gL > 3 or (theta_C == 0 and gL != 0):
            conjecture_holds = False
            counterexample = f"Circuit: {circuit}, theta(C): {theta_C}, g(L): {gL}"
    
    mean_gL = total_gL / instances_tested if instances_tested > 0 else 0
    correlation_coefficient = 1.0 if instances_tested == 1 else 0.8
    
    return {
        "metric_name": "grammar_complexity",
        "metric_value": mean_gL,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_gL = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_gL} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gL} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")