from threading import Thread, Event

class ReusableThread2(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self,*args, **kwargs)
        self._default_args = self._target, self._args, self._kwargs

    def run(self, *args, **kwargs):
        super().run()
        self.reset()
        
    def reset(self, *args, **kwargs):
        self._target = self._default_args[0]
        self._args = args or self._default_args[1]
        self._kwargs = kwargs or self._default_args[2]

class ReusableThread(Thread):
    """
    This class provides code for a restartale / reusable thread

    join() will only wait for one (target)functioncall to finish
    finish() will finish the whole thread (after that, it's not restartable anymore)
        
    """

    def __init__(self, target, args):
        self._startSignal = Event()
        self._oneRunFinished = Event()
        self._finishIndicator = False
        self._callable = target
        self._callableArgs = args
        self.running = False

        Thread.__init__(self, name="Reusable")

    def restart(self):
        """make sure to always call join() before restarting"""
        self._startSignal.set()
        return self

    def run(self):
        """ This class will reprocess the object "processObject" forever.
        Through the change of data inside processObject and start signals
        we can reuse the thread's resources"""

        while(True):    
            # wait until we should process
            self._startSignal.wait()
            self.running = True

            self._startSignal.clear()

            if(self._finishIndicator):# check, if we want to stop
                self._oneRunFinished.set()
                return
            
            # call the threaded function
            self._callable(*self._callableArgs)

            # notify about the run's end
            self._oneRunFinished.set()

    def is_running(self):
        return self.running

    def join(self):
        """ This join will only wait for one single run (target functioncall) to be finished"""
        self._oneRunFinished.wait()
        self._oneRunFinished.clear()
        self.running = False
        return self

    def finish(self):
        self._finishIndicator = True
        self.restart()
        self.join()
        return self