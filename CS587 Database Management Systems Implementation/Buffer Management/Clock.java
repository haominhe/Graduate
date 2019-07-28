package bufmgr;

import global.GlobalConst;
import global.Page;

//CS 587 
//Creators: Haomin He, Zicheng Ren


/*
 *  Clock approximates LRU behavior by approximating the time of each page’s 
 *  last access by one bit, called the reference bit.
 *  
 *  Each frame descriptor keeps a reference bit (refbit), which is true if 
 *  the page has been referenced recently. It is set to true when the pincount 
 *  is set to zero.
 */

class Clock implements GlobalConst{
	 
	 // go through each frame in frametable
	 protected FrameDesc[] frametable;
	 protected Page[] bufpoolpool;
	 /*
	  * The clock algorithm keeps a circular list of pages in memory, with the 
	  * "hand" (iterator) pointing to the last examined page frame in the list. 
	  */
	protected int headiter;
	 // size of total frames
	protected int framesize;
	protected boolean found;
	 
	public Clock(BufMgr bufferMgr) {
		 frametable = bufferMgr.frametab;
		 bufpoolpool = bufferMgr.bufpool;
		 
		 //Iterator points to nothing at the beginning
		 headiter = INVALID_PAGEID;
		 found = false;
		 framesize = bufferMgr.getNumFrames();
	 }
	
	//*called when bufmgr calls pinpage,
	public void pinned(FrameDesc frameno) {
		frameno.refbit = true;
	}
		
	//**called when bufmgr calls unpinpage	
	public void unpinned(FrameDesc frameno) {
		if (frameno.pincount == 0) {
			frameno.refbit = false;//**only when pincount is 0 set refbit to false
		}
			
	}
		
	//**called when bufmgr calls freepage
	public void freepage(FrameDesc frameno) {
		frameno.refbit = false;
	} 
	 
	public int pickVictim() {
		/*
		  *  The clock replacement policy keeps a current variable that indicates which 
		  *  frame is currently being considered for replacement. Frames are considered 
		  *  consecutively for replacement, wrapping back to 0 when from N-1 is reached.
		  *  
		  *  When the clock needs to pick a victim, it first considers the current frame. 
		  *  If the current frame’s state is invalid the frame is chosen. Otherwise, if 
		  *  the pin count is greater than 0, the frame is not chosen.
		  *  
		  *  If the pin count is 0, then the reference bit is considered: if the reference 
		  *  bit is false, the frame is chosen. Otherwise, the reference bit is set to 
		  *  false and the next frame is considered.
		  *  
		  *  If current makes a full sweep without picking a victim, it should go around 
		  *  another time. If it makes another full sweep, we conclude that there are no 
		  *  available frames and we return an error.
		 */
		
		
		for (int counter = 0; counter < 2*framesize; counter++){
			headiter = (headiter+1) % framesize; //**spin around the clock
			if (frametable[headiter].pincount == 0){
				if (frametable[headiter].refbit == true){
					frametable[headiter].refbit = false;
				} else {
					//found = true; // found the victim frame
					return headiter;
				}
			}	
		} 
		return INVALID_PAGEID;
		
	  } // public int pick_victim
	
}