import datetime
import time
import psutil


def get_process(sort_by='cpu_percent', only_user=None):
    # get process from psutil
    process = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'username']):
        try:
            process.append(proc.info)
        except psutil.NoSuchProcess:
            pass

    if only_user:
        process = [proc for proc in process if proc['username'] in only_user]

    return sorted(process, key=lambda x: x[sort_by], reverse=True)[:20]


def get_user():
    # get logged in user from psutil
    users = psutil.users()
    return [dict(name=user.name, terminal=user.terminal, host=user.host,
                 started=datetime.datetime.fromtimestamp(user.started).strftime("%H:%M:%S")) for user in users]


def get_number_of_users():
    # get logged in user from psutil
    users = psutil.users()
    return len(users)


def get_usernames():
    # get logged in user from psutil
    users = psutil.users()
    return [user.name for user in users]


def get_boot_time():
    # get boot time from psutil

    t = time.clock_gettime(time.CLOCK_BOOTTIME)

    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S")


def get_cpu_usage():
    # get cpu usage from psutil
    return psutil.cpu_percent(interval=1, percpu=True)


def get_average_load_5():
    # get average load from psutil
    num_cpu = psutil.cpu_count()

    load = psutil.getloadavg()[1]
    return load / num_cpu


def get_memory_usage():
    # get available memory from psutil
    return psutil.virtual_memory().percent/100


def get_disks_usage():
    return [dict(mount=p.mountpoint, usage=psutil.disk_usage(p.mountpoint)[3]) for p in psutil.disk_partitions()]

