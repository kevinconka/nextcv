# Makefile for NextCV, intended for C++ related development

.DEFAULT_GOAL := help
PRESET := uv-env

# Common paths and patterns
SRC_DIR := nextcv/_cpp/src
BUILD_DIR := build
CPP_FILES := $(shell find $(SRC_DIR) -name '*.cpp' -not -path '*/bindings/*')

# Cross-platform detection for clang-tidy
OS := $(shell uname -s)
CLANG_TIDY_EXTRA_FLAGS :=
ifeq ($(OS), Darwin)
    SDK_PATH := $(shell xcrun --show-sdk-path)
    CLANG_TIDY_EXTRA_FLAGS += --extra-arg='-isysroot' --extra-arg='$(SDK_PATH)'
endif

# Clang-Tidy base command
CLANG_TIDY_BASE_CMD := @clang-tidy -p $(BUILD_DIR) $(CLANG_TIDY_EXTRA_FLAGS)

.PHONY: help
help: ## Show available commands
	@echo "NextCV Makefile"
	@echo "---------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

# Environment and dependency checks
.PHONY: deps-clang
deps-clang: ## Check for clang-tidy and clang-format
	@command -v clang-tidy >/dev/null || (echo "❌ clang-tidy not found" && (echo "   Install: macOS → brew install llvm | Linux → apt install clang-tidy" && exit 1))
	@command -v clang-format >/dev/null || (echo "❌ clang-format not found" && (echo "   Install: macOS → brew install clang-format | Linux → apt install clang-format" && exit 1))
	@echo "✅ Clang-Tidy and Clang-Format OK ($(OS))"

# Build and clean
.PHONY: build
build: ## Configure and build the project
	@command -v cmake >/dev/null || (echo "❌ cmake not found" && echo "   Install: macOS → brew install cmake | Linux → apt install cmake" && exit 1)
	cmake --preset $(PRESET)
	cmake --build --preset $(PRESET)

.PHONY: clean
clean: ## Remove build directory
	rm -rf $(BUILD_DIR)
	@echo "✅ Clean complete"

# Code formatting and linting
.PHONY: format
format: deps-clang ## Run clang-format on all C++ files
	@echo "Running clang-format..."
	@clang-format -i $(CPP_FILES)

.PHONY: tidy
tidy: build deps-clang ## Run clang-tidy on all C++ files
	@echo "Running clang-tidy on all files..."
	$(CLANG_TIDY_BASE_CMD) $(CPP_FILES)

.PHONY: tidy-file
tidy-file: build deps-clang ## Run clang-tidy on a specific file. Usage: make tidy-file FILE=path/to/file.cpp
	@echo "Running clang-tidy on $(FILE)..."
	$(CLANG_TIDY_BASE_CMD) $(FILE)

.PHONY: tidy-fix
tidy-fix: build deps-clang ## Run clang-tidy --fix on all C++ files
	@echo "Running clang-tidy --fix on all files..."
	$(CLANG_TIDY_BASE_CMD) --fix $(CPP_FILES)

# Python tooling
.PHONY: ruff-fix
ruff-fix: ## Run ruff formatter and linter with safe fixes
	@command -v uvx >/dev/null || (echo "❌ uvx not found" && (echo "   Install: uv pip install uvx" && exit 1))
	@uvx ruff format .
	@uvx ruff check . --fix --exit-zero
	@uvx ruff format .

.PHONY: ruff-fix-unsafe
ruff-fix-unsafe: ## Run ruff linter with unsafe fixes
	@echo "Running ruff check with unsafe fixes..."
	@command -v uvx >/dev/null || (echo "❌ uvx not found" && (echo "   Install: uv pip install uvx" && exit 1))
	@uvx ruff format .
	@uvx ruff check . --fix --unsafe-fixes --exit-zero
	@uvx ruff format .

.PHONY: stubs
stubs: clean ## Generate Python stubs for the C++ module
	@echo "Syncing environment..."
	@uv sync --reinstall
	@echo "Generating stubs for C++ module..."
	@pybind11-stubgen nextcv._cpp.nextcv_py --output-dir .
	@echo "Running ruff-fix-unsafe after stub generation..."
	@$(MAKE) ruff-fix-unsafe # Call the ruff-fix-unsafe target
