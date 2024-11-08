# Define your project directory (src)
SRC_DIR := src

# Define the target binary name
TARGET := gateway

# Define Go files to build
SRC_FILES := $(SRC_DIR)/main.go $(SRC_DIR)/server.go $(SRC_DIR)/server_pool.go $(SRC_DIR)/health_check.go $(SRC_DIR)/utils.go

.PHONY: build run clean

build:
	@echo "Building the project..."
	go build -o $(TARGET) $(SRC_FILES)

run: build
	@echo "Running the project..."
	./$(TARGET)

clean:
	@echo "Cleaning up..."
	rm -f $(TARGET)
