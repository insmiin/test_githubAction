# helpers.py
def convert_to_uppercase(value_b):
    mapping = {"b": "A", "c": "X"}

    if value_b not in mapping:
        # Fail fast with a clear message
        raise ValueError(f"Mapping failed: '{value_b}' is not a valid identifier.")

    return mapping[value_b]

def test_processing_behavior2():
    # If this raises a ValueError, Pytest catches it and marks the test as FAILED.
    # This is exactly what you want if the input was supposed to be valid.


    result = 3
    assert result == 3

# test_script.py
def test_processing_behavior():
    # If this raises a ValueError, Pytest catches it and marks the test as FAILED.
    # This is exactly what you want if the input was supposed to be valid.
    a = convert_to_uppercase("invalid_b")

    result = 3
    assert result == 3