def check_numbers(tup: tuple) -> bool:
  """
  **check_numbers Function**
  This function checks if all elements in a tuple are either integers or floats. It iterates through 
  each element in the input tuple and verifies whether it is an instance of either int or float. 
  If any element fails this check, the function returns False. If all elements pass the check, 
  it returns True.
  
  Args:
      tup (tuple, required): A tuple containing elements to be checked for numeric type.
  
  Returns:
      bool: True if all elements in `tup` are either integers or floats, otherwise False.
      
  Raises:
      TypeError: If `tup` is not a tuple.
  """
  for _,i in enumerate(tup):
    if (not isinstance(i, int)) or (not isinstance(i, float)):
      return False
  return True
