p2: lex.yy.o cal.tab.o
	gcc -o p2 lex.yy.o cal.tab.o
	echo 2+3 | ./p2

lex.yy.o: cal.l
	flex cal.l; gcc -c lex.yy.c

cal.tab.o: cal.y
	bison -d cal.y; gcc -c cal.tab.c

clean:
	rm -f p2 cal.output *.o cal.tab.c lex.yy.c cal.tab.h
