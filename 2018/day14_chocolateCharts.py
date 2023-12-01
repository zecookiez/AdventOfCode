from time import time
t0 = time()
puzzle = 919901

def chocolateCharts(target):
    # Using python 2.7, this took:
    # O(n) Bruteforce check: 10 seconds
    # O(n) Hashing solution: 7.5 seconds

    # n in this case is the number of iterations taken to generate the numbers, which is ~10 million

    # Using pypy:
    # Bruteforce check: 1.3 seconds
    # Hashing approach: 1 seconds
    
    length = len(str(target)) # Number of digits
    mult = pow(10, length - 1) # Position of most significant digit
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    curHash = 37 # Hash number, we used base 10 to easily conceptualize and its also very convenient with other operations
    addRecipe = recipes.append # Saving a function as an alias saves time, especially when it has 20 million iterations
    while 1:
        newRecipe = recipes[elf1] + recipes[elf2]
        if newRecipe > 9: # Double-digits, guaranteed to be a 1 because the maximum is 9 + 9 => 18
            curHash = curHash % mult * 10 + 1 # Remove most-significant digit, shift every digit, add the number on the right
            # Ex: 12345 (Original hash number) => 2345 (Remove with modulo) => 23450 (Mult by 10) => 23451 (The new hash number)
            addRecipe(1)
            if target == curHash: # Found it!
                return len(recipes) - length
            elif len(recipes) - 10 == target: # Part A problem
                print("Part A: %s" % "".join(map(str, recipes[-10:])))
            newRecipe -= 10 # Remove the digit
        curHash = curHash % mult * 10 + newRecipe # Same operations as line 25
        addRecipe(newRecipe)
        if target == curHash: # Found it!
            return len(recipes) - length
        elif len(recipes) - 10 == target: # Part A problem
            print("Part A: %s" % "".join(map(str, recipes[-10:])))
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes) # Update elf positions
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

print("Part B: %d" % chocolateCharts(puzzle))
print("Time: %d ms" % (1000 * (time() - t0)))
