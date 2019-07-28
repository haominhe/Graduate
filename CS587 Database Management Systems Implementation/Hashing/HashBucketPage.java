package index;

import global.Minibase;
import global.PageId;


//CS 587
//Creators: Haomin He, Zicheng Ren



/**
 * An object in this class is a page in a linked list.
 * The entire linked list is a hash table bucket.
 */
class HashBucketPage extends SortedPage {

  /**
   * Gets the number of entries in this page and later
   * (overflow) pages in the list.
   * <br><br>
   * To find the number of entries in a bucket, apply 
   * countEntries to the primary page of the bucket.
   */
  public int countEntries() {

	  //throw new UnsupportedOperationException("Not implemented");
	  PageId pgId = getNextPage();//**called from SortedPage
	  HashBucketPage mempg = new HashBucketPage();//**hold the content of the page
	  int entryCnt = getEntryCount(); //**called from SortedPage
	  //**add up the entrycnt for each page
	  while(pgId.pid != INVALID_PAGEID){
		  Minibase.BufferManager.pinPage(pgId, mempg, PIN_DISKIO);
		  entryCnt += mempg.getEntryCount();
		  PageId nextpgId = mempg.getNextPage();
		  Minibase.BufferManager.unpinPage(pgId, UNPIN_CLEAN);
		  pgId = nextpgId;
	  }
	  
	  return entryCnt;
	  

  } // public int countEntries()

  /**
   * Inserts a new data entry into this page. If there is no room
   * on this page, recursively inserts in later pages of the list.  
   * If necessary, creates a new page at the end of the list.
   * Does not worry about keeping order between entries in different pages.
   * <br><br>
   * To insert a data entry into a bucket, apply insertEntry to the
   * primary page of the bucket.
   * 
   * @return true if inserting made this page dirty, false otherwise
   */
  public boolean insertEntry(DataEntry entry) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  try{
		  super.insertEntry(entry);
		  return true; 
	  }
	  catch(IllegalStateException illegalstate){
		  PageId pgId = getNextPage();
		  HashBucketPage memPg = new HashBucketPage();
		  //**if the next page is invalid, add a new page at the end of the list.
		  if (pgId.pid == INVALID_PAGEID){
			  pgId = Minibase.BufferManager.newPage(memPg, 1);
			  setNextPage(pgId);//**called from SortedPage
			  boolean dirty = memPg.insertEntry(entry);//**insert the entry into the page
			  Minibase.BufferManager.unpinPage(pgId, dirty);//**if dirty true, write it to disk
			  return true;
		  }
		  //**if the page is valid, insert entry in this page
		  if (pgId.pid != INVALID_PAGEID){
			  Minibase.BufferManager.pinPage(pgId, memPg, PIN_DISKIO);
			  boolean dirty = memPg.insertEntry(entry);
			  Minibase.BufferManager.unpinPage(pgId, dirty);
			  return false;
		  }
		  throw illegalstate;  
	  }

  } // public boolean insertEntry(DataEntry entry)

  /**
   * Deletes a data entry from this page.  If a page in the list 
   * (not the primary page) becomes empty, it is deleted from the list.
   * 
   * To delete a data entry from a bucket, apply deleteEntry to the
   * primary page of the bucket.
   * 
   * @return true if deleting made this page dirty, false otherwise
   * @throws IllegalArgumentException if the entry is not in the list.
   */
  public boolean deleteEntry(DataEntry entry) {

	  //throw new UnsupportedOperationException("Not implemented");
	  try{
		  super.deleteEntry(entry);//**delete entry from bucket
		  return true;
	  }
	  catch(IllegalArgumentException illegalstate){
		  PageId pgId = getNextPage(); //**called from SortedPage
		  HashBucketPage memPg = new HashBucketPage();
		  //**look for the next page for the entry
		  if (pgId.pid != INVALID_PAGEID) {
			  Minibase.BufferManager.pinPage(pgId, memPg, PIN_DISKIO);
			  boolean dirty = memPg.deleteEntry(entry);//**called from SortedPage
			  if (memPg.getEntryCount() == 0){
				  //**delete the empty page and point to the next page
				  setNextPage(memPg.getNextPage());
				  Minibase.BufferManager.unpinPage(pgId, dirty);
				  Minibase.BufferManager.freePage(pgId);
				  return true;
			  }
			  Minibase.BufferManager.unpinPage(pgId, dirty);
			  return false;
		  }
		  throw illegalstate;
	  }
	  

  } // public boolean deleteEntry(DataEntry entry)

} // class HashBucketPage extends SortedPage