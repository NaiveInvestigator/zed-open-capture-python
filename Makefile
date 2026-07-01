.PHONY: all clone build_zed_oc install_zed_oc udev build install clean reinstall distclean update

BUILD_DIR     := build
PYTHON        := $(shell which python3)
THIRD_PARTY   := third_party
ZED_OC_DIR    := $(THIRD_PARTY)/zed-open-capture
ZED_OC_REPO   := https://github.com/stereolabs/zed-open-capture.git
ZED_OC_BUILD  := $(ZED_OC_DIR)/build

all: deps clone udev build_zed_oc build install

# ----> Install system prerequisites
deps:
	@echo "📦 Installing prerequisites..."
	sudo apt update
	sudo apt install -y build-essential cmake \
		libusb-1.0-0-dev libhidapi-libusb0 libhidapi-dev \
		libopencv-dev libopencv-viz-dev
# <---- Install system prerequisites

# ----> Clone upstream repo if not already present
clone:
	@if [ ! -d "$(ZED_OC_DIR)" ]; then \
		echo "📥 Cloning zed-open-capture..."; \
		git clone $(ZED_OC_REPO) $(ZED_OC_DIR); \
	else \
		echo "✅ zed-open-capture already present"; \
	fi
# <---- Clone upstream repo if not already present

update:
	@cd $(ZED_OC_DIR) && git pull

# ----> Add udev rule for USB HID sensor access
udev: clone
	@echo "🔌 Installing udev rule (requires sudo)..."
	@cd $(ZED_OC_DIR)/udev && sudo bash install_udev_rule.sh
# <---- Add udev rule for USB HID sensor access

# ----> Build the upstream C++ library only (no examples, video disabled to save time)
build_zed_oc: clone
	@mkdir -p $(ZED_OC_BUILD)
	@cd $(ZED_OC_BUILD) && cmake .. \
		-DCMAKE_BUILD_TYPE=Release \
		-DBUILD_EXAMPLES=OFF
	@cmake --build $(ZED_OC_BUILD) -- -j$(shell nproc)
	@echo "✅ zed-open-capture built"
# <---- Build the upstream C++ library

# ----> Install it system-wide so headers/lib are findable normally
install_zed_oc: build_zed_oc
	@cd $(ZED_OC_BUILD) && sudo make install
	@sudo ldconfig
	@echo "✅ zed-open-capture installed system-wide"
# <---- Install it system-wide

# ----> Build the Python bindings against the local vendored library
build: build_zed_oc
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && cmake .. \
		-DCMAKE_BUILD_TYPE=Release \
		-DPYTHON_EXECUTABLE=$(PYTHON)
	@cmake --build $(BUILD_DIR) -- -j$(shell nproc)
# <---- Build the Python bindings

install: build
	@cd $(BUILD_DIR) && cmake --install . --prefix $(shell $(PYTHON) -c "import sys; print(sys.prefix)")
	@echo "✅ Installed. Test with: python3 -c 'import sensor_capture'"

reinstall: clean all

clean:
	@rm -rf $(BUILD_DIR) $(ZED_OC_BUILD)
	@echo "🧹 Cleaned build dirs (kept cloned source)"

distclean: clean
	@rm -rf $(THIRD_PARTY)
	@echo "🧹 Removed cloned third_party sources too"
