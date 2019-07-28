package heap; 

import global.GlobalConst;
import global.Minibase;
import global.Page;
import global.PageId;
import global.RID;

//CS 587 
//Creators: Haomin He, Zicheng Ren

/**
 * <h3>Minibase Heap Files</h3>
 * A heap file is the simplest database file structure.  It is an unordered 
 * set of records, stored on a set of data pages. <br>
 * This class supports inserting, selecting, updating, and deleting
 * records.<br>
 * Normally each heap file has an entry in the database's file library.
 * Temporary heap files are used for external sorting and in other
 * relational operators. A temporary heap file does not have an entry in the
 * file library and is deleted when there are no more references to it. <br>
 * A sequential scan of a heap file (via the HeapScan class)
 * is the most basic access method.
 */
public class HeapFile implements GlobalConst {

  /** HFPage type for directory pages. */
  protected static final short DIR_PAGE = 10;

  /** HFPage type for data pages. */
  protected static final short DATA_PAGE = 11;

  private static final short MAX_ENTRIES = 0;

  // --------------------------------------------------------------------------

  /** Is this a temporary heap file, meaning it has no entry in the library? */
  protected boolean isTemp;

  /** The heap file name.  Null if a temp file, otherwise 
   * used for the file library entry. 
   */
  protected String fileName;

  /** First page of the directory for this heap file. */
  protected PageId headId;

  // --------------------------------------------------------------------------

  /**
   * If the given name is in the library, this opens the corresponding
   * heapfile; otherwise, this creates a new empty heapfile. 
   * A null name produces a temporary file which
   * requires no file library entry.
   */
  public HeapFile(String name) {
	  
	  fileName = name;
	  //**given name is in the library
	  if (name != null) {
		  isTemp = false;
          headId = Minibase.DiskManager.get_file_entry(name);
	  } //if (name != null) 
	//**if name is null, meaning the file is not in the library
	  else {
		//this.isTemp = true;
		  isTemp = true;
		  //this.fileName = null;
		  fileName = null;
	  } // else (name == null)
	  
	  //**if headId is null, meaning the file is not in the library, 
	  //**this creates a new empty heapfile.
	  if (headId == null){
		  DirPage dirPage = new DirPage(); //**create new dirpage
          headId = Minibase.BufferManager.newPage(dirPage, 1); //**get new page from pool
          dirPage.setCurPage(headId);//**set current dirpage pageno
          Minibase.BufferManager.unpinPage(headId, UNPIN_DIRTY); //**unpin the page from pool
          // If it is not a temp file, add its name and start page number
          if(!isTemp) {
        	  Minibase.DiskManager.add_file_entry(name, headId);
          }//!isTemp
	  }
	  
  } // public HeapFile(String name)

  
  
  
  /**
   * Called by the garbage collector when there are no more references to the
   * object; deletes the heap file if it's temporary.
   */
  protected void finalize() throws Throwable {//**Throwable may give not only exception but also errors

	    //throw new UnsupportedOperationException("Not implemented");
	  
	  //**handled by garbage collector from object class, override it by adding deleting temp heap file
	  if (isTemp == true){
		  deleteFile();//**call deleteFile() to delete temporary.
	  }

  } // protected void finalize() throws Throwable

  
  
  
  
  /**
   * Deletes the heap file from the database, freeing all of its pages
   * and its library entry if appropriate.
   */
  public void deleteFile() {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**we need to delete heap file by scanning total entries and counting how entries
	  //**occupied and freeing each occupied page that resizes in the entry.
	  PageId dirCurId = new PageId(headId.pid);//**locate the head dirpage of heapfile
	  DirPage curDirPg = new DirPage(); //**hold the content of the page
	  PageId dirNextId; //**next directory page
	  
	  //**existing heap file in system, need to remove
	  if (isTemp == false){
		  Minibase.DiskManager.delete_file_entry(fileName);//**call delete_file_entry(String fname) from DiskMgr.java
	  }
	  
	  //**free all of heap file pages from database
	  while (dirCurId != null) {
		  //**read the heap file into pool
		  Minibase.BufferManager.pinPage(dirCurId, curDirPg, PIN_DISKIO);
		  //**count how many pages held in curDirPg
		  int entryCnts = curDirPg.getEntryCnt();
		  //**free all the pages from the entries by calling BufMgr freePage
		  for (int i = 0; i < entryCnts; i++){
			  Minibase.BufferManager.freePage(curDirPg.getPageId(i));
		  }
		  dirNextId = curDirPg.getNextPage();//**to get next dirpage to free before unpin
		  Minibase.BufferManager.unpinPage(dirCurId, UNPIN_CLEAN);
		  Minibase.BufferManager.freePage(dirCurId); //**free the page that is being pointed now
		  
		  dirCurId = dirNextId;//assign the next page id to current id
	  }//while

  } // public void deleteFile()

  
  
  /**
   * Inserts a new record into the file and returns its RID.
   * Should be efficient about finding space for the record.
   * However, fixed length records inserted into an empty file
   * should be inserted sequentially.
   * Should create a new directory and/or data page only if
   * necessary.
   * 
   * @throws IllegalArgumentException if the record is too 
   * large to fit on one data page
   */
  public RID insertRecord(byte[] record) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**search available space in dirpage. MAX_TUPSIZE = 1004
	  int recLength = record.length;//**get the length of the inserted record
	  //**check if it is smaller than the Max record size allowed
	  if (recLength <= MAX_TUPSIZE){
		  DataPage pg4Rec = new DataPage();
		  
		  //**PageId pgid4Rec = this.getAvailPage(recLength);
		  //PageId pgid4Rec = getAvailPage(recLength + HFPage.SLOT_SIZE); //**Add slot size buffer on it
		  PageId pgid4Rec = getAvailPage(recLength);
		  Minibase.BufferManager.pinPage(pgid4Rec, pg4Rec, PIN_DISKIO); //**pin the page space we just got
		  //**call insertRecord from HFPage class to insert into datapage
		  RID insertRecId = pg4Rec.insertRecord(record);
		  //**update entry info
		  short freecnt = pg4Rec.getFreeSpace();
		  
		  Minibase.BufferManager.unpinPage(pgid4Rec, UNPIN_DIRTY); //**unpin the page
		  updateDirEntry(pgid4Rec, 1, freecnt); //**call updateEntry 
		  //this.updateDirEntry(pgid4Rec, 1, freecnt);
		  
		  return insertRecId;
	  }
	  else{
		  throw new IllegalArgumentException("The record is too large to fit on one data page");
	  }
	  
   } // public RID insertRecord(byte[] record)

  
  
  
  /**
   * Reads a record from the file, given its rid.
   * 
   * @throws IllegalArgumentException if the rid is invalid
   */
  public byte[] selectRecord(RID rid) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**rid has page id info, pin the page to get the content of the page, then call selectRecord from 
	  //**HFPage class to track down the record
	  DataPage mempg = new DataPage();//** used to hold the content of the page that the record belongs to
	  byte[] selRcd = null; //**init the record holder to return the record
	  Minibase.BufferManager.pinPage(rid.pageno, mempg, PIN_DISKIO);//**pin the page
	  //**IllegalArgumentException if the rid is invalid
	  try{
		  selRcd = mempg.selectRecord(rid);
	  }catch (IllegalArgumentException exc){
		  throw exc;
	  }
	  Minibase.BufferManager.unpinPage(rid.pageno, UNPIN_CLEAN);//**unpin the page
	  
	  return selRcd;
  } // public byte[] selectRecord(RID rid)

  
  
  
  /**
   * Updates the specified record in the heap file.
   * 
   * @throws IllegalArgumentException if the rid or new record is invalid
   */
  public void updateRecord(RID rid, byte[] newRecord) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**similar to selectRecord, find out the page id to which rid points, call updateRecord from HFPage
	  DataPage mempg = new DataPage();
	  Minibase.BufferManager.pinPage(rid.pageno, mempg, PIN_DISKIO);//**pin the page
	  //**throws IllegalArgumentException if the rid or new record is invalid
	  try{
		  mempg.updateRecord(rid, newRecord);
		  Minibase.BufferManager.unpinPage(rid.pageno, UNPIN_DIRTY);//**unpin the page if it passes the try catch statement   
	  }catch (IllegalArgumentException exc){
		  //**don't forget unpin here
		  Minibase.BufferManager.unpinPage(rid.pageno, UNPIN_CLEAN);//**unpin the page if it doesn't pass the try catch statement
		  throw exc;
	  }

  } // public void updateRecord(RID rid, byte[] newRecord)

  
  
  
  /**
   * Deletes the specified record from the heap file.
   * Removes empty data and/or directory pages.
   * 
   * @throws IllegalArgumentException if the rid is invalid
   */
  public void deleteRecord(RID rid) {

	  //throw new UnsupportedOperationException("Not implemented"); 
	  
	  //**similar to the above, find out page id and call deleteRecord from HFPage
	  DataPage mempg = new DataPage();
	  Minibase.BufferManager.pinPage(rid.pageno, mempg, PIN_DISKIO);//**pin the page
	  //**throws IllegalArgumentException if the rid is invalid
	  try{
		  mempg.deleteRecord(rid);
		  //**update dirpage entry info
		  short freecnt = mempg.getFreeSpace();
		  //**this.updateDirEntry(rid.pageno, -1, freecnt);
		  updateDirEntry(rid.pageno, -1, freecnt);//**minus one record because of deletion
		  Minibase.BufferManager.unpinPage(rid.pageno, UNPIN_DIRTY);//**unpin the page if it passes the try catch statement
	  }catch (IllegalArgumentException exc){
		  Minibase.BufferManager.unpinPage(rid.pageno, UNPIN_CLEAN);//**unpin the page if it doesn't pass the try catch statement
		  throw exc;
	  }

  } // public void deleteRecord(RID rid)

  
  
  
  
  /**
   * Gets the number of records in the file.
   */
  public int getRecCnt() {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**traverse through dirpages, for each dirpage count the entries and count the records within each entry
	  //**need to call getEntryCnt(), getRecCnt() from DirPage class.
	  PageId dirId = new PageId(headId.pid); //starting from the header page
	  DirPage dirPage = new DirPage();//to hold the content of dirpage
	  PageId nextDirId;
	  short recCnt = 0;//initialize the record count
	  
	  while (dirId.pid != INVALID_PAGEID){//if the pid is valid
		  Minibase.BufferManager.pinPage(dirId, dirPage, PIN_DISKIO);//pin the page
		  short entryCnt = dirPage.getEntryCnt();//get directory entries count on dirPage
		  //**loop through each entry
		  for (int entryNum = 0; entryNum < entryCnt; entryNum++){
			  short temp = dirPage.getRecCnt(entryNum);//get record count at the given index
			  recCnt += temp;
		  }//for
		  nextDirId = dirPage.getNextPage();//move on to the next page
		  
		  Minibase.BufferManager.unpinPage(dirId, UNPIN_CLEAN);//unpin the page and make it clean
		  dirId = nextDirId;//set current to the next		  
	  }
	  
	  return recCnt;//return the record count

  } // public int getRecCnt()

  
  
  
  
  /**
   * Initiates a sequential scan of the heap file.
   */
  public HeapScan openScan() {
    return new HeapScan(this);
  }

  
  
  
  /**
   * Returns the name of the heap file.
   */
  public String toString() {
    return fileName;
  }

  
  
  
  
  /**
   * Searches the directory for the first data page with enough free space to store a
   * record of the given size. If no suitable page is found, this creates a new
   * data page.
   * A more efficient implementation would start with a directory page that is in the
   * buffer pool.
   */
  protected PageId getAvailPage(int reclen) {
	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**invoked by insertRecord() to search for free space; 
	  PageId dirCurId = new PageId(headId.pid);//**init by getting the head dirpage id
	  DirPage curDirPg = new DirPage();
	  PageId dirNextId;
	  PageId availPgId = null;//**returned page id, initialized as null
	  
	  //**traversing through dirpage, when the pid is valid and availPgId is null 
	  while(dirCurId.pid != INVALID_PAGEID && availPgId == null){
		  Minibase.BufferManager.pinPage(dirCurId, curDirPg, PIN_DISKIO);//pin the page
		  //System.out.println(dirCurId.pid);//**test
		  //**collect free space info for each entry in dirpage
		  for(int entryNo=0; entryNo < curDirPg.getEntryCnt(); entryNo++){
			  //**if found available space return the availPgId, (freecnt - slot_size) is the actual free space for reclen 
			  //**SLOT_SIZE = 4
			  if (curDirPg.getFreeCnt(entryNo) >= (reclen + HFPage.SLOT_SIZE)){
				  availPgId = curDirPg.getPageId(entryNo);
				  //System.out.println(availPgId);//**test
				  break;//**jump out of loop to return availPgId
			  }
			  //**if else, just continue the for loop
		  }//for
		  //**point to the next dirpage
		  dirNextId = curDirPg.getNextPage();
		  
		  Minibase.BufferManager.unpinPage(dirCurId, UNPIN_CLEAN);//unpin the page with clean
		  dirCurId = dirNextId;//**always point to the next before unpin the current
	  }//while
	  
	  //**if searching no luck, insert a new page and get the page id.
	  if (availPgId == null){
		  //**availPgId = this.insertPage();
		  availPgId = insertPage();
	  }  
	  return availPgId;

  } // protected PageId getAvailPage(int reclen)

  
  
  
  /**
   * Helper method for finding directory entries of data pages.
   * A more efficient implementation would start with a directory
   * page that is in the buffer pool.
   * 
   * @param pageno identifies the page for which to find an entry
   * @param dirId output param to hold the directory page's id (pinned)
   * @param dirPage output param to hold directory page contents
   * @return index of the data page's entry on the directory page
   */
  protected int findDirEntry(PageId pageno, PageId dirId, DirPage dirPage) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**locate the head directory page
	  //**dirId.pid = this.headId.pid;
	  dirId.pid = headId.pid;
	  int entryNum = 0;//**keep track of the entry
	  
	  //**traverse through directory pages
	  while (true){//this allows the program always enters the loop
		  //**pin directory page in pool
		  Minibase.BufferManager.pinPage(dirId, dirPage, PIN_DISKIO);
		  //**loop through all the entries within each directory page to find the pageid
		  for (entryNum = 0; entryNum < dirPage.getEntryCnt(); entryNum++){
			  if (pageno.pid == dirPage.getPageId(entryNum).pid){
				  //**jump out of loop to return the entry value
				  //break;
				  return entryNum;
			  }//if
		  }//for
		  //**iterator goes to the next directory page
		  PageId nextDirId = dirPage.getNextPage();
		  Minibase.BufferManager.unpinPage(dirId, UNPIN_CLEAN);//unpin the page with clean
		  //**dirId = nextDirId; //**update the current dirId
		  dirId.pid = nextDirId.pid;
	  }//while
	  //return entryNum;

  } // protected int findEntry(PageId pageno, PageId dirId, DirPage dirPage)

  
  
  
  /**
   * Updates the directory entry for the given data page.
   * If the data page becomes empty, remove it.
   * If this causes a dir page to become empty, remove it
   * @param pageno identifies the data page whose directory entry will be updated
   * @param deltaRec input change in number of records on that data page
   * @param freecnt input new value of freecnt for the directory entry
   */
  protected void updateDirEntry(PageId pageno, int deltaRec, int freecnt) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  PageId dirId = new PageId();//**to locate directory page id
	  DirPage dirPage = new DirPage();//** to hold directory page content
	  //**through the pageno findDirEntry
	  //**int entryNum = this.findDirEntry(pageno, dirId, dirPage);
	  int entryNum = findDirEntry(pageno, dirId, dirPage);
	  
	  //**look up the record counts for the entry
	  int recCnt = dirPage.getRecCnt(entryNum);
	  //**with input change in number of records, update recCnt
	  recCnt += deltaRec;
	  if (recCnt >= 1){//if record count is positive
		  //**set record counts, freecnt for the entry
		  dirPage.setRecCnt(entryNum, (short)recCnt);
		  dirPage.setFreeCnt(entryNum, (short)freecnt);
		  //**dirpage modified, unpin dirty page
		  Minibase.BufferManager.unpinPage(dirId, UNPIN_DIRTY);
	  }
	  if (recCnt <= 0){//if record count is negative
		  //**datapage become empty, call deletePage to remove it
		  //**this.deletePage(pageno, dirId, dirPage, entryNum);
		  deletePage(pageno, dirId, dirPage, entryNum);
	  }
	  

  } // protected void updateEntry(PageId pageno, int deltaRec, int deltaFree)

  
  
  
  /**
   * Inserts a new empty data page and its directory entry into the heap file. 
   * If necessary, this also inserts a new directory page.
   * Leaves all data and directory pages unpinned
   * 
   * @return id of the new data page
   */
  protected PageId insertPage() {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**locate dirpg id, and create a mempg to hold dirpg content
	  PageId dirCurId = new PageId(headId.pid);//**locate the head dirpage of heapfile
	  DirPage curDirPg = new DirPage(); //**hold the content of the page
			  
	  //traverse through dirpage and each entry within it
	  //**if insert is done, jump out of loop
	  while(true) {//this makes the program always excutes the while loop
		  //**pin the dirpage in the pool
		  Minibase.BufferManager.pinPage(dirCurId, curDirPg, PIN_DISKIO);
		  //**DirPage.MAX_ENTRIES = 125
		  if (curDirPg.getEntryCnt() < DirPage.MAX_ENTRIES){
			  //**not exceeding the max entries within dirpage, just create a new data page
			  //**insert is complete, jump out of the loop to create a new data page
			  break; 
		  }
		  PageId dirNextId = curDirPg.getNextPage();
		  //**this dirpage is full, go to next dirpage
		  /* if (curDirPg.getEntryCnt() == DirPage.MAX_ENTRIES){
			  //**PageId dirNextId = curDirPg.getNextPage(); //**next directory page
			  Minibase.BufferManager.unpinPage(dirCurId, UNPIN_DIRTY);
			  dirCurId = dirNextId;
			  
		  }*/
		  //**traverse towards the end, no luck, create a new dirpage
		  if (dirNextId.pid == INVALID_PAGEID){//if the pid is invalid
			  DirPage insertDirPg = new DirPage(); 
			  PageId insertDirId = Minibase.BufferManager.newPage(insertDirPg, 1);//get pageid by pinning
			  
			  //**chain the newly inserted dirpage (insertDirPg) with the current page and previous page.
			  //**set current page as insertDirPg, which is curDirPg's next page, whose previous page id is dirCurId.
			  insertDirPg.setCurPage(insertDirId); 
			  curDirPg.setNextPage(insertDirId);
			  insertDirPg.setPrevPage(dirCurId);
			  
			  //**done with dirCurId, unpin it qirh dirty
			  Minibase.BufferManager.unpinPage(dirCurId, UNPIN_DIRTY);
			  //**now the dirpage we are working on is the newly created one
			  dirCurId = insertDirId;
			  curDirPg = insertDirPg;
			  
			  //**insert is complete, jump out of the loop
			  break;//**
		  }//if
		  //**unpin the page with clean
		  Minibase.BufferManager.unpinPage(dirCurId, UNPIN_CLEAN);
		  dirCurId = dirNextId;//set the pointer to the next
	  }// while
	  
	  
	  //**new datapage in the new dirpage
	  DataPage insertPg = new DataPage();
	  //**pin the new datapg
	  PageId insertId = Minibase.BufferManager.newPage(insertPg, 1);
	  insertPg.setCurPage(insertId);//set current page is the new insert page
	  //**set up the parameters (page id, reccnt, freecnt, entrycnt) in dirpage entry for the newly inserted data page 
	  curDirPg.setPageId(curDirPg.getEntryCnt(), insertId);
	  curDirPg.setRecCnt(curDirPg.getEntryCnt(), (short)0);
	  curDirPg.setFreeCnt(curDirPg.getEntryCnt(),insertPg.getFreeSpace());
	  curDirPg.setEntryCnt((short)(curDirPg.getEntryCnt()+1));
	  //**unpin datapage, unpin dirpage. with dirty
	  Minibase.BufferManager.unpinPage(insertId, UNPIN_DIRTY);
	  Minibase.BufferManager.unpinPage(dirCurId, UNPIN_DIRTY);
	  
	  return insertId;	  

  } // protected PageId insertPage()

  
  
  
  /**
   * Deletes the given data page and its directory entry from the heap file. If
   * appropriate, this also deletes the directory page.
   * 
   * @param pageno identifies the page to be deleted
   * @param dirId input param id of the directory page holding the data page's entry
   * @param dirPage input param to hold directory page contents
   * @param index input the data page's entry on the directory page
   */
  protected void deletePage(PageId pageno, PageId dirId, DirPage dirPage,
      int index) {

	  //throw new UnsupportedOperationException("Not implemented");
	  
	  //**invoked by updateDirEntry
	  //the operation is in the pool, use BufMgr.freePage to remove the page and reset the page to 0
	  Minibase.BufferManager.freePage(pageno);
	  //**shift down the entry (index) because of the removal, calling compact from DirPage class
	  dirPage.compact(index);//**now the dirpage is compacted, no empty slots in between entries
	  //**get the entry count 
	  short entryCnt = dirPage.getEntryCnt();
	  
	  //**check if entryCnt > 1 or <=1 to determine if we need to delete directory page or just 
	  //**decrement entryCnt. Or if it's header dirpage, don't need to delete
	  if ((entryCnt > 1) || (dirId.pid == headId.pid)){
		  entryCnt -= 1;
		  dirPage.setEntryCnt(entryCnt);//set updated entry count
		  //**unpin dirty page in the pool
		  Minibase.BufferManager.unpinPage(dirId, UNPIN_DIRTY);
	  }
	  else{
		  //**this case we need to rechain the previous dirpage and next dirpage after deleting the target dirpage
		  //**init temp dirpage to hold the dirpage content during rechaining.
		  DirPage curdirPg = new DirPage();
		  PageId prevdirPgId = dirPage.getPrevPage();//get previous page id
		  PageId nextdirPgId = dirPage.getNextPage();//get next page id		  
		  
		  //if the previous pid is valid
		  if(prevdirPgId.pid != -1)
          {	  //**chain the prev with next
              Minibase.BufferManager.pinPage(prevdirPgId, curdirPg, PIN_DISKIO);//pin the page
              curdirPg.setNextPage(nextdirPgId);//set the next page as curdirPg and connects it with prevdirPgId
              Minibase.BufferManager.unpinPage(prevdirPgId, UNPIN_DIRTY);//**modified, write out dirty page
          }
		  //if the next pid is valid
          if(nextdirPgId.pid != -1)
          {	  //**chain the prev with next dirpage
              Minibase.BufferManager.pinPage(nextdirPgId, curdirPg, PIN_DISKIO);
              curdirPg.setPrevPage(prevdirPgId);//set the previous page as curdirPg and connects it with nextdirPgId
              Minibase.BufferManager.unpinPage(nextdirPgId, UNPIN_DIRTY); ;//**modified, write out dirty page
          }
          
          Minibase.BufferManager.unpinPage(dirId, UNPIN_CLEAN);//unpin the page with clean
          Minibase.BufferManager.freePage(dirId); //**nothing followed by curdirPg, so just delete it
		  
	  }//else
	  
	  

  } // protected void deletePage(PageId, PageId, DirPage, int)

} // public class HeapFile implements GlobalConst














