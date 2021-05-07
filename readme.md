# description
alertmanager的webhook，对接企业微信机器人

# dependence
- k8s
- kube_prometheus

# build
docker build -t harbor.dreame.com/zhangchunlin/flask-alert-webhook:v0.1.11  -f Dockerfile .

# config
```shell script
cat prometheus-webhook-flask-alert.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    run: prometheus-webhook-wechat
  name: prometheus-webhook-wechat
  namespace: monitoring
spec:
  selector:
    matchLabels:
      run: prometheus-webhook-wechat
  template:
    metadata:
      labels:
        run: prometheus-webhook-wechat
    spec:
      containers:
      - image: harbor.dreame.com/zhangchunlin/flask-alert-webhook:v0.1.10
        name: prometheus-webhook-wechat
        ports:
        - containerPort: 5000
          protocol: TCP
        volumeMounts:
        - name: localtime
          mountPath: /etc/localtime
        env:
        - name: chatKey
          value: "55570b17-87ea-4855-ab44-2c83eaabead7"
        - name: env
          value: "test"
      volumes:
      - name: localtime
        hostPath:
          path: /etc/localtime
---
apiVersion: v1
kind: Service
metadata:
  labels:
    run: prometheus-webhook-wechat
  name: prometheus-webhook-wechat
  namespace: monitoring
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 5000
  selector:
    run: prometheus-webhook-wechat
  type: ClusterIP
```

# run
kubectl apply -f prometheus-webhook-flask-alert.yaml