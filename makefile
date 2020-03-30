
project_dir=$(shell pwd)
crawler_dir=${project_dir}/crawler
visualize_daily_py_dir=${project_dir}/visualization/python/

css_template='https://fenggeorgeyu.github.io/css-templates/github.css'

all:

crawl_ohio:
	cd ${crawler_dir} && \
	python3 crawler_v2.py

crawl_stat_card:
	cd ${crawler_dir} && \
	python3 crawl_stat_card.py

crawl_csv_summary_ohio:
	cd ${project_dir} && \
	python3 crawler/crawl_csv_summary.py 

visualize_daily:
	cd ${visualize_daily_py_dir} && \
	python3 visualize_daily.py

visualize_daily_county:
	cd ${project_dir} && \
	python3 ${visualize_daily_py_dir}/visualize_daily_county.py

index:
	pandoc -s -c ${css_template} -o index.html README.md 

commit:
	git add .; \
	git add -u ;\
    git commit -am 'committed by fyu'; \
    git push

