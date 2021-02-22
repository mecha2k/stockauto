def printlog(message, *args):
  for arg in args:
    message += (arg + " ")
  print(message)


printlog("message :", "test1", "test2")
printlog("message :", "test1", "test2", "test3")