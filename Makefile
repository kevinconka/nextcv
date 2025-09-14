.DEFAULT_GOAL := help
SHELL := /bin/bash

# ---- paths & knobs -----------------------------------------------------------
SRC_DIR   := nextcv/_cpp/src
BUILD_DIR := build
PRESET    := uv-env

# ---- tool detection (cross-platform) ----------------------------------------
UNAME := $(shell uname)

# Prefer Homebrew LLVM's clang-tidy on macOS; otherwise fall back to system
ifeq ($(UNAME),Darwin)
  BREW_PREFIX  := $(shell brew --prefix llvm 2>/dev/null || echo "")
  CLANG_TIDY   := $(if $(BREW_PREFIX),$(BREW_PREFIX)/bin/clang-tidy,clang-tidy)
  SDK          := $(shell xcrun --show-sdk-path 2>/dev/null || echo "")
  EXTRA_ARGS   := $(if $(SDK),-isysroot $(SDK)) -stdlib=libc++
else
  CLANG_TIDY   := clang-tidy
  EXTRA_ARGS   :=
endif

# ---- sources & tidy flags ----------------------------------------------------
# Only run on translation units; headers are picked up via --header-filter
FILES      := $(shell find $(SRC_DIR) -type f -name '*.cpp')
TIDY_FLAGS := --header-filter='^$(abspath $(SRC_DIR))/.*' --format-style=file

# Parallelism for xargs (macOS `sysctl`, Linux `nproc`)
NPROCS := $(shell sysctl -n hw.ncpu 2>/dev/null || nproc || echo 1)

# ---- help -------------------------------------------------------------------
.PHONY: help
help:
	@echo "NextCV C++ Makefile"
	@echo "-------------------"
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS=":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

# ---- deps check --------------------------------------------------------------
.PHONY: check-deps
check-deps: ## Check cmake + clang-tidy (and macOS SDK on Darwin)
	@set -e; fail=0; \
	command -v cmake >/dev/null 2>&1 || { echo "✖ cmake not found"; fail=1; }; \
	command -v $(CLANG_TIDY) >/dev/null 2>&1 || { echo "✖ clang-tidy not found"; fail=1; }; \
	if [ "$(UNAME)" = "Darwin" ]; then \
	  xcrun --show-sdk-path >/dev/null 2>&1 || { echo "✖ macOS SDK missing (xcode-select --install)"; fail=1; }; \
	fi; \
	[ $$fail -eq 0 ] && echo "✓ deps OK" || (echo "hint: macOS → brew install llvm cmake; Linux → apt install clang-tidy cmake"; exit 1)

# ---- configure & build -------------------------------------------------------
.PHONY: configure
configure: check-deps ## Configure the build with CMake preset
	cmake --preset $(PRESET)

.PHONY: build
build: configure ## Build using CMake preset
	cmake --build --preset $(PRESET)

# ---- tidy runners (DRY with a small macro) ----------------------------------
define _RUN_TIDY_LIST
	$(CLANG_TIDY) -p $(BUILD_DIR) $(TIDY_FLAGS) $(1) -- $(EXTRA_ARGS)
endef

define _RUN_TIDY_ALL
	printf '%s\0' $(FILES) | xargs -0 -n1 -P $(NPROCS) $(CLANG_TIDY) -p $(BUILD_DIR) $(TIDY_FLAGS) -- $(EXTRA_ARGS)
endef

.PHONY: tidy
tidy: configure ## Run clang-tidy (all files or: make tidy file1.cpp file2.cpp)
	@TIDY_FILES=$$(echo $(filter-out tidy,$(MAKECMDGOALS))); \
	if [ -n "$$TIDY_FILES" ]; then \
	  echo "Running clang-tidy on $$(echo $$TIDY_FILES | wc -w) files…"; \
	  $(call _RUN_TIDY_LIST,$$TIDY_FILES); \
	else \
	  echo "Running clang-tidy on $(words $(FILES)) files (P=$(NPROCS))…"; \
	  @$(call _RUN_TIDY_ALL); \
	fi

.PHONY: tidy-fix
tidy-fix: configure ## Run clang-tidy --fix (all or specific files), then rebuild
	@TIDY_FILES=$$(echo $(filter-out tidy-fix,$(MAKECMDGOALS))); \
	if [ -n "$$TIDY_FILES" ]; then \
	  echo "Running clang-tidy --fix on $$(echo $$TIDY_FILES | wc -w) files…"; \
	  $(CLANG_TIDY) -p $(BUILD_DIR) --fix $(TIDY_FLAGS) $$TIDY_FILES -- $(EXTRA_ARGS); \
	else \
	  echo "Running clang-tidy --fix on $(words $(FILES)) files (P=$(NPROCS))…"; \
	  @printf '%s\0' $(FILES) | xargs -0 -n1 -P $(NPROCS) $(CLANG_TIDY) -p $(BUILD_DIR) --fix $(TIDY_FLAGS) -- $(EXTRA_ARGS); \
	fi; \
	echo "Rebuilding to verify…"; cmake --build --preset $(PRESET)

.PHONY: tidy-changed
tidy-changed: configure ## Run clang-tidy on changed C++ files (git index vs HEAD)
	@set -e; \
	CHANGED=$$(git diff --name-only --diff-filter=AM -- '*.cpp' | sed -e 's|^|./|'); \
	if [ -z "$$CHANGED" ]; then echo "No changed .cpp files."; exit 0; fi; \
	echo "Running clang-tidy on $$(( $$(echo "$$CHANGED" | wc -w) )) changed files…"; \
	$(CLANG_TIDY) -p $(BUILD_DIR) $(TIDY_FLAGS) $$CHANGED -- $(EXTRA_ARGS)

# ---- clean ------------------------------------------------------------------
.PHONY: clean
clean: ## Remove build directory
	@echo "Cleaning $(BUILD_DIR)…"
	rm -rf "$(BUILD_DIR)"
	@echo "✓ Clean complete"
