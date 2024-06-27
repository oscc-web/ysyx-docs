TAG := latest

.PHONY : clean
clean :
	find . -empty -type d -delete

.PHONY : pull
pull :
	./pull_content.py --repo oscc-web/ysyx-docs-content --tag $(TAG) --map zh:docs --map en:i18n/en/docusaurus-plugin-content-docs/current
