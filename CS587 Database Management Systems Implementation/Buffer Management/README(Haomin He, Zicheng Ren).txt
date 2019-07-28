CS 587 
Creators: Haomin He, Zicheng Ren

We build our project based on instructions from BufferManagerAssignment-Win2018.pdf. We started out reading through the diskmgr.java, minibase.java, page.java, PageId.java, to get ourselves familiar with how the lower layer (disk manager) works and how it communicates with buffer manager. We started by looking into the BMTest.java file and stepping through the test code to find out the input and output of each function. 

The test calls newPage() function first so we try to make connections among the classes, packages to implement newPage(). 

newPage() calls for pinPage(), so pinPage() is connected with newPage() closely. newPage() hands over the first page that needs to be pinned to pinPage(). 

pinPage() modifies the page's parameters and its Framedesc's members. The modified page is returned back to newPage() and newPage() returns the value back to the test. 

unpinPage() decreases the pincount of a page by 1 and set on or off (according to the parameter dirty) for the frame that the page resides in. But it does not result in writing the dirty page onto disk right away.

freePage() deallocates a page who is valid by calling Minibase.DiskManager.deallocate_page() to remove it from the pool and reset the page to 0. If the page is pinned throw error, if not reset the the page's FrameDesc info.

flushPage() writes a dirty page to disk by calling Minibase.DiskManager.write_page() and resets the page pincount to 0.

flushAllFrames() calls flushPage() iteratively. 

getNumFrames() returns the size of the buffer pool.

getNumUnpinned() returns the total number of pages who has pincount 0.

We implemented FrameDesc class to hold each page's parameters. It's used to access the information such as a page's pincount, pageid refbit and dirty bit.

We also implmented Clock class for the buffer pool page replacement. It has a pickVictim() method that is used to return a chosen page number (integer) or -1 if no page could be chosen. It is called in pinPage(), unpinPage() and freePage() from the buffer manager class to set the refbit to true or false accordingly.

For the debugging purpose we first set a small amount of int toAlloc (we set it to 5) and printed out the page number along with page content. We expected the our test results to be 0, 1, 2, 3, 4 for page numbers and 99999, 100000, 100001, 100002, 100003 for the data on the page. This way we are certain that the pageid.pid (key in the hashmap) is increased along with the FrameDesc (value in the hashmap) and what is read off of page is what we have written into the page. We follow the pseudo code from the pdf file to implement the clock algorithm. 

Clock.java has a main function called pickVictim() which return a victim page number (an integer) back to pinPage() to replace with. 

References:
BufferManagerAssignment-Win2018.pdf
Ramakrishnan, Gehrke - Database Management Systems
https://en.wikipedia.org/wiki/Page_replacement_algorithm
https://github.com/dhanukarajat/buffer-manager
https://github.com/nikpawar89/Minbase
https://github.com/yawen214/BufferManager
https://github.com/munafahad/bufferManager
https://github.com/Elessawy/BufferManager
https://github.com/iyanuobidele/buffer-manager

