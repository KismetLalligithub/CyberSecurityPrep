try: 
    ...
    ...
    ...
except ValueError:
    print("Error: enter valid value for denominator.")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
except Exception as e:
    print(f"An unexpected error occured: {e}")

#multiple errors handling in one

try:
    value = int("text")
except (ValueError, TypeError): 
    print("A ValueError or TypeError occurred.")

try:
    ...
except: 
    ...
else: 
    ...
finally:
    # always runs. 


