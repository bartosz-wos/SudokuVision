CXX = g++
CXXFLAGS = -std=c++17 -Wall -O3
SRC = src/main.cpp src/DLX.cpp
OUT = build/solver

all: $(OUT)

$(OUT): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(OUT)

clean:
	rm -f $(OUT)
