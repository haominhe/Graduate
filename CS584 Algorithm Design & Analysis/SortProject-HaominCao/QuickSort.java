/* 
CS 584: Algorithm Design and Analysis
Final Project
Haomin He Cao
June 2019

Comparison of Sorting Algorithms - Quicksort 

References: 
https://www.vogella.com/tutorials/JavaPerformance/article.html
https://www.baeldung.com/java-measure-elapsed-time
https://github.com/Acg1000/Quicksort
https://www.geeksforgeeks.org/quick-sort/
https://www.geeksforgeeks.org/java-util-random-nextint-java/
https://stackoverflow.com/questions/27976857/how-to-get-random-number-with-negative-number-in-range
*/




public class QuickSort {

    public static void QuickSort (int[] array, int left, int right){
        // base case
        if (left >= right) return;
        int i = left;
        int j = right;
        int pivotValue = array[(left + right)/2];  // Pivot is at midpoint
        while (i < j){
            while (array[i] < pivotValue) i++;
            while (pivotValue < array[j]) j--;
            if (i <= j){
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
                i++;
                j--;
            }
        }
        QuickSort (array, left, j);
        QuickSort (array, i, right);
    } 
}