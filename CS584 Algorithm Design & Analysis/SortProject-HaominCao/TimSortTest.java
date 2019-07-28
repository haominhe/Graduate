
/* 
CS 584: Algorithm Design and Analysis
Final Project
Haomin He Cao
June 2019

Comparison of Sorting Algorithms - TimSort 

References: 
https://www.geeksforgeeks.org/timsort/
https://github.com/JaKamb/Assignment_1
https://www.techiedelight.com/check-array-sorted-java/
https://www.techiedelight.com/merge-sort/
https://github.com/enriquegeorg/timsorte
*/



import java.io.*;
import java.util.*;

public class TimSortTest {
    
    // isSorted function checks whether the specified array is sorted
    // according to natural ordering or not. An array is considered sorted
    // if any successor has a less value than its predecessor.
    public static boolean isSorted(int[] a) {
        for (int i = 0; i < a.length - 1; i++) {
            if (a[i] > a[i + 1]) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // initialize
        TimSort sort = new TimSort();
        int MAX = 5001;
        Random random = new Random();
        System.out.println(
                "*** This program sorts an array of random integers between -5000 to 5000 by using Timsort algorithm.");

        long startSmall = System.nanoTime();
        int smallArray[] = new int[25];
        for (int n = 0; n <= 24; n++) {
            int nnum = (int) (random.nextInt(MAX) * (random.nextBoolean() ? -1 : 1));
            smallArray[n] = nnum;
        }
        // before TimSort
        // System.out.println(Arrays.toString(smallArray));
        sort.TimSort(smallArray, smallArray.length);
        // after TimSort
        // System.out.println();
        // System.out.println(Arrays.toString(smallArray));

        System.out.println();
        System.out.println("*** TimSort Test 1: Small size array. There are 25 integers in the array.");

        if (isSorted(smallArray)) {
            System.out.println("TimSort on small size array SUCCESSFULLY performed.");
        } else {
            System.out.println("TimSort on small size array FAILED.");
        }

        long endSmall = System.nanoTime();
        float secSmall = (endSmall - startSmall);
        System.out.println("Used time in nanoseconds: " + secSmall);

        // Get the Java runtime
        Runtime runtimeSmall = Runtime.getRuntime();
        // Run the garbage collector
        runtimeSmall.gc();
        // Calculate the used memory
        long memorySmall = runtimeSmall.totalMemory() - runtimeSmall.freeMemory();
        System.out.println("Used memory in bytes: " + memorySmall);





        long startMedium = System.nanoTime();
        int MediumArray[] = new int[500];
        for (int l = 0; l <= 499; l++) {
            int lnum = (int) (random.nextInt(MAX) * (random.nextBoolean() ? -1 : 1));
            MediumArray[l] = lnum;
        }
        // before TimSort
        // System.out.println(Arrays.toString(MediumArray));
        sort.TimSort(MediumArray, MediumArray.length);
        // after TimSort
        // System.out.println();
        // System.out.println(Arrays.toString(MediumArray));

        System.out.println();
        System.out.println("*** TimSort Test 2: Medium size array. There are 500 integers in the array.");

        if (isSorted(MediumArray)) {
            System.out.println("TimSort on medium size array SUCCESSFULLY performed.");
        } else {
            System.out.println("TimSort on medium size array FAILED.");
        }

        long endMedium = System.nanoTime();
        float secMedium = (endMedium - startMedium);
        System.out.println("Used time in nanoseconds: " + secMedium);

        // Get the Java runtime
        Runtime runtimeMedium = Runtime.getRuntime();
        // Run the garbage collector
        runtimeMedium.gc();
        // Calculate the used memory
        long memoryMedium = runtimeMedium.totalMemory() - runtimeMedium.freeMemory();
        System.out.println("Used memory in bytes: " + memoryMedium);




        long startBig = System.nanoTime();
        int bigArray[] = new int[10000];
        for (int m = 0; m <= 9999; m++) {
            int mnum = (int) (random.nextInt(MAX) * (random.nextBoolean() ? -1 : 1));
            bigArray[m] = mnum;
        }
        // before TimSort
        // System.out.println(Arrays.toString(bigArray));
        sort.TimSort(bigArray, bigArray.length);
        // after TimSort
        // System.out.println();
        // System.out.println(Arrays.toString(bigArray));

        System.out.println();
        System.out.println("*** TimSort Test 3: Big size array. There are 10,000 integers in the array.");

        if (isSorted(bigArray)) {
            System.out.println("TimSort on big size array SUCCESSFULLY performed.");
        } else {
            System.out.println("TimSort on big size array FAILED.");
        }

        long endBig = System.nanoTime();
        float secBig = (endBig - startBig);
        System.out.println("Used time in nanoseconds: " + secBig);

        // Get the Java runtime
        Runtime runtimeBig = Runtime.getRuntime();
        // Run the garbage collector
        runtimeBig.gc();
        // Calculate the used memory
        long memoryBig = runtimeBig.totalMemory() - runtimeBig.freeMemory();
        System.out.println("Used memory in bytes: " + memoryBig);
    }

}