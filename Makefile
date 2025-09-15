.DEFAULT_GOAL := help
PRESET := uv-env

# Cross-platform detection
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    STDLIB_FLAG := -stdlib=libc++
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

.PHONY: deps-build
deps-build: ## Check if cmake and clang-tidy are available
	@command -v cmake >/dev/null || (echo "❌ cmake not found" && echo "   Install: macOS → brew install cmake | Linux → apt install cmake" && exit 1)
	@echo "✅ Build Dependencies OK ($(UNAME_S))"

.PHONY: deps-ci
deps-ci: ## Check if cmake and clang-tidy are available for CI
	@command -v clang-tidy >/dev/null || (echo "❌ clang-tidy not found" && echo "   Install: macOS → brew install llvm | Linux → apt install clang-tidy" && exit 1)
	@echo "✅ CI Dependencies OK ($(UNAME_S))"

.PHONY: build
build: deps-build ## Configure and build the project
	cmake --preset $(PRESET)
	cmake --build --preset $(PRESET)

.PHONY: tidy
tidy: build deps-ci ## Run clang-tidy on all C++ files
	$(TIDY_CMD)

.PHONY: tidy-fix
tidy-fix: build deps-ci ## Run clang-tidy --fix on all C++ files
	find $(CPP_FILES) -exec $(TIDY_BASE) --fix {} -- $(STDLIB_FLAG) \;

.PHONY: clean
clean: ## Remove build directory
	rm -rf $(BUILD_DIR)
	@echo "✅ Clean complete"

.PHONY: docs
docs: ## Build documentation
	@echo "🔄 Building documentation..."
	python3 build_docs.py

.PHONY: docs-serve
docs-serve: ## Serve documentation locally
	@echo "🌐 Serving documentation at http://127.0.0.1:8000"
	mkdocs serve

.PHONY: docs-deploy
docs-deploy: ## Deploy documentation to GitHub Pages
	@echo "🚀 Deploying documentation to GitHub Pages..."
	mkdocs gh-deploy

# Catch-all for file arguments (allows 'make tidy file1.cpp file2.cpp')
%:
	@:
