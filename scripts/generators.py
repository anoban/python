from random import randint

numbers: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
iterator = iter(
    numbers
)  # the global function iter() returns an iterator from a collection
# like C++ iterators, Python iterators are exhaustible, they cannot be reused to reiterate over the collection again
# we'll need a new iterator!!!!

while True:
    try:
        print(
            next(iterator)
        )  # nex() basically returns each element in the collection sequentially, like calling the dereferencing operator and increment operator on a C++ iterator
    except StopIteration:
        print("Iterator exhausted!")
        break
print("-------\n\n")

# when we write a for loop like this, the interpretor calls the __iter__() method of that object to get an iterator
# it then uses that iterator to traverse through the collection
for n in numbers:
    print(n)
print("-------\n\n")

# [print(n) for n in numbers]

for n in iter(numbers):
    print(n)
print("-------\n\n")

# the more detailed version of the above is
__iterator = numbers.__iter__() # we capture the iterator, this is equivalent to obtaining the iterator with the global iter() function
while True:
    try:
        print(__iterator.__next__())    # this is equivalent to moving to the next element with the global next() function
    except StopIteration: # when the iterator is exhausted
        break

# this means a Python iterator is aware of the internal details of the collection it represents i.e number of elements, current offset
# consider this,
randoms: list[int] = [randint(0, 10) for _ in range(100)]
__iterator_previous_state = randoms.__iter__()
for i in range(0, 100, 2):
    randoms[i] = 0
__iterator_final_state = randoms.__iter__()

print(sum(__iterator_previous_state), sum(__iterator_final_state))

# let's see what methods and attributes are available in an iterator
sequence: list[int] = [i for i in range(100)]
iterator = sequence.__iter__()
print(dir(iterator))

print(f"__sizeof__ {iterator.__sizeof__()}")   # size of the iterator in bytes
print(f"__getstate__ {iterator.__getstate__()}")    # seems to be None all the time ???
# after calling __next__() 50 times
for _ in range(50):
    iterator.__next__()

# __setstate__() ????
print(f"__length_hint__ {iterator.__length_hint__()}")
iterator.__length_hint__() = 80
for i in iterator:
    print(i)
