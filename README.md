# Insight_Challenge
This code uses predict.txt stock ID to find the match in actual.txt for each hour. After computing the error for each stock ID, I stock them in a list. I extend the list for the next hour till it reaches the window size.
The average is calculated and save to the list of results.
When the next hour of stock ID is extracted, it is extended to the bottom of the error window list. The top hour's error is removed from the error window.
By using this stacking method, a list of averages within a window is computed.
