
from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates key value pair in hash map.  If given key already exists in hash map, associated value must be replaced
        with new value.  If given key is not in hash map a new key/value pair must be added
        """

        hash_map = self._hash_function(key)

        index = hash_map % self._capacity
        bucket = self._buckets.get_at_index(index)

        if self.table_load() > 1.0:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        if bucket is None:
            bucket.insert(key, value)
            self._size += 1

            if self.table_load() >= 1.0:
                new_capacity = self._capacity * 2
                self.resize_table(new_capacity)

        elif bucket.contains(key) is not None:
            bucket.remove(key)
            bucket.insert(key, value)

        else:
            bucket.insert(key, value)
            self._size += 1

            if self.table_load() > 1.0:
                new_capacity = self._capacity * 2
                self.resize_table(new_capacity)


    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets
        """
        empty_count = 0
        bucket = self._buckets

        for count in range(self._capacity):
            if bucket.get_at_index(count).length() == 0:
                empty_count += 1

        return empty_count


    def table_load(self) -> float:
        """
        Returns current table load
        """

        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears contents of hash map.  Does not change capacity
        """

        buckets = self._buckets

        for count in range(self._capacity):
            buckets.set_at_index(count, LinkedList())
            self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table
        """
        new_hash = DynamicArray()
        keys = LinkedList()

        if new_capacity < 1:
            return

        else:
            if self._is_prime(new_capacity) is False:
                capacity = self._next_prime(new_capacity)

            else:
                capacity = new_capacity

            #creates new hash table to store values

            for count in range(capacity):
                new_hash.append(LinkedList())

            for count in range(self._capacity):
                bucket = self._buckets.get_at_index(count)

                for chain in bucket:
                        keys.insert(chain.key, chain.value)

            self._buckets = new_hash
            self._capacity = capacity
            self._size = 0

            for node in keys:
                self.put(node.key, node.value)


    def get(self, key: str):
        """
        Returns value of a given key.  otherwise returns None
        """
        bucket = self._buckets
        hash_map = self._hash_function(key)
        index = hash_map % self._capacity

        if bucket.get_at_index(index).contains(key) is not None:

            return bucket.get_at_index(index).contains(key).value

        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in hash map otherwise return false.
        """

        bucket = self._buckets
        hash_map = self._hash_function(key)
        index = hash_map % self._capacity


        if bucket.get_at_index(index).contains(key) is not None:
            return True

        else:
            return False


    def remove(self, key: str) -> None:
        """
        Removes a given key and associated value from hash map
        """

        hash_map = self._hash_function(key)
        index = hash_map % self._capacity
        bucket = self._buckets.get_at_index(index)

        if bucket.contains(key) is None:
            return

        else:
            bucket.remove(key)
            self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns dynamic array where each index contains a tuple of a key/value pair stored in hash map
        """

        new_da = DynamicArray()
        bucket = self._buckets

        for count in range(bucket.length()):
            for node in bucket.get_at_index(count):
                new_da.append(node.value)

        return new_da


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())
