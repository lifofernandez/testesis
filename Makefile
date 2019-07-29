test:
	yml2mid tests/test-*.yml && \
	cp output.mid /root/Varios/output.mid && \
	cp output.mid /home/lf/output.mid 

# ./reserva/utiles/mid2asc output.mid | grep Key

foo:
	for i in `find tests$\*`; \
	do \
		echo "$$i"; \
	done;	
