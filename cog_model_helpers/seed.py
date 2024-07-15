from cog import Input
import random


def predict_seed() -> int:
    return Input(
        description="Set a seed for reproducibility. Random by default.",
        default=None,
    )


def generate(seed: int) -> int:
    if seed is None or seed < 0:
        seed = random.randint(0, 2**32 - 1)
        print(f"Random seed set to: {seed}")
    else:
        print(f"Seed set to: {seed}")
    return seed
