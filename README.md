[![Burrowts](https://github.com/iunary/burrowts/actions/workflows/app.yml/badge.svg)](https://github.com/iunary/burrowts/actions/workflows/app.yml)

# BurrowTS

The BurrowTS is a Python library that provides a simple and efficient time series database for storing and retrieving time-stamped values.

## Features

- Insert values into the time series database with an associated timestamp.
- Retrieve time series data for a given series name.
- Retrieve time series data for a given series name by timestamp range.
- Thread-safe operations using a lock.
- Data persistence using pickle.

## Installation

You can install the BurrowTS using pip:

```
pip install burrowts
```

## Usage

Here's an example of how to use the BurrowTS:

```python
from burrowts import BurrowTS

db = BurrowTS()

# Insert values
db.insert("cpu", 12.3)
db.insert("cpu", 14.9)
db.insert("mem", 20.4)

# Retrieve time series data
cpu_data = db.get_series("cpu")
print("CPU Data:", cpu_data)
```

## Data Persistence

The BurrowTS uses pickle for data persistence. The database data is stored in a pickle file specified by the `file_path` parameter. The data is automatically saved to the file after each insertion operation.

## Thread Safety

The BurrowTS ensures thread safety by using a lock. This allows for concurrent access from multiple threads while maintaining data integrity.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
