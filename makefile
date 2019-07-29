TESTS := $(shell find tests -name '*.yml') 
test:
	for i in $(TESTS); \
	do \
		echo "eo $$i"; \
		yml2mid "$$i" -o "$$i"; \
	done;	
comp:
	cp tests /home/lf/ -r
pepe:
	make test
	make comp
	
# ./reserva/utiles/mid2asc output.mid | grep Key
