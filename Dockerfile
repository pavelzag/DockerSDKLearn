FROM python:2
ADD main.py /
RUN pip install docker
RUN pip install fake_useragent
RUN pip install pytest
RUN pip install requests
RUN py.test main.py --html=report.html
