.DEFAULT_GOAL := help
PRESET := uv-env

# Cross-platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    STDLIB_FLAG := -stdlib=libc++
    # Add Homebrew LLVM to PATH for macOS if not already present
    LLVM_PATH := $(shell brew --prefix llvm 2>/dev/null)
    $(info LLVM_PATH: $(LLVM_PATH))
    $(info PATH: $(PATH))
    ifneq ($(LLVM_PATH),)
        ifeq (,$(findstring $(LLVM_PATH)/bin,$(PATH)))
            $(info Adding LLVM to PATH)
            export PATH := $(LLVM_PATH)/bin:$(PATH)
            $(info PATH: $(PATH))
        endif
    endif
else
    STDLIB_FLAG :=
endif

# Common paths and patterns
SRC_DIR := nextcv/_cpp/src
BUILD_DIR := build
CPP_FILES := $(SRC_DIR) -name '*.cpp' -not -path '*/bindings/*'
TIDY_BASE := clang-tidy -p $(BUILD_DIR) --header-filter='$(SRC_DIR)/.*'
TIDY_CMD := find $(CPP_FILES) -exec $(TIDY_BASE) {} -- $(STDLIB_FLAG) \;

.PHONY: help
help: ## Show available commands
	@echo "NextCV Makefile"
	@echo "---------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

.PHONY: deps
deps: ## Check if cmake and clang-tidy are available
	@command -v cmake >/dev/null || (echo "❌ cmake not found" && echo "   Install: macOS → brew install cmake | Linux → apt install cmake" && exit 1)
	@command -v clang-tidy >/dev/null || (echo "❌ clang-tidy not found" && echo "   Install: macOS → brew install llvm | Linux → apt install clang-tidy" && exit 1)
	@echo "✅ Dependencies OK ($(UNAME_S))"

.PHONY: build
build: deps ## Configure and build the project
	cmake --preset $(PRESET)
	cmake --build --preset $(PRESET)

.PHONY: tidy
tidy: build ## Run clang-tidy on all C++ files
	$(TIDY_CMD)

.PHONY: tidy-fix
tidy-fix: build ## Run clang-tidy --fix on all C++ files
	find $(CPP_FILES) -exec $(TIDY_BASE) --fix {} -- $(STDLIB_FLAG) \;

.PHONY: clean
clean: ## Remove build directory
	rm -rf $(BUILD_DIR)
	@echo "✅ Clean complete"

# Catch-all for file arguments (allows 'make tidy file1.cpp file2.cpp')
%:
	@:
