import numpy as np
from numba import njit
import time
import sys

@njit
def generate_random_numbers(chunk_size):
    """Generate an array of random numbers."""
    random_numbers = np.empty(chunk_size, dtype=np.uint8)
    for i in range(chunk_size):
        random_numbers[i] = np.random.randint(0, 256)
    return random_numbers

def generate_random_bytes(filename, size, chunk_size=1024*1024):
    try:
        with open(filename, 'wb') as f:
            start_time = time.time()
            total_chunks = size // chunk_size + (1 if size % chunk_size != 0 else 0)
            for i in range(total_chunks):
                current_chunk_size = min(chunk_size, size)
                # Generate random numbers using Numba
                random_numbers = generate_random_numbers(current_chunk_size)
                # Convert the random numbers to bytes
                random_bytes = random_numbers.tobytes()
                f.write(random_bytes)
                size -= current_chunk_size
                progress = (i + 1) / total_chunks
                bar_length = 50
                filled_length = int(round(bar_length * progress))
                bar_fill = '#' * filled_length + '-' * (bar_length - filled_length)
                sys.stdout.write(f"\rGenerating random bytes: [{bar_fill}] {int(round(progress * 100))}%")
                sys.stdout.flush()
            end_time = time.time()
            sys.stdout.write(f"\nGenerated random bytes in {end_time - start_time:.2f} seconds\n")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_file_contents(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

def main():
    input_filename = 'input_bytes.bin'
    output_filename = 'random_bytes.bin'
    input_contents = get_file_contents(input_filename)
    if input_contents is not None:
        input_size = len(input_contents)
        print(f"Input file size: {input_size} bytes")
        generate_random_bytes(output_filename, input_size)
    else:
        print("Exiting due to file not found.")

if __name__ == "__main__":
    main()
