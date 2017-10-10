**Install:**

install python-jenkins:
```
pip install python-jenkins
```

copy and update config file:
```
cp config/config_default.py config/config.py
```

copy and update xml:
```
cp xml/job_default.xml xml/job.xml
```

**Usage:**

```
python2 generate_jobs.py tests/api
```

```
python2 generate_jobs.py tests/api delete # delete _all_ jobs in all jenkins!!!
```

```
python2 update_jobs.py tests/api
```

**How to run docker jenkins (https://hub.docker.com/_/jenkins/):**

```
docker pull jenkins
```

```
docker run --name local_jenkins -p 8080:8080 -p 50000:50000 -v `pwd`/work/jenkins:/var/jenkins_home --env JAVA_OPTS="-Dhudson.model.DirectoryBrowserSupport.CSP=\"default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';\"" -d jenkins
```
where `pwd`/work/jenkins - path to local directory
