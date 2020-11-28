Naive streaming engine:

Write a small framework that processes an endless event stream of integers. The assumption is that processing will be static and sequential, where each processing unit pass the output to the next processing unit, unless defined differently (e.g. filter, fixed-event-window). The program
should be a Console Application (c#/java) or a script file (python/node.js).

The framework should include the 6 following “building blocks”:
1. stdin-source: reads one number from stdin, prints ‘> ‘ and the number afterwards.  
For example, if the user entered 1, it will print "> 1"
2. filter: only passes events that match a predicate (a function that returns true or false given a number). The predicate is given during the initialization time of filter.
3. fixed-event-window: aggregates events into a fixed size array, pass it forward when full. The size of the fixed array is defined during the initialization of fixed-event-window.
4. fold-sum: sums the value of the events in the array, and pass forward the sum.
5. fold-median: calculate the median (ןויצח) value of the events in the array, and pass forward the median.
6. stdout-sink: prints the number to stdout and pass forward the number.

From these 6 building blocks, any pipeline can be built, here is one for example:  
stdin-source -> filter(i=>i>0) -> fixed-event-window(2) -> fold-sum -> fixed-event-window(3) -> fold-median -> stdout-sink

An example for an input by the user:
\> 1  
\> 2  
\> -5  
\> 3  
\> 4  
\> 5  
\> 6  
7 ← printed by stdout-sink  
\> 10  
\> 11  
\> 12  
\> 13  
\> 14  
\> 15  
??? ← what would be the value here?  

Your job is to implement the above while thinking of the following:

● No need to think of multithreading or multi-process solutions at this point.  
● How to design the system so it would be easy to add more building blocks later on.  
● How do you create the connection between the building blocks (passing values forward)  

Where needed, and go back to reading a number when a building block “decides” to stop processing the information (e.g. filter can decide not to pass the input if the predicate returns false on the input).
