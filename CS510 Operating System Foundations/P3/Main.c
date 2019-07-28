code Main

  -- OS Class: Project 3
  --
  -- Haomin He
  --
  --
  --
  -- References: 
  -- Tanenbaum textbook, SleepingBarberProblem.pdf
  -- http://users.dickinson.edu/~braught/courses/cs354s00/classes/code/SleepBarber.src.html
  -- https://courses.cs.washington.edu/courses/cse451/98sp/Projects/Assign4/mipsi-solution/USER/barber.c
  -- https://github.com/JuShuck
  -- http://web.cecs.pdx.edu/~harry/Blitz/OSProject/p2/Main.c  
  -- https://github.com/tgjamin
  -- https://github.com/ladinu
-----------------------------  Main  ---------------------------------

  function main ()
      InitializeScheduler ()  
      SleepingBarber ()
      ThreadFinish ()
    endFunction


-----------------------------  SleepingBarber  ---------------------------------

  const CHAIRNUM = 5     -- # chairs for waiting customers 
  const CUSTOMERNUM = 10  -- 10 customers
  const BARBERNUM = 1     -- 1 barber

  var 
    customers: Semaphore = new Semaphore   -- # of customers waiting for service 
    barbers: Semaphore = new Semaphore     -- # of barbers waiting for customers 
    mulock: Mutex = new Mutex    -- for mutual exclusion 
    waiting: int = 0   -- customer are waiting (not being cut)

    -- 10 customers/threads. 1 barber/thread
    cusArray: array [CUSTOMERNUM] of Thread = new array of Thread { CUSTOMERNUM of new Thread }   -- thread for customer
    barArray: array [BARBERNUM] of Thread = new array of Thread { BARBERNUM of new Thread }  -- thread for barber


  function SleepingBarber()
    -- initialize variables 
    customers.Init(0)  -- nothing happens yet, set semaphore to 0
    barbers.Init(0)  
    mulock.Init()   -- initialize the lock

    print("         Barber  1   2   3   4   5   6   7   8   9   10  \n")
    -- initialize one barber thread
    barArray[0].Init("Barber")
    barArray[0].Fork(barber, 1)

    -- initialize 10 customer threads
    cusArray[0].Init("Customer 1")
    cusArray[0].Fork(CutAndWait,1)

    cusArray[1].Init("Customer 2")
    cusArray[1].Fork(CutAndWait,2)

    cusArray[2].Init("Customer 3")
    cusArray[2].Fork(CutAndWait,3)

    cusArray[3].Init("Customer 4")
    cusArray[3].Fork(CutAndWait,4)

    cusArray[4].Init("Customer 5")
    cusArray[4].Fork(CutAndWait,5)

    cusArray[5].Init("Customer 6")
    cusArray[5].Fork(CutAndWait,6)

    cusArray[6].Init("Customer 7")
    cusArray[6].Fork(CutAndWait,7)

    cusArray[7].Init("Customer 8")
    cusArray[7].Fork(CutAndWait,8)

    cusArray[8].Init("Customer 9")
    cusArray[8].Fork(CutAndWait,9)

    cusArray[9].Init("Customer 10")
    cusArray[9].Fork(CutAndWait,10)

  endFunction


  function CutAndWait (p: int)
    -- The parameter "p" identifies which customer this is.
    -- a customer entering the shop has to count the number of
    -- waiting customers. If it is less than the number of chairs (5), 
    -- he stays; otherwise, he leaves.
    -- There are 10 cutomers in total, we need to go around and check each customer status
    -- When a customer is done haircut and left, other customer in waiting can take the seat
      var
        i: int
      for i = 1 to 10
        -- call customer function
        customer(p)
      endFor
  endFunction



  function barber()
    while(true)
      customers.Down()  -- go to sleep if # of customers is 0, Sleep until someone arrives and wakes you
      mulock.Lock()   -- acquire access to "waiting", get the lock
      waiting = waiting - 1   -- decrement count of waiting customers, cut current customer hair
      barbers.Up()   -- one barber is now ready to cut hair, wake up barber
      mulock.Unlock()   -- release 'waiting' lock
      cut_hair()   -- cut hair (outside critical region)
    endWhile  -- 
  endFunction




  function customer(p:int)
    -- The parameter "p" identifies which customer this is.
    -- get lock before enter critical section

    mulock.Lock()
    enterh(p) -- customer entered the barber shop
    if(waiting < CHAIRNUM)   -- if the customer has a place to sit, if there are no free chairs, leave 
      waiting = waiting + 1   -- increment count of waiting customers
      sith(p)  -- customer sit down
      customers.Up()   -- wake up barber if necessary, signal that a customer showed up 
      mulock.Unlock()  -- release access to 'waiting'
      barbers.Down()   -- go to sleep if # of free barbers is 0, wait for barber
      get_haircut(p)   -- be seated and be served,  barber is cutting hair 
      leaveh(p)  -- get haircut done and leave
    else
    leaveh(p) -- if there are no free chairs, leave
      mulock.Unlock()  -- shop is full; do not wait 
    endIf
  endFunction


  function get_haircut(p:int)
    --customer get haircut
    var
      i:int
      mulock.Lock()
      beginh(p)
      for i=1 to 80
        currentThread.Yield()  --haircut time consuming
      endFor

      finishh(p) --print we are done
      mulock.Unlock()
    endFunction


  function cut_hair()
    -- cut current customer hair
    -- let the current thread wait. 
    -- acquire lock before cutting
    var 
      len: int

    mulock.Lock()
    starth() --start haircut

    -- haricut consuming time 80
    for len = 1 to 80
      -- make other threads wait until we are done. other threads do not have the lock
      currentThread.Yield()
    endFor

    endh() --end haircut
    mulock.Unlock()  -- release the lock
  endFunction


  -- E = Enter, S = Sit in waiting chair, B = Begin haircut, F = Finish haircut, L = Leave
  -- start = Barber begins haircut, end = Barber ends haircut

  function beginh(p:int)
    --print begin haircut
    currentchairstatus()
    printspace(p)
    print("B\n")
  endFunction


  function finishh(p:int)
    -- print finish haircut
    currentchairstatus()
    printspace(p)
    print("F\n")
  endFunction

  function printspace(p:int)
    -- print spaces for current thread
    var
        i: int
      print("          ")
      for i = 1 to (p - 1) * 4
        print("-")
      endFor
    endFunction


  function currentchairstatus()
   var
      seat: int
      print(" ")
      -- print how many chairs occupied 
      for seat = 1 to waiting
        print ("X")
      endFor

      -- how many chairs are empty
      for seat = 1 to CHAIRNUM - waiting
        print ("_")
      endFor
      print(" ")
   endFunction

  function starth()
    currentchairstatus()
    print("  start\n")
   endFunction


  function endh()
    currentchairstatus()
    print("  end\n")
  endFunction
  

  function enterh(p:int)
    currentchairstatus()
    printspace(p)
    print("E\n")
  endFunction


  function sith(p:int)
    currentchairstatus()
    printspace(p)
    print("S\n")
  endFunction


  function leaveh(p:int)
    currentchairstatus()
    printspace(p)
    print("L\n")
  endFunction
  





    
endCode

 
