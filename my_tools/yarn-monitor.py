import requests
import paramiko
import time
from bs4 import BeautifulSoup

def get_yarn_resource():
    '''
        :return yarn集群可以资源,单位GB
    '''
    try:
        url = 'http://ahadoop003:8088/cluster/apps/RUNNING'
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'lxml')
        trs = soup.select("#metricsoverview tr")
        ths1 = trs[0].find_all('th')
        ths2 = trs[1].find_all('td')
        memory_total = None
        memory_used = None
        for i, th in enumerate(ths1):
            if 'Memory Total' == th.text.strip():
                memory_total = ths2[i].text.strip()
            elif 'Memory Used' == th.text.strip():
                memory_used = ths2[i].text.strip()

        if memory_total and memory_used:
            words = memory_used.split(' ')
            used = float(words[0]) * (1000 if 'TB' == words[1] else 1);
            words = memory_total.split(' ')
            total = float(words[0]) * (1000 if 'TB' == words[1] else 1);
            return total - used;
    except Exception:
        raise ValueError('解析异常,请检查网络')


def submit_task(cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("ip", 22, "username", "password")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.readlines())
    ssh.close()

def do_task(cmd, min_resource, interval=60):
    while True:
        if get_yarn_resource() >= min_resource:
            submit_task(cmd)
            break;
        else:
            time.sleep(interval)

if __name__ == '__main__':
    do_task('sh ~/jars/test.sh', 1000)
