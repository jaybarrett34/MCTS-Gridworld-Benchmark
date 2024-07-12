import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from algorithms.uct import UCT
from algorithms.bts import BTS
from algorithms.ments import MENTS
# from algorithms.dents import DENTS
from components.tree import Tree
import time
from components.print import print_grid
import threading

# Timeout decorator
def timeout(seconds=10, error_message="Runtime limit exceeded"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            def thread_func():
                result[0] = func(*args, **kwargs)
            
            thread = threading.Thread(target=thread_func)
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                print(error_message)
                return None
            return result[0]
        return wrapper
    return decorator

@timeout(seconds=10)
def run_benchmark(algorithm_class, env, iterations=10000):
    env.reset()

    tree = Tree()
    algorithm = algorithm_class(env=env, tree=tree)

    start_time = time.time()
    algorithm.run(iterations)
    end_time = time.time()

    print(f"Algorithm: {algorithm_class.__name__}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    algorithm.print_best_path()

if __name__ == "__main__":
    algorithms = [UCT, MENTS, BTS]
    env_name = 'FrozenLake-v1'
    iterations = 10000

    env = gym.make(env_name, desc=generate_random_map(size=4), is_slippery=False)

    print("Initial Environment Grid:")
    print_grid(env)

    for algo in algorithms:
        print(f"\nRunning benchmark for {algo.__name__}")
        run_benchmark(algo, env, iterations)
