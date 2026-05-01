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
    
    def tropical_add(a, b):
        return max(a, b)
    
    def tropical_multiply(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def tropical_negate(a):
        return -a
    
    def tropical_zero():
        return float('-inf')
    
    def tropical_one():
        return 0
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('-inf')
        return a / b
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_sin(a):
        return math.sin(a)
    
    def tropical_cos(a):
        return math.cos(a)
    
    def tropical_tan(a):
        return math.tan(a)
    
    def tropical_cot(a):
        return 1 / math.tan(a)
    
    def tropical_sec(a):
        return 1 / math.cos(a)
    
    def tropical_csc(a):
        return 1 / math.sin(a)
    
    def tropical_sinh(a):
        return (math.exp(a) - math.exp(-a)) / 2
    
    def tropical_cosh(a):
        return (math.exp(a) + math.exp(-a)) / 2
    
    def tropical_tanh(a):
        return math.tanh(a)
    
    def tropical_coth(a):
        return 1 / math.tanh(a)
    
    def tropical_sech(a):
        return 1 / math.cosh(a)
    
    def tropical_csch(a):
        return 1 / math.sinh(a)
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, n=0):
        return round(a, n)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('-inf')
        return a / b
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_sin(a):
        return math.sin(a)
    
    def tropical_cos(a):
        return math.cos(a)
    
    def tropical_tan(a):
        return math.tan(a)
    
    def tropical_cot(a):
        return 1 / math.tan(a)
    
    def tropical_sec(a):
        return 1 / math.cos(a)
    
    def tropical_csc(a):
        return 1 / math.sin(a)
    
    def tropical_sinh(a):
        return (math.exp(a) - math.exp(-a)) / 2
    
    def tropical_cosh(a):
        return (math.exp(a) + math.exp(-a)) / 2
    
    def tropical_tanh(a):
        return math.tanh(a)
    
    def tropical_coth(a):
        return 1 / math.tanh(a)
    
    def tropical_sech(a):
        return 1 / math.cosh(a)
    
    def tropical_csch(a):
        return 1 / math.sinh(a)
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, n=0):
        return round(a, n)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('-inf')
        return a / b
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_sin(a):
        return math.sin(a)
    
    def tropical_cos(a):
        return math.cos(a)
    
    def tropical_tan(a):
        return math.tan(a)
    
    def tropical_cot(a):
        return 1 / math.tan(a)
    
    def tropical_sec(a):
        return 1 / math.cos(a)
    
    def tropical_csc(a):
        return 1 / math.sin(a)
    
    def tropical_sinh(a):
        return (math.exp(a) - math.exp(-a)) / 2
    
    def tropical_cosh(a):
        return (math.exp(a) + math.exp(-a)) / 2
    
    def tropical_tanh(a):
        return math.tanh(a)
    
    def tropical_coth(a):
        return 1 / math.tanh(a)
    
    def tropical_sech(a):
        return 1 / math.cosh(a)
    
    def tropical_csch(a):
        return 1 / math.sinh(a)
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, n=0):
        return round(a, n)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('-inf')
        return a / b
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_sin(a):
        return math.sin(a)
    
    def tropical_cos(a):
        return math.cos(a)
    
    def tropical_tan(a):
        return math.tan(a)
    
    def tropical_cot(a):
        return 1 / math.tan(a)
    
    def tropical_sec(a):
        return 1 / math.cos(a)
    
    def tropical_csc(a):
        return 1 / math.sin(a)
    
    def tropical_sinh(a):
        return (math.exp(a) - math.exp(-a)) / 2
    
    def tropical_cosh(a):
        return (math.exp(a) + math.exp(-a)) / 2
    
    def tropical_tanh(a):
        return math.tanh(a)
    
    def tropical_coth(a):
        return 1 / math.tanh(a)
    
    def tropical_sech(a):
        return 1 / math.cosh(a)
    
    def tropical_csch(a):
        return 1 / math.sinh(a)
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, n=0):
        return round(a, n)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('-inf')
        return a / b
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_sin(a):
        return math.sin(a)
    
    def tropical_cos(a):
        return math.cos(a)
    
    def tropical_tan(a):
        return math.tan(a)
    
    def tropical_cot(a):
        return 1 / math.tan(a)
    
    def tropical_sec(a):
        return 1 / math.cos(a)
    
    def tropical_csc(a):
        return 1 / math.sin(a)
    
    def tropical_sinh(a):
        return (math.exp(a) - math.exp(-a)) / 2
    
    def tropical_cosh(a):
        return (math.exp(a) + math.exp(-a)) / 2
    
    def tropical_tanh(a):
        return math.tanh(a)
    
    def tropical_coth(a):
        return 1 / math.tanh(a)
    
    def tropical_sech(a):
        return 1 / math.cosh(a)
    
    def tropical_csch(a):
        return 1 / math.sinh(a)
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, n=0):
        return round(a, n)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    
    def tropical_divide(a, b):
        if b == 0:
            return float('-inf')
        return a / b
    
    def tropical_exp(a):
        return math.exp(a)
    
    def tropical_log(a):
        if a <= 0:
            return float('-inf')
        return math.log(a)
    
    def tropical_sin(a):
        return math.sin(a)
    
    def tropical_cos(a):
        return math.cos(a)
    
    def tropical_tan(a):
        return math.tan(a)
    
    def tropical_cot(a):
        return 1 / math.tan(a)
    
    def tropical_sec(a):
        return 1 / math.cos(a)
    
    def tropical_csc(a):
        return 1 / math.sin(a)
    
    def tropical_sinh(a):
        return (math.exp(a) - math.exp(-a)) / 2
    
    def tropical_cosh(a):
        return (math.exp(a) + math.exp(-a)) / 2
    
    def tropical_tanh(a):
        return math.tanh(a)
    
    def tropical_coth(a):
        return 1 / math.tanh(a)
    
    def tropical_sech(a):
        return 1 / math.cosh(a)
    
    def tropical_csch(a):
        return 1 / math.sinh(a)
    
    def tropical_floor(a):
        return math.floor(a)
    
    def tropical_ceil(a):
        return math.ceil(a)
    
    def tropical_round(a, n=0):
        return round(a, n)
    
    def tropical_abs(a):
        return abs(a)
    
    def tropical_sign(a):
        if a > 0:
            return 1
        elif a < 0:
            return -1
        else:
            return 0
    
    def tropical_min(x, y):
        return min(x, y)
    
    def tropical_max(x, y):
        return max(x, y)
    
    def tropical_distance(a, b):
        return abs(a - b)
    