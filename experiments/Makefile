default:

.PHONY: clean
clean:
	rm -f *.out *~

filename1 = ../fileops.py
.PHONY:	test1
test1:
	rm -f test1.out
	./test1 $(filename1)
	cmp test1.out $(filename1)

filename2 = ../big1-audio-list
.PHONY:	test2
test2:
	rm -f test2.out
	./test2 $(filename2)
	zcat test2.out | cmp - $(filename2)

