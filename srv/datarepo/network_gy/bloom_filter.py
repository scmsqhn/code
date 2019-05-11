from bitarray import bitarray
import numpy as np
import pdb

# 3rd party
#import mmh3

class BloomFilter(set):

    def __init__(self):
        super(BloomFilter, self).__init__()
        self.size = [256,127]
        self.bit_array_a = bitarray(self.size[0])
        self.bit_array_b = bitarray(self.size[1])
        self.bit_array_a.setall(0)
        self.bit_array_b.setall(0)

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.bit_array_a)

    def add(self, item):
            idx = hash(item) % self.size[0]
            idy = hash(item) % self.size[1]
            self.bit_array_a[idx] = 1
            self.bit_array_b[idy] = 1

    def __contains__(self, item):
        out = True
        idx = hash(item) % self.size[0]
        idy = hash(item) % self.size[1]
        if self.bit_array_a[idx] == 0 or self.bit_array_b[idy] == 0:
            out = False
        return out

def main():
        bloom = BloomFilter()
        animals = ['dog', 'cat', 'giraffe', 'fly', 'mosquito', 'horse', 'eagle',
                   'bird', 'bison', 'boar', 'butterfly', 'ant', 'anaconda', 'bear',
                   'chicken', 'dolphin', 'donkey', 'crow', 'crocodile']
        # First insertion of animals into the bloom filter
        for animal in animals:
            bloom.add(animal)
            # There should not be any false negatives
        for animal in animals:
            if animal in bloom:
                print('{} is in bloom filter as expected'.format(animal))
            else:
                print('Something is terribly went wrong for {}'.format(animal))
                print('FALSE NEGATIVE!')

        # Membership existence for not inserted animals
        # There could be false positives
        other_animals = ['badger', 'cow', 'pig', 'sheep', 'bee', 'wolf', 'fox',
                 'whale', 'shark', 'fish', 'turkey', 'duck', 'dove',
                 'deer', 'elephant', 'frog', 'falcon', 'goat', 'gorilla',
                 'hawk' ]
        for other_animal in other_animals:
            if other_animal in bloom:
                print('{} is not in the bloom, but a false positive'.format(other_animal))
            else:
                print('{} is not in the bloom filter as expected'.format(other_animal))


if __name__ == '__main__':
    main()
