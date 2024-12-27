# flask 웹서버 구축 
-----
## AWS EC2 프리티어 (ubuntu OS) 크롬 브라우저, 크롬 드라이버 설치 
* 크롬 브라우저 설치
```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt install -y ./google-chrome-stable_current_amd64.deb
```

* 크롬 브라우저 버전 확인
```
$ /usr/bin/google-chrome --version
```

* 크롬 드라이버 설치 (크롬 브라우저 버전과 일치한 것 다운받기)
  * https://googlechromelabs.github.io/chrome-for-testing/
```
$ wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip
$ unzip chromedriver-linux64.zip
$ sudo mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
```

* 크롬 드라이버 버전 확인
```
$ chromedriver --version
```
