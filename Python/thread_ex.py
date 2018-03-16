import time
import threading
import logging
import queue as Queue

def encrypt_save_worker(args):
    a = "encrypt_save_worker " + str(args)
    if args == 2:
        time.sleep(5)
        print("Returning ", a)
        return a
    else:
        print("Returning ", a)
        return a

class MultiEncryptIOThread(object):
    def __init__(self, function, argsVector,
                 maxThreads=10,
                 daemonThread=True,
                 ):
        """
        Multi-threaded Encryption and IO thread Pool

        :param function: the worker function to encryption each eamil and
        save it to the local directory
        :param argsVector: the args vector for the worker function
        :param maxThreads: the maximum threaded in this thread pool; default
        is 10
        :param daemonThread: to use daemon thread or not;default is True
        """
        self._function = function
        self._lock = threading.Lock()
        self._nextArgs = iter(argsVector).__next__
        self._threadPool = [threading.Thread(target=self._doSome)
                            for i in range(maxThreads)]

        self._daemonThread = daemonThread
        if self._daemonThread:
            self._daemon = threading.Thread(target=self._doDaemon)
            self._daemon.setDaemon(True)

        self._queue = Queue.Queue()
        self._print_num = 0

    def _doSome(self):
        while True:
            self._lock.acquire()
            try:
                try:
                    args = self._nextArgs()
                    print("args ", args)
                except StopIteration:
                    break
            finally:
                self._lock.release()
                try:
                    result = self._function(args)
                except UnboundLocalError:
                    pass
            if result:
                print("put in queue", result)
                self._queue.put(result)

    def _DeamonEmailUpload(self,
                           encrypt_email):
        print("_DeamonEmailUpload",encrypt_email)
        

    def _doDaemon(self):
        while True:
            print("while True")
            try:
                head_encrypt_email = self._queue.get()
            except Exception as e:
                print(e)
            print("while True", head_encrypt_email)
            self._print_num += 1
            logging.debug(
                'uploading the #{} encrypt email...'.format(
                    self._print_num))
            # store the encrypt email to the mail box
            self._DeamonEmailUpload(head_encrypt_email)
            print("while True _DeamonEmailUpload")
            self._queue.task_done()  # indicate completion, must
            print("while True task_done")

    def start(self):
        if self._daemonThread:
            self._daemon.start()
        for thread in self._threadPool:
            time.sleep(0)  # necessary to give other threads a chance to run
            thread.start()
    '''        
    def join(self, timeout=None):
        for thread in self._threadPool:
            thread.join(timeout)

    def join_daemon(self):
        if self._daemonThread:
            self._queue.join()  # wait for all encrypt email to be consumed
    '''
encrpt_args = [x for x in range(3)]
mt = MultiEncryptIOThread(encrypt_save_worker, encrpt_args,
                              daemonThread=True)
mt.start()
#mt.join()
#mt.join_daemon()