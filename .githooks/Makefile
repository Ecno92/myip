.git/hooks/: $(shell find .githooks -type f)
	ln -f -s $(PWD)/.githooks/*[^Makefile] .git/hooks
	find .git/hooks -xtype l -delete

setup-webhooks := .git/hooks/
