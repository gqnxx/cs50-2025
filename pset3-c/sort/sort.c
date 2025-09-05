// CS50 pset3: Sort - Analysis of sorting algorithms
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Sort analysis: This program should contain the results of analyzing
    // the timing of different sorting algorithms on different inputs
    
    printf("sort1 uses: Bubble Sort\n");
    printf("sort2 uses: Merge Sort\n"); 
    printf("sort3 uses: Selection Sort\n");
    
    /*
    Analysis based on timing results:
    
    - sort1 (Bubble Sort): 
      * Best case O(n) when array is already sorted
      * Worst case O(n²) when array is reverse sorted
      * Shows significant improvement on sorted arrays
    
    - sort2 (Merge Sort):
      * Consistent O(n log n) performance
      * Similar timing regardless of input order
      * Most efficient for large datasets
    
    - sort3 (Selection Sort):
      * Always O(n²) regardless of input
      * No improvement on pre-sorted arrays
      * Slowest overall performance
    */
    
    return 0;
}
