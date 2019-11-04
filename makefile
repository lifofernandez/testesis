TESTS := $(shell find tests -name '*.yml') 
CURRENT := $(shell pwd)

install:
	pip install -r requirements.txt
	ln -s $(CURRENT)/yml2mid /usr/bin/
test:
	for i in $(TESTS); \
	do \
		echo "secuenciando: $$i"; \
		yml2mid "$$i" -o "$$i"; \
	done;	

	
# ./recursos/utiles/mid2asc output.mid | grep Key
