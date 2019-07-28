package bufmgr;

import global.PageId; 

//CS 587 
//Creators: Haomin He, Zicheng Ren

/**
 * (from assignment doc) Each frame has certain states associated with it. These states include whether the frame
is dirty, whether it includes valid data (data which reflects data in a disk page), and if it
includes valid data then what is the disk page number of the data, how many callers
have pins on the data (the pin count), and any other information you wish to store, for
example information relevant to the replacement algorithm. Be sure to store this information as 
efficiently as possible while preserving readability. You should store these
states in a structure described by a separate class called FrameDesc. Call the structure
frametab; I’ll refer to it as the frame table, or frame descriptors.
 */
 
class FrameDesc {
  //**the members are accessible by outside class
  public int idx; //**buffer pool index
  public PageId pageno; //**identifier for page in frame, inherited from PageId class
  public int pincount; //**count number of pins
  public boolean dirty; //**check if the page is dirty
  public boolean refbit;//**reference check 
   
  //**initialize FrameDesc constructor
  public FrameDesc(int frameno) {
    this.idx = frameno;
    this.pageno = new PageId();
    this.pincount = 0;
    this.dirty = false;
    this.refbit = true; //
  }

  //** set the pin count for current page
  public void setPinCount(int i) {
	  this.pincount = i;
  }
  
  //** get the pin count for current page
  public int getPinCount() {
	  return this.pincount;
  }
  
  //** check if the page is dirty
  public boolean checkDirty() {
	  return this.dirty;
  }
   
} // class FrameDesc