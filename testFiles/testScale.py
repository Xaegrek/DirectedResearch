from datetime import datetime
import time

desiredPath = [[0,1],[2,2]]
posHistory = [0,1,3,5]

a = str(time.time()) + '.txt'
f = open(a, 'a')
f.write('desired path')
f.write(str(desiredPath))
f.write('actual path')
f.write(str(posHistory))
f.close()