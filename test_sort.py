"""
Модуль тестирования функций сортировки
"""

import unittest
import main

class TestSort(unittest.TestCase):
    reference_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    test_list = [9, 6, 8, 7, 4, 10, 5, 3, 1, 2, 0]
    def testBubbleSort(self):
        """
        Тест сортировки пузырьком
        :return: None
        """
        sort = main.bubble_sort(self.test_list)
        self.assertListEqual(sort[1], self.reference_list)
        #self.assertTrue(sort[0])
    def testRadixSort(self):
        """
        Тест поразрядной сортировки
        :return: None
        """
        sort = main.radix_sort(self.test_list)
        self.assertListEqual(sort[1], self.reference_list)
    def testCountingSort(self):
        """
        Тест сортировки подсчетом
        :return: None
        """
        sort = main.counting_sort(self.test_list, max(self.test_list))
        self.assertListEqual(sort[1], self.reference_list)
    def testHeapSort(self):
        """
        Тест прирамидальной сортировки
        :return: None
        """
        sort = main.heap_sort(self.test_list)
        self.assertListEqual(sort[1], self.reference_list)
    def testMergeSort(self):
        """
        Тест сортировки слиянием
        :return: None
        """
        sort = main.merge_sort(self.test_list)
        self.assertListEqual(sort[1], self.reference_list)
    def testQuickSort(self):
        """
        Тест быстрой сортировки
        :return: None
        """
        sort = main.quicksort(self.test_list)
        self.assertListEqual(sort[1], self.reference_list)



if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
