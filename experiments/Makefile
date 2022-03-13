default:

.PHONY: clean
clean:
	rm -f *.out *~

.PHONY:	test1
test1:
	rm -f test1.out
	./test1
	cmp test1.out ../fileops.py

.PHONY:	test2
test2:
	rm -f test2.out
	./test2
	zcat test2.out | cmp - ../fileops.py

