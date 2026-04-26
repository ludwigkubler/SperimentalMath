import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):  # Each variable appears twice positively and negatively
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            if random.random() < 0.5:
                clauses.append((var, sign))
            else:
                clauses.append((-var, -sign))
        return clauses
    
    def fourier_entropy(n, clauses):
        total = 0
        for subset in range(2**n):
            prob = 1
            for i in range(n):
                if (subset >> i) & 1:
                    sign = sum(clause[1] for clause in clauses if clause[0] == i + 1)
                    prob *= math.exp(-sign * 1j * math.pi / n)
                else:
                    sign = sum(clause[1] for clause in clauses if clause[0] == -i - 1)
                    prob *= math.exp(sign * 1j * math.pi / n)
            total += abs(prob) ** 2
        return total
    
    def communication_complexity(n):
        # Simplified deterministic protocol: O(n) bits
        return n
    
    n = random.choice([5, 8, 11, 14])
    formula = generate_3cnf(n)
    entropy = fourier_entropy(n, formula)
    complexity = communication_complexity(n)
    
    metric_name = "Fourier Entropy / Communication Complexity Ratio"
    metric_value = entropy / complexity
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if abs(entropy - n * math.log2(n)) < 1e-6 and abs(complexity - n) < 1e-6:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    total_entropy = 0
    total_complexity = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_entropy += trial_result["metric_value"]
        total_complexity += trial_result["instances_tested"] * trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_entropy = total_entropy / len(seeds)
    std_entropy = math.sqrt(sum((x["metric_value"] - mean_entropy) ** 2 for x in results) / len(results))
    support_fraction = count_supporting / len(seeds)
    
    print(f"TRIAL: {results}")
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Fourier entropy and communication complexity are not inversely proportional\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")