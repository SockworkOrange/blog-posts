import sys
from statistics import median

def stdin_source():
  def try_to_int(val):
      try:
          return int(val)
      except ValueError:
          return None

  for input in sys.stdin:
    if input.strip() == 'exit':
      exit()

    val = try_to_int(input)
    if val is not None:
      print('> %d' % val)
      yield val

def filter_numbers(numbers, predicate):
  for val in numbers:
    if predicate(val):
      yield val

def fixed_event_window(numbers, window_size):
  arr = []
  for val in numbers:
    arr.append(val)
    
    if len(arr) >= window_size:
      res = arr.copy()
      arr = []
      yield res

def fold_sum(arrs):
  for arr in arrs:
    yield sum(arr)

def fold_median(arrs):
  for arr in arrs:  
    yield median(arr)

def stdout_sink(numbers):
  for val in numbers:
    print(val)
    yield val

numbers = stdin_source()
filtered = filter_numbers(numbers, lambda x: x > 0)
windowed_for_sum = fixed_event_window(filtered, 2)
folded_sum = fold_sum(windowed_for_sum)
windowed_for_median = fixed_event_window(folded_sum, 3)
folded_median = fold_median(windowed_for_median)
res = stdout_sink(folded_median)

if __name__== "__main__":
    list(res)
