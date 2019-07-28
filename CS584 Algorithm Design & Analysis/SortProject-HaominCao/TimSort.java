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

public class TimSort {
	static int RUN = 64;

	// iterative Timsort function to sort the array[0...n-1] (similar to merge sort)
	public static void TimSort(int[] array, int n) {

		// Sort individual subarrays of size RUN
		for (int i = 0; i < n; i += RUN) {
			insertionSort(array, i, Math.min((i + RUN - 1), (n - 1)));
		}

		// start merging from size RUN (or 64). It will merge to form size 64, then 128,
		// 256 and so on ....
		for (int size = RUN; size < n; size = 2 * size) {
			// pick starting point of left sub array.
			// merge array[left..left+size-1] and array[left+size, left+2*size-1]
			// After every merge, increase left by 2*size
			for (int left = 0; left < n; left += 2 * size) {
				// find ending point of left sub array
				// mid+1 is starting point of right sub array
				int mid = left + size - 1;
				// make sure mid is not out of bound
				if (mid > n) {
					mid = n - 1;
				}
				int right = Math.min((left + 2 * size - 1), (n - 1));
				// merge sub array array[left.....mid] & array[mid+1....right]
				mergeSort(array, left, mid, right);
			}
		}
	}




	// this function sorts array from left index to right index. Array size is
	// atmost RUN
	public static void insertionSort(int[] array, int left, int right) {
		int currentVal;
		int j;
		for (int i = left + 1; i <= right; i++) {
			// current
			currentVal = array[i];
			// previous
			j = i - 1;
			// make sure index is greater than zero
			while (j >= 0 && array[j] > currentVal && j >= left) {
				array[j + 1] = array[j];
				j--;
			}
			array[j + 1] = currentVal;
		}
	}




	// this function merges the sorted runs/subarrays
	public static void mergeSort(int[] array, int leftPoint, int midPoint, int rightPoint) {
		// original array is broken in two parts left and right array
		int leftPart = midPoint - leftPoint + 1;
		int rightPart = rightPoint - midPoint;

		int[] left = new int[leftPart];
		int[] right = new int[rightPart];
		for (int count = 0; count < leftPart; count++) {
			left[count] = array[leftPoint + count];
		}
		for (int count2 = 0; count2 < rightPart; count2++) {
			right[count2] = array[midPoint + 1 + count2];
		}

		int templeft = 0;
		int tempright = 0;
		int target = leftPoint;

		// after comparing, we merge those two arrays in a larger sub array
		while (templeft < leftPart && tempright < rightPart) {
			if (left[templeft] <= right[tempright]) {
				array[target] = left[templeft];
				templeft++;
			} else {
				array[target] = right[tempright];
				tempright++;
			}
			target++;
		}
		// copy remaining elements of left, if any
		while (templeft < leftPart) {
			array[target] = left[templeft];
			target++;
			templeft++;
		}
		// copy remaining element of right, if any
		while (tempright < rightPart) {
			array[target] = right[tempright];
			target++;
			tempright++;
		}
	}

}