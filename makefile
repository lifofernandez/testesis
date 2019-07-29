TESTS := $(shell find tests -name '*.yml') 
TODOS := $(shell find . -name '*.py') 

test:
	for i in $(TESTS); \
	do \
		echo "secuenciando: $$i"; \
		yml2mid "$$i" -o "$$i"; \
	done;	
comp:
	cp tests /home/lf/ -r
pepe:
	make test
	make comp

todos:
	for i in $(TODOS); \
	do\
	        echo "$$i "; \
		cat "$$i" | grep TODO; \
	done;	
	
# ./reserva/utiles/mid2asc output.mid | grep Key
