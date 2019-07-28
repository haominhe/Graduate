/* 
CS 584: Algorithm Design and Analysis
Final Project
Haomin He Cao
June 2019

Comparison of Sorting Algorithms - Counting Sort 

References: 
https://www.geeksforgeeks.org/counting-sort/
https://github.com/farhankhwaja/CountingSort
*/

import java.util.*;

public class CountingSort {
    public static void CountingSort(int[] arr) {
        int maxNum = Arrays.stream(arr).max().getAsInt();
        int minNum = Arrays.stream(arr).min().getAsInt();
        int rangeNum = maxNum - minNum + 1;
        int counter[] = new int[rangeNum];
        int output[] = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
           //calculate the total number of times that a value in INPUT array
            counter[arr[i] - minNum]++;
        }

        for (int i = 1; i < counter.length; i++) {
            // add up previous value
            counter[i] += counter[i - 1];
        }

        for (int i = arr.length - 1; i >= 0; i--) {
            // calculate the OUTPUT array
            output[counter[arr[i] - minNum] - 1] = arr[i];
            counter[arr[i] - minNum]--;
        }

        for (int i = 0; i < arr.length; i++) {
            arr[i] = output[i];
        }
    }
}