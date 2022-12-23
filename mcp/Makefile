# -------------------------------------------
# RUNTIME
# -------------------------------------------
.PHONY: env_down
local_down:
	@bash -c "./publish_images.sh aws ci"
	@echo "Environment DOWN"

.PHONY: env_up
local_up:
	deploy/localstack/build.sh HE
	./build.sh HE
	@echo "Environment DOWN"
