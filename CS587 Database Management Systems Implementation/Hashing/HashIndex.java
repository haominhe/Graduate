package index;

import global.GlobalConst;
import global.Minibase;
import global.PageId;
import global.RID;
import global.SearchKey;


//CS 587
//Creators: Haomin He, Zicheng Ren



/**
 * <h3>Minibase Hash Index</h3>
 * This unclustered index implements static hashing as described on pages 371 to
 * 373 of the textbook (3rd edition).  The index file is a stored as a heapfile.  
 */
public class HashIndex implements GlobalConst {

  /** File name of the hash index. */
  protected String fileName;

  /** Page id of the directory. */
  protected PageId headId;
  
  //Log2 of the number of buckets - fixed for this simple index
  protected final int  DEPTH = 7;

  // --------------------------------------------------------------------------

  /**
   * Opens an index file given its name, or creates a new index file if the name
   * doesn't exist; a null name produces a temporary index file which requires
   * no file library entry and whose pages are freed when there are no more
   * references to it.
   * The file's directory contains the locations of the 128 primary bucket pages.
   * You will need to decide on a structure for the directory.
   * The library entry contains the name of the index file and the pageId of the
   * file's directory.
   */
  public HashIndex(String fileName) {

	  //throw new UnsupportedOperationException("Not implemented");
	  this.fileName = fileName;
	  boolean exists = false;
	  //**filename is not null, check if there exists a file in the library
	  if (fileName != null){
		  this.headId = Minibase.DiskManager.get_file_entry(fileName);
		  if (this.headId != null)
			  exists = true;
	  }
	  
	  
	  //**create a new index file if the name doesn't exist
	  if (exists == false) {
		  HashDirPage hdPg = new HashDirPage();
		  this.headId = Minibase.BufferManager.newPage(hdPg, 1);
		  Minibase.BufferManager.unpinPage(this.headId, UNPIN_DIRTY);
		  //**filename is not null, add to library
		  if (fileName != null)
			  Minibase.DiskManager.add_file_entry(fileName, this.headId);
	  }

  } // public HashIndex(String fileName)

  
  
  
  /**
   * Called by the garbage collector when there are no more references to the
   * object; deletes the index file if it's temporary.
   */
  protected void finalize() throws Throwable {

	  //throw new UnsupportedOperationException("Not implemented");
	  if (this.fileName == null)
		  deleteFile();

  } // protected void finalize() throws Throwable
  
  
  

   /**
   * Deletes the index file from the database, freeing all of its pages.
   */
  public void deleteFile() {

	  //throw new UnsupportedOperationException("Not implemented");
	  PageId dirId = new PageId(this.headId.pid);
	  HashBucketPage hbPg = new HashBucketPage();//**hold content of page in the bucket
	  HashDirPage dirPg = new HashDirPage();//**hold content of hash dirpage
	  //**traverse through hash dirpage and count entries for each directory
	  while (dirId.pid != INVALID_PAGEID){
		  Minibase.BufferManager.pinPage(dirId, dirPg, PIN_DISKIO);
		  int entryCnt = dirPg.getEntryCount();
		  for (int cnt = 0; cnt < entryCnt; ++cnt){
			  //**free all the pages in the entry
			  PageId idx = dirPg.getPageId(cnt);
			  while(idx.pid != INVALID_PAGEID){
				  Minibase.BufferManager.pinPage(idx, hbPg, PIN_DISKIO);
				  PageId nexthbId = hbPg.getNextPage();
				  Minibase.BufferManager.unpinPage(idx, UNPIN_CLEAN);
				  Minibase.BufferManager.freePage(idx);
				  idx = nexthbId;
			  }
		  }
		  PageId nextdirId = dirPg.getNextPage();
		  Minibase.BufferManager.unpinPage(dirId, UNPIN_CLEAN);
		  Minibase.BufferManager.freePage(dirId);
		  dirId = nextdirId;
	  }
	  //**if filename is valid, delete from library
	  if (this.fileName != null)
		  Minibase.DiskManager.delete_file_entry(this.fileName);
	  

  } // public void deleteFile()

  
  
  
  /**
   * Inserts a new data entry into the index file.
   * 
   * @throws IllegalArgumentException if the entry is too large
   */
  public void insertEntry(SearchKey key, RID rid) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //declare and initialize variables
	  PageId hashpageid = new PageId(headId.pid);//a head PageId is simply an integer
	  //a page in a linked list. The entire linked list is a hash table bucket
	  HashBucketPage hashbuckpage = new HashBucketPage();
	  //Hash directory pages simply contain page ids to data pages
	  HashDirPage hashdirpage = new HashDirPage();
	  //Gets the hash value for the search key, given the depth
	  int keyhash = key.getHash(DEPTH);
	  // temp next Id value
	  PageId tempnext = new PageId();
	  
	  //Constructs a DataEntry from the given values
	  DataEntry argentry = new DataEntry(key, rid);
	  //checking entry length, display IllegalArgumentException if the entry is too large
	  //MAX_ENTRY_SIZE = (PAGE_SIZE - HEADER_SIZE - SLOT_SIZE), it means the biggest size
	  //an entry could be
	  if(argentry.getLength() > SortedPage.MAX_ENTRY_SIZE) {
		  throw new IllegalArgumentException("The entry is too large");
	  }
	  
	  //MAX_ENTRIES = (PAGE_SIZE - HEADER_SIZE) / ENTRY_SIZE, it means how many entries can
	  //fit in one page
	  //if the hashed value >= to MAX_ENTRIES a page can hold
	  while(keyhash >= HashDirPage.MAX_ENTRIES){
		  //Pin the page: disk page number pageno should reside in a frame in the buffer 
		  //pool and have an additional pin assigned to it, and mempage should refer to 
		  //the contents of that frame.
		  //read the page from disk into the frame
		  Minibase.BufferManager.pinPage(hashpageid, hashbuckpage, PIN_DISKIO);
		  //Gets the next page's id in the hash bucket and assign it to the temp variable
		  tempnext = hashbuckpage.getNextPage();
		  //unpin the page:Unpins a disk page from the buffer pool, decreasing its pin count
		  //UNPIN_CLEAN: data is not modified 
		  Minibase.BufferManager.unpinPage(hashpageid, UNPIN_CLEAN);
		  //assign the current page id points to the next page id
		  hashpageid = tempnext;
		  //after we have brought in a new page, we decrement the keyhash value by the
		  //MAX_ENTRIES size, so that it points to the new created page
		  keyhash = keyhash - HashDirPage.MAX_ENTRIES;
	  }
	  
	  //pin the hashdirpage
	  Minibase.BufferManager.pinPage(hashpageid, hashdirpage, PIN_DISKIO);
	  //Gets the first page id of the bucket for the given hash value
	  PageId pageidbuck = hashdirpage.getPageId(keyhash);
	  //if the page id from the bucket is valid pin and unpin page
	  if(pageidbuck.pid != INVALID_PAGEID) {
		  Minibase.BufferManager.pinPage(pageidbuck, hashbuckpage, PIN_DISKIO);
		  Minibase.BufferManager.unpinPage(hashpageid, UNPIN_CLEAN);
	  }
	  //if it is not valid, allocate a new page with page number of one
	  else {
		  pageidbuck = Minibase.BufferManager.newPage(hashbuckpage, 1);
		  //Sets the first page id of the bucket for the given hash value
		  hashdirpage.setPageId(keyhash, pageidbuck);
		//UNPIN_DIRTY: data is modified 
		  Minibase.BufferManager.unpinPage(hashpageid, UNPIN_DIRTY);
	  }
	  
	  //insert a data entry into a bucket, apply insertEntry to the primary page of 
	  //the bucket, return true if inserting made this page dirty, false otherwise
	  //unpin the page after insertion
	  Minibase.BufferManager.unpinPage(pageidbuck, hashbuckpage.insertEntry(argentry));
  } // public void insertEntry(SearchKey key, RID rid)

  
  
  
  /**
   * Deletes the specified data entry from the index file.
   * 
   * @throws IllegalArgumentException if the entry doesn't exist
   */
  public void deleteEntry(SearchKey key, RID rid) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //declare and initialize variables
	  PageId hashpageid = new PageId(headId.pid);//a head PageId is simply an integer
	  //a page in a linked list. The entire linked list is a hash table bucket
	  HashBucketPage hashbuckpage = new HashBucketPage();
	  //Hash directory pages simply contain page ids to data pages
	  HashDirPage hashdirpage = new HashDirPage();
	  //Gets the hash value for the search key, given the depth
	  int keyhash = key.getHash(DEPTH);
	  // temp next Id value
	  PageId tempnext = new PageId();
	  //Constructs a DataEntry from the given values
	  DataEntry argentry = new DataEntry(key, rid);

	  
	  //MAX_ENTRIES = (PAGE_SIZE - HEADER_SIZE) / ENTRY_SIZE, it means how many entries can
	  //fit in one page
	  //if the hashed value >= to MAX_ENTRIES a page can hold
	  while(keyhash >= HashDirPage.MAX_ENTRIES){
		  //Pin the page: disk page number pageno should reside in a frame in the buffer 
		  //pool and have an additional pin assigned to it, and mempage should refer to 
		  //the contents of that frame.
		  //read the page from disk into the frame
		  Minibase.BufferManager.pinPage(hashpageid, hashdirpage, PIN_DISKIO);
		  //Gets the next page's id in the hash bucket and assign it to the temp variable
		  tempnext = hashdirpage.getNextPage();
		  //unpin the page:Unpins a disk page from the buffer pool, decreasing its pin count
		  //UNPIN_CLEAN: data is not modified 
		  Minibase.BufferManager.unpinPage(hashpageid, UNPIN_CLEAN);
		  //assign the current page id points to the next page id
		  hashpageid = tempnext;
		  //after we have brought in a new page, we decrement the keyhash value by the
		  //MAX_ENTRIES size, so that it points to the new created page
		  keyhash = keyhash - HashDirPage.MAX_ENTRIES;
	  }
	  //pin the hashdirpage
	  Minibase.BufferManager.pinPage(hashpageid, hashdirpage, PIN_DISKIO);
	  //Gets the first page id of the bucket for the given hash value
	  PageId pageidbuck = hashdirpage.getPageId(keyhash);
	  Minibase.BufferManager.unpinPage(hashpageid, UNPIN_CLEAN);
	  
	  //if the page id from the bucket is valid, try to pin the page
	  if(pageidbuck.pid != INVALID_PAGEID) {
		  Minibase.BufferManager.pinPage(pageidbuck, hashbuckpage, PIN_DISKIO);
	  }
	  //if it is not valid, throw exception if failed
	  else {
		  throw new IllegalArgumentException("The entry doesn't exist");
	  }
	  //try to delete the entry, throw exception if failed
	  try {
		  //To delete a data entry from a bucket, apply deleteEntry to the primary page of 
		  //the bucket, return true if deleting made this page dirty, false otherwise
		  //unpin the page after deletion
		  Minibase.BufferManager.unpinPage(pageidbuck, hashbuckpage.deleteEntry(argentry));
	  }catch(IllegalArgumentException e){
		  //deletion failed means the data is not modified
		  Minibase.BufferManager.unpinPage(pageidbuck, UNPIN_CLEAN);
		  throw e;
	  }
	   
  } // public void deleteEntry(SearchKey key, RID rid)

  
  
  
  /**
   * Initiates an equality scan of the index file.
   */
  public HashScan openScan(SearchKey key) {
    return new HashScan(this, key);
  }

  
  
  
  /**
   * Returns the name of the index file.
   */
  public String toString() {
    return fileName;
  }

  
  
  
  /**
   * Prints a high-level view of the directory, namely which buckets are
   * allocated and how many entries are stored in each one. Sample output:
   * 
   * <pre>
   * IX_Customers
   * ------------
   * 0000000 : 35
   * 0000001 : null
   * 0000010 : 27
   * ...
   * 1111111 : 42
   * ------------
   * Total : 1500
   * </pre>
   */
  public void printSummary() {

	  //throw new UnsupportedOperationException("Not implemented");

	  System.out.println();
	  //check if filename is valid
	  String validfilename = "empty string";
	  if(fileName == null) {
		  validfilename = "temp file name";
	  }else {
		  validfilename = this.fileName;
	  }
	  System.out.println(validfilename);
	  
	  for (int counter=0; counter < validfilename.length(); counter++){
		  System.out.print("-");		  
	  }
	  System.out.println();
	  
	  //declare and initialize variables
	  PageId hashpageid = new PageId(headId.pid);//a head PageId is simply an integer
	  //a page in a linked list. The entire linked list is a hash table bucket
	  HashBucketPage hashbuckpage = new HashBucketPage();
	  //Hash directory pages simply contain page ids to data pages
	  HashDirPage hashdirpage = new HashDirPage();
	  // temp next Id value
	  PageId tempnext = new PageId();
	  PageId temppageid = new PageId();
	  int counter1 =0;
	  String temp1;
	  
	  //if the page id from the bucket is valid, try to pin the page
	  while(hashpageid.pid != INVALID_PAGEID) {
		  Minibase.BufferManager.pinPage(hashpageid, hashdirpage, PIN_DISKIO);
		  //Gets the number of entries on the page
		  int numentry;
		  numentry = hashdirpage.getEntryCount();
		  for(int cnt = 0; cnt < numentry; cnt++) {
			  temp1 = Integer.toString(cnt, 2);
			  for(int cnt1 = 0; cnt1 < DEPTH - temp1.length(); cnt1++) {
				  System.out.print('0');
			  }//for2
			  System.out.print(temp1 + " : "); 
			  //Gets the first page id of the bucket for the given hash value
			  temppageid = hashdirpage.getPageId(cnt);
			  
			  //if the page id from the bucket is valid, try to pin the page
			  if(temppageid.pid != INVALID_PAGEID) {
				  Minibase.BufferManager.pinPage(temppageid, hashbuckpage, PIN_DISKIO);
				  //Gets the number of entries in this page and later
				  //(overflow) pages in the list.
				  System.out.println(hashbuckpage.countEntries());
				  counter1 = counter1 + (hashbuckpage.countEntries());
				  Minibase.BufferManager.unpinPage(temppageid, UNPIN_CLEAN);
			  }//if
			  else {
				  System.out.println("null");
			  }//else			  
		  }//for
		  //Gets the next page's id in the hash bucket and assign it to the temp variable
		  tempnext = hashdirpage.getNextPage();
		  //unpin the page:Unpins a disk page from the buffer pool, decreasing its pin count
		  //UNPIN_CLEAN: data is not modified 
		  Minibase.BufferManager.unpinPage(hashpageid, UNPIN_CLEAN);
		  //assign the current page id points to the next page id
		  hashpageid = tempnext;
		  
	  }//while
	  
	  for (int cnt2 = 0; cnt2 < validfilename.length(); cnt2++){
		  System.out.print('-');
	  }
	  System.out.println();
	  System.out.println("Total : "+ counter1);
	  
	  
  } // public void printSummary()

  
  
} // public class HashIndex implements GlobalConst





