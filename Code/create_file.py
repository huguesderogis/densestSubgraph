
import time
beg = time.clock()
for k in range (1040307) :

	try :
		file_read = open("Krapivin2009/test/" + str(k) + ".txt", 'r')
		file_write = open("Krapivin2009/test/" + str(k) + "_new.txt", 'w')

		s = file_read.read()
		s_list = s.split()
		i =0;
		word = s_list[0]
		while word != '--R' :
			i= i+1
			file_write.write(word + " " )
			word = s_list[i]

	except IOError :
		print ("n'existe pas")

end = time.clock()
tps = end-beg
print("Time to compute : ", tps)
