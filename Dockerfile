FROM python:alpine

LABEL maintainer="liuchang"

COPY ./src /alertmanager-webhook-wechat/

WORKDIR /alertmanager-webhook-wechat

RUN \
    chmod +x run.sh && \
    pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000

CMD ["./run.sh"]
