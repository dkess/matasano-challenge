import util

gen1 = util.MT19937(100)
o1 = [gen1.extract_number(), gen1.extract_number(), gen1.extract_number(), gen1.extract_number()]

gen2 = util.MT19937(100)
o2 = [gen2.extract_number(), gen2.extract_number(), gen2.extract_number(), gen2.extract_number()]

print('4 random numbers with seed 100:')
print(o1)
if o1 != o2:
    print('Generator is not deterministic! Something is very wrong')
