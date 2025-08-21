from typing import Callable


def get_match_for_valid_exec(name: str, match_func: Callable, actual, expected, is_failed) -> bool:
    if is_failed:
        return False
    try:
        return match_func(expected, actual)
    except Exception as e:
        print(f"warning: matching error {type(e).__name__}: {str(e)}")
        print(f"function: {name}")
        print(f"expected ({type(expected)}): {expected}")
        print(f"actual ({type(actual)}): {actual}")
        print()
        return False
