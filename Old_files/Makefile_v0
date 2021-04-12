# --------------------------------------------------------------------------- #
# Example
square:
	gcc -Wall -Werror -fPIC -I./src/ -c src/square.c -o bin/square.o
	gcc -shared -o libsquare.so bin/square.o

cube:
	gcc -Wall -Werror -fPIC -I./src/ -c src/cube.c -o bin/cube.o
	gcc -shared -o libcube.so bin/cube.o

main:
	# Compile
	gcc -Wall -Werror -I./src/ -c src/main.c -o bin/main.o
	# Link
	gcc -o prog bin/main.o -L. -lcube -lsquare -lm

# --------------------------------------------------------------------------- #
# my_papi
my_papi:
	gcc -Wall -Werror -fPIC -I./src/ -c src/my_papi.c -o bin/my_papi.o
	gcc -shared -o libmy_papi.so bin/my_papi.o -L/usr/local/lib -lpapi

	gcc -Wall -Werror -I./src/ -c src/papi_main.c -o bin/papi_main.o
	gcc -o papi_prog bin/papi_main.o -L. -lmy_papi
	
	# Importante! de lo contrario no nos deja de medir la 1a vez
	sudo sysctl -w kernel.perf_event_paranoid=1
	export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:.:/usr/local/lib
	./papi_prog

clean:
	rm bin/* *.so *prog

my_papi_copy:
	gcc -Wall -Werror -fPIC -I./src/ -c src/my_papi_copy.c -o bin/my_papi_copy.o
	gcc -shared -o libmy_papi_copy.so bin/my_papi_copy.o -L/usr/local/lib -lpapi

	gcc -Wall -Werror -I./src/ -c src/papi_main_copy.c -o bin/papi_main_copy.o
	gcc -o papi_prog_copy bin/papi_main_copy.o -L. -lmy_papi_copy
	
	# Importante! de lo contrario no nos deja de medir la 1a vez
	sudo sysctl -w kernel.perf_event_paranoid=1
	export LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:.:/usr/local/lib
	./papi_prog_copy
