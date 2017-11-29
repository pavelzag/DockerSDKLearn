FROM python:2
ADD main.py /
RUN pip install docker
RUN pip install fake_useragent
RUN pip install os
RUN pip install pytest
RUN pip install random
RUN pip install requests
RUN pip install string
RUN pip install time
CMD ["pytest", "./main.py", "--html=report.html"]
