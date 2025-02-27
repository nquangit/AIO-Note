
```bash

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic-keyring.gpg

sudo apt-get install apt-transport-https

echo "deb [signed-by=/usr/share/keyrings/elastic-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list

sudo apt-get update && sudo apt-get install elasticsearch

sudo apt-get update && sudo apt-get install logstash

sudo apt-get update && sudo apt-get install kibana


```

```bash
# Cấu hình Elasticsearch
echo "network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml

# Khởi động Elasticsearch
systemctl enable elasticsearch
systemctl start elasticsearch

# Cấu hình Kibana để cho phép truy cập từ tất cả các nguồn
echo "server.host: 0.0.0.0" >> /etc/kibana/kibana.yml

# Khởi động Kibana
systemctl enable kibana
systemctl start kibana
```



The password and certificate and keys are output to your terminal. You can reset the password for the elastic user with the `elasticsearch-reset-password` command.

You can then generate an enrollment token for Kibana with the `elasticsearch-create-enrollment-token` tool.

```bash
# Reset mật khẩu elastic search và tạo token cho kibana
elastic_password=$(echo "y" | /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic | grep -o "New value: .*" | cut -d ' ' -f 3-)
kibana_token=$(/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana)

# Di chuyển và mở verification code
cd /usr/share/kibana && verification_code=$(bin/kibana-verification-code)

# Hiển thị thông tin đăng nhập
echo "Thông tin đăng nhập:"
echo "-------------------"
echo "Elasticsearch:"
echo "   Tài khoản: elastic"
echo "   Mật khẩu: $elastic_password"
echo ""
echo "Kibana:"
echo "   Token: $kibana_token"
echo ""
echo "Mã xác minh Kibana:"
echo "$verification_code"
```

```bash
vi /etc/logstash/conf.d/container-3150.conf 
```

```yaml
input {
  beats {
    port => 5044
  }
}

output {
  elasticsearch {
    index => "containers_3.150"
    hosts => ["10.32.3.110:9200"]
    user => "elastic"
    password => "WsD0RVA+Zdf53UDOYTL_"
    ssl => true
    ssl_certificate_verification => false #bạn có thể chuyển thành true và sử dụng /etc/elasticsearch/certs/http_ca.crt
  }
}
```

```bash
# Allow logtash port
ufw allow 5044/tcp
systemctl stop logstash && systemctl start logstash 
```

## Client

Filebeat install 

```bash
#!/bin/bash

# Cập nhật hệ thống
sudo apt update

# Cài đặt các gói cần thiết
sudo apt install -y apt-transport-https wget

# Tải xuống và cài đặt GPG key của Elastic
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Thêm kho lưu trữ Elastic vào danh sách nguồn
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

# Cập nhật hệ thống để áp dụng thay đổi mới
sudo apt update

# Cài đặt Filebeat
sudo apt install -y filebeat

# Sao chép file cấu hình mẫu
sudo cp /etc/filebeat/filebeat.yml /etc/filebeat/filebeat.yml.bak

# Bật dịch vụ Filebeat
sudo systemctl enable filebeat
sudo systemctl start filebeat
```

```bash
mv /etc/filebeat/filebeat.yml /etc/filebeat/filebeat.yml.bak # lưu lại file cấu hình mặc định của filebeat (kiểu backup lại sau bạn có dùng thì dùng)
```

```yaml
/etc/filebeat/filebeat.yml 

filebeat.inputs:
- type: log
  paths:
    - /var/lib/docker/containers/*/*-json.log # thu thập logs tất cả các container hiện có trên server

output.logstash:
  hosts: ["10.32.3.110:5044"]
```

```bash
$ filebeat test output #test output filebeat như dưới đây là đã sẵn sàng gửi logs về logstash.
```
