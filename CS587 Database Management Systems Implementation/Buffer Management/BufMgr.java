package bufmgr;

import global.GlobalConst;
import global.Minibase;
import global.Page;
import global.PageId;

import java.util.HashMap;

//CS 587 
//Creators: Haomin He, Zicheng Ren

/**
 * <h3>Minibase Buffer Manager</h3>
 * The buffer manager manages an array of main memory pages.  The array is
 * called the buffer pool, each page is called a frame.  
 * It provides the following services:
 * <ol>
 * <li>Pinning and unpinning disk pages to/from frames
 * <li>Allocating and deallocating runs of disk pages and coordinating this with
 * the buffer pool
 * <li>Flushing pages from the buffer pool
 * <li>Getting relevant data
 * </ol>
 * The buffer manager is used by access methods, heap files, and
 * relational operators.
 */
public class BufMgr implements GlobalConst {

//**our code
	// defined as protected since they are only accessed within this subclass
    // array of Pages
    protected Page[] bufpool;
    // array of descriptors containing parameters such as pin counts, dirty bit
    protected FrameDesc[] frametab;
    // map current page number to frame
    protected HashMap<Integer, FrameDesc> bufmap;
    // clock replacement policy
    protected Clock clock;   
//**our code
    
  /**
   * Constructs a buffer manager by initializing member data.  
   * 
   * @param numframes number of frames in the buffer pool
   */
  public BufMgr(int numframes) {

    //throw new UnsupportedOperationException("Not implemented");
    //**numbframes is defined in TestDriver
	bufpool = new Page[numframes];//**initialize bufpool 100 init size
	frametab = new FrameDesc[numframes];//**initialize frametab 10000 init size
	
	//** Initialize each frametab and bufferpool!!! 
	for (int i=0; i<numframes; i++) {
		bufpool[i] = new Page();
		frametab[i] = new FrameDesc(i);
	}
	
	bufmap = new HashMap<Integer, FrameDesc>(numframes);//**initialize bufmap same of the above
	clock = new Clock(this);//**initialize replace policy class
	
  } // public BufMgr(int numframes)

  /**
   * The result of this call is that disk page number pageno should reside in
   * a frame in the buffer pool and have an additional pin assigned to it, 
   * and mempage should refer to the contents of that frame. <br><br>
   * 
   * If disk page pageno is already in the buffer pool, this simply increments 
   * the pin count.  Otherwise, this<br> 
   * <pre>
   * 	uses the replacement policy to select a frame to replace
   * 	writes the frame's contents to disk if valid and dirty
   * 	if (contents == PIN_DISKIO)
   * 		read disk page pageno into chosen frame
   * 	else (contents == PIN_MEMCPY)
   * 		copy mempage into chosen frame
   * 	[omitted from the above is maintenance of the frame table and hash map]
   * </pre>		
   * @param pageno identifies the page to pin
   * @param mempage An output parameter referring to the chosen frame.  If
   * contents==PIN_MEMCPY it is also an input parameter which is copied into
   * the chosen frame, see the contents parameter. 
   * @param contents Describes how the contents of the frame are determined.<br>  
   * If PIN_DISKIO, read the page from disk into the frame.<br>  
   * If PIN_MEMCPY, copy mempage into the frame.<br>  
   * If PIN_NOOP, copy nothing into the frame - the frame contents are irrelevant.<br>
   * Note: In the cases of PIN_MEMCPY and PIN_NOOP, disk I/O is avoided.
   * @throws IllegalArgumentException if PIN_MEMCPY and the page is pinned.
   * @throws IllegalStateException if all pages are pinned (i.e. pool is full)
   */
 
public void pinPage(PageId pageno, Page mempage, int contents) { 

	//**throw new UnsupportedOperationException("Not implemented");
	  
	//**(Cited from the hint from doc)Suppose you've selected a victim page for replacement in the
	//frame table. You've done the work needed to set the frame up, and you insert it into bufmap 
	//with the pageno PageId reference we received as an argument as the key.
	//FrameDesc frameno = bufmap.put(pageno, victim_page);**
	
	FrameDesc frameno = bufmap.get(pageno.pid); //**get the value of key pageno.pid and store it into frameno
	//test// System.out.println(bufmap.get(pageno.pid));
	//**If disk page pageno is already in the buffer pool, this simply increments the pin count.
	if (frameno != null) {
		if (contents == PIN_MEMCPY){
			throw new IllegalArgumentException("PIN_MEMCPY and the page is pinned.");
		}
		//if (contents == PIN_NOOP) {
		else {
			frameno.setPinCount(frameno.getPinCount()+1); //**increment pincount by 1
			mempage.setPage(bufpool[frameno.idx]); //**
			clock.pinned(frameno); //**set refbit for clock object
			return;
		}
	} //frameno != null
	
	//**if disk page pageno is not in the buffer pool, uses the replacement policy to select 
	//**a frame to replace, writes the frame's contents to disk if valid and dirty
	//**PIN_DISKIO, read the page from disk into the frame
	if (frameno == null){
		
		int victim_page_no = (int) clock.pickVictim(); //**call clock to replace a page in pool
			
		//**the case of returning no available page to replace
		//**if (victim_page_no == INVALID_PAGEID && contents != PIN_MEMCPY){
		if (victim_page_no == INVALID_PAGEID){
			throw new IllegalStateException("all pages are pinned (i.e. pool is full)");
		}
		//**found a victim page
		//**FrameDesc victim_page = frametab[victim_page_no];
		frameno = frametab[victim_page_no];
		//**bufmap.put(pageno.pid, victim_page);

		//**if the victim page index is valid
		//**if (victim_page_no != INVALID_PAGEID && contents != PIN_MEMCPY){
		if (frameno.pageno.pid != INVALID_PAGEID){
			bufmap.remove(frameno.pageno.pid); //**remove the key value pair in the hashmap
			//**write the page to disk if the page is dirty
			if(frameno.checkDirty() == true){
				Minibase.DiskManager.write_page(frameno.pageno, bufpool[victim_page_no]);
			}
		}
		//**PIN_MEMCPY copy mempage into chosen frame
		//**if (victim_page_no != INVALID_PAGEID && contents == PIN_MEMCPY){
		if (contents == PIN_MEMCPY){
			//System.out.println(victim_page_no);//**test purpose
			//System.out.println(bufpool[victim_page_no]);//**test purpose
			bufpool[victim_page_no].copyPage(mempage);
			
		}
		//**PIN_DISKID read a page from disk to the frame
		//if (contents == PIN_DISKIO){
		else {
			Minibase.DiskManager.read_page(pageno, bufpool[victim_page_no]);
		}
		
		//**initialize the frame and page since we are getting a new comer
		//System.out.println(pageno.pid);//**test purpose
		
		frameno.pageno.pid = pageno.pid; //**assign the new page id to frame pageid pid
		//System.out.println(frameno);//**test purpose
		frameno.setPinCount(1); //**pincount is 1 because it just got loaded in
		
		bufmap.put(pageno.pid, frameno);
		mempage.setPage(bufpool[victim_page_no]); //**init a page space in the frame where the victim resided in
		clock.pinned(frameno);//**update refbit for clock obj
			
	} //frameno == null
	
  } // public void pinPage(PageId pageno, Page page, int contents)
  



  /**
   * Unpins a disk page from the buffer pool, decreasing its pin count.
   * 
   * @param pageno identifies the page to unpin
   * @param dirty UNPIN_DIRTY if the page was modified, UNPIN_CLEAN otherwise
   * @throws IllegalArgumentException if the page is not in the buffer pool
   *  or not pinned
   */
  public void unpinPage(PageId pageno, boolean dirty) {

    //**throw new UnsupportedOperationException("Not implemented");
	
	FrameDesc frameno = bufmap.get(pageno.pid);//**first check the incoming pageno if it's in pool
	//frameno.dirty = dirty;
	if (frameno == null){
		throw new IllegalArgumentException("the page is not in the buffer pool");
	}
	if (frameno != null) {
		//frameno.dirty = dirty;
		if (frameno.getPinCount() >= 0){
			frameno.setPinCount(frameno.getPinCount() - 1);//**decrease pincount by 1 
			frameno.dirty = dirty; //**if boolean dirty is set on meaning we need to set dirty check in frame
			//if (frameno.getPinCount() <= 0) {clock.unpinned(frameno);}
			clock.unpinned(frameno);
			return;
		}
	}

  } // public void unpinPage(PageId pageno, boolean dirty)
  
  
  
  
  /**
   * Allocates a run of new disk pages and pins the first one in the buffer pool.
   * The pin will be made using PIN_MEMCPY.  Watch out for disk page leaks.
   * 
   * @param firstpg input and output: holds the contents of the first allocated page
   * and refers to the frame where it resides
   * @param run_size input: number of pages to allocate
   * @return page id of the first allocated page
   * @throws IllegalArgumentException if firstpg is already pinned
   * @throws IllegalStateException if all pages are pinned (i.e. pool exceeded)
   */
  public PageId newPage(Page firstpg, int run_size) {

    //throw new UnsupportedOperationException("Not implemented");
	//**allocate a run_size (to_Alloc from BMTest) of disk pages, call diskMgr allocate_page()
	//** and it returns The id of the first page in the run
	PageId allopid =  Minibase.DiskManager.allocate_page(run_size);
	
	//**pin the first page by calling pinPage() with PIN_MEMCPY (value is 10) on pageid, not sure about what disk page leaks means
	
	pinPage(allopid, firstpg, PIN_MEMCPY); 
	//throw an exception, but that's the right behavior
	
	//**return the pid of the fist allocated page
	return allopid;
  } // public PageId newPage(Page firstpg, int run_size)

  
  
  /**
   * Deallocates a single page from disk, freeing it from the pool if needed.
   * 
   * @param pageno identifies the page to remove
   * @throws IllegalArgumentException if the page is pinned
   */
  public void freePage(PageId pageno) {

    //throw new UnsupportedOperationException("Not implemented");
	
	FrameDesc frameno = bufmap.get(pageno.pid);//**find out the new comer's page id if it's in the frame
	//**if it's not in any frame, can't be freed, throw error
	/*if (frameno == null){
		throw new IllegalArgumentException("cannot be freed, it's not in the pool");
	}*///**block for test
	//**if it's in the frame, free the page except the pincount is not 0
	if (frameno != null) {
		if (frameno.pincount != 0){
			throw new IllegalArgumentException("page is pinned");
		}
		else{
			frameno.pageno.pid = INVALID_PAGEID;//**set the page id in that frame as -1 (invalid)
			frameno.pincount = 0;
			bufmap.remove(pageno.pid);//**get rid of the frame in the hashmap
			clock.freepage(frameno);//**set refbit for clock obj
		}
		Minibase.DiskManager.deallocate_page(pageno);//**remove it from the pool and reset the page to 0
		
	}

  } // public void freePage(PageId firstid)

  
  
  
  /**
   * Write all valid and dirty frames to disk.
   * Note flushing involves only writing, not unpinning or freeing
   * or the like.
   * 
   */
  public void flushAllFrames() {

    //**throw new UnsupportedOperationException("Not implemented");
	
	//** flushAllFrames() calls flushPage(), flushPage() does the dirty work
	for (int i = 0; i < frametab.length; i++){
		flushPage(frametab[i].pageno); //**iterate through bufpool, flush every dirty page detected
	}
	//**test if there's still page pinned after flushing
	/*if (this.getNumUnpinned() != 0) {
		System.out.println("there are page still pinned");
	}*/

  } // public void flushAllFrames()

  
  
  /**
   * Write a page in the buffer pool to disk, if dirty.
   * 
   * @throws IllegalArgumentException if the page is not in the buffer pool
   */
  public void flushPage(PageId pageno) {
	  
	//**throw new UnsupportedOperationException("Not implemented");
	
	//**call for Minibase.DiskManager.write_page() to write the dirty page back to disk
	for (int i = 0; i < frametab.length; i++){
		if ((pageno == null || frametab[i].pageno.pid == pageno.pid) && frametab[i].dirty){
			//System.out.println(pageno.pid);//**test purpose
			frametab[i].pincount = 0; //reset pin count to 0
			Minibase.DiskManager.write_page(frametab[i].pageno, bufpool[i]);//**bufpool[i] holds the content, ->mempage
		}
	}
    
  }

   /**
   * Gets the total number of buffer frames.
   */
  public int getNumFrames() {
    //throw new UnsupportedOperationException("Not implemented");
    return bufpool.length; //**the array length is the number of frames, handed over to allocated pages in the test
  }

  /**
   * Gets the total number of unpinned buffer frames.
   */
  public int getNumUnpinned() {
    //throw new UnsupportedOperationException("Not implemented");
	//**iterate through bufpool and check the each frame's pincount, count up if pincount is 0
	int unpin_cnts = 0; //**to be returned
	for (int i = 0; i < bufpool.length; i++){
		if (frametab[i].pincount == 0){
			unpin_cnts +=1;
		}
	}
	return unpin_cnts;
  }

} // public class BufMgr implements GlobalConst
