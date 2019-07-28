package index;

import global.GlobalConst;
import global.Minibase;
import global.PageId;
import global.RID;
import global.SearchKey;


//CS 587
//Creators: Haomin He, Zicheng Ren



/**
 * A HashScan retrieves all records with a given key (via the RIDs of the records).  
 * It is created only through the function openScan() in the HashIndex class. 
 */
public class HashScan implements GlobalConst {

  /** The search key to scan for. */
  protected SearchKey key;

  /** Id of HashBucketPage being scanned. */
  protected PageId curPageId;

  /** HashBucketPage being scanned. */
  protected HashBucketPage curPage;

  /** Current slot to scan from. */
  protected int curSlot;

  // --------------------------------------------------------------------------

  /**
   * Constructs an equality scan by initializing the iterator state.
   */
  protected HashScan(HashIndex index, SearchKey key) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  
	  //build a hash directory pages contain page ids to data pages (i.e. buckets).
	  HashDirPage hashdpage = new HashDirPage();
	  //HashBucketPage being scanned
	  curPage = new HashBucketPage();
	  //initialize current slot to scan from, EMPTY_SLOT = -1
	  this.curSlot = EMPTY_SLOT;
	  
	  //initialize this search key with incoming argument key
	  //a search key consists of a type, a length and a value
	  this.key = new SearchKey(key);
	  //Gets the hash value for the search key, given the depth, depth is 7
	  //use this to find hash directory page in hashdpage
	  int searchkeyhashval = key.getHash(index.DEPTH);
	  
	  //get the pid of the head of the index
	  PageId indexpageid = new PageId(index.headId.pid);
	  
	  //HashScan.java should have at most one page pinned at any given time.
	  //Pin the page: disk page number pageno should reside in a frame in the buffer 
	  //pool and have an additional pin assigned to it, and mempage should refer to 
	  //the contents of that frame.
	  //read the page from disk into the frame
	  Minibase.BufferManager.pinPage(indexpageid, hashdpage, PIN_DISKIO);
	  
	  //get the first page id of HashBucketPage being scanned for the given hash value
	  curPageId = hashdpage.getPageId(searchkeyhashval);
	  //unpin the page:Unpins a disk page from the buffer pool, decreasing its pin count
	  //UNPIN_CLEAN: data is not modified 
	  Minibase.BufferManager.unpinPage(indexpageid, UNPIN_CLEAN);
	  
	  //check the being scanned hash bucket page's pid is valid or not
	  //if it is valid, pin being scanned id of hash bucket page in hash bucket page
	  //read the page from disk into the frame
	  if(curPageId.pid != INVALID_PAGEID) {
		  Minibase.BufferManager.pinPage(curPageId, curPage, PIN_DISKIO);
	  }

  } // protected HashScan(HashIndex index, SearchKey key)

  
  
  
  /**
   * Called by the garbage collector when there are no more references to the
   * object; closes the scan if it's still open.
   */
  protected void finalize() throws Throwable {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //check the being scanned hash bucket page's pid is valid or not
	  //if it is valid, closes the index scan, releasing any pinned pages.
	  if(curPageId.pid != INVALID_PAGEID) {
		 close();
	  }

  } // protected void finalize() throws Throwable

  
  
  
  /**
   * Closes the index scan, releasing any pinned pages.
   */
  public void close() {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //check the being scanned hash bucket page's pid is valid or not
	  //if it is valid, releasing any pinned pages and make the pid invalid
	  //UNPIN_CLEAN: data is not modified 
	  if(curPageId.pid != INVALID_PAGEID) {
			 Minibase.BufferManager.unpinPage(curPageId, UNPIN_CLEAN);
			 curPageId.pid = INVALID_PAGEID;
		  }

  } // public void close()

  
  
  
   /**
   * Gets the next entry's RID in the index scan.
   * 
   * @throws IllegalStateException if the scan has no more entries
   */
  public RID getNext() {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //A record is uniquely identified by its page number and slot number.
	  RID recordid = null;
	  //check the being scanned hash bucket page's pid is valid or not
	  //if it is valid, do index scan and see if there is next bucket
	  while(curPageId.pid != INVALID_PAGEID) {
		  //Searches for the next entry that matches the given search key, and stored
		  //after the given slot
		  this.curSlot = this.curPage.nextEntry(this.key, this.curSlot);
		  //if slot number of the entry is not found(-1)
		  if(this.curSlot <= -1) {
			  //Gets the next page's id.
			  PageId nextId = this.curPage.getNextPage();
			  //unpin the current page id without any modifications
		      Minibase.BufferManager.unpinPage(this.curPageId, UNPIN_CLEAN);
		      //make the current page id points to the next page id
		      this.curPageId = nextId;
		      //if the next page id'pid is valid
		      //pin the current page id in current page, read the page from disk into the frame
		      if (this.curPageId.pid != INVALID_PAGEID) {
		          Minibase.BufferManager.pinPage(this.curPageId, this.curPage, PIN_DISKIO);
		      }
		  }//if curSlot = -1
		  //if we can find slot number of the entry
		  else {
			  try {
				  //Gets record id of the data entry at the given slot number
				  recordid = new RID(this.curPage.getEntryAt(this.curSlot).rid);
			  } catch(IllegalStateException ex){
				  //throw IllegalStateException if the scan has no more entries
				  throw new IllegalStateException("the scan has no more entries");
			  }//catch
		  }//else
	  }//while
	  
	  return recordid;
  } // public RID getNext()

  
  
  
} // public class HashScan implements GlobalConst












