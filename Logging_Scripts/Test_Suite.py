import os
import time
import psutil
import shutil

def system_Health_Check(logger,thresholds=None):
    # Runs a series of system health tests and logs status.
    # Returns True if system is healthy, False otherwise.
    
    if thresholds is None:
        thresholds = {
            'cpu_percent': 85,
            'ram_percent': 90,
            'disk_percent': 90,
            'min_disk_space_mb': 200,
            'ping_host': '8.8.8.8'
        }

    logger.info('###### Running System Health Checks ######')
    healthy = True

    ###########################################################################
                                ### CPU LOAD ###
    ###########################################################################
    cpu = psutil.cpu_percent(interval=1)
    logger.info(f'CPU load: {cpu}%')
    if cpu > thresholds['cpu_percent']:
        logger.error(f'CPU load too high: {cpu}%')
        healthy = False

    ###########################################################################
                                ### RAM USAGE ###
    ###########################################################################
    mem = psutil.virtual_memory()
    logger.info(f'RAM usage: {mem.percent}% ({mem.used/1e6:.1f} MB used)')
    if mem.percent > thresholds['ram_percent']:
        logger.error(f'RAM usage too high: {mem.percent}%')
        healthy = False

    ###########################################################################
                                ### DISK SPACE ###
    ###########################################################################
    disk = shutil.disk_usage('/')
    free_mb = disk.free / (1024 * 1024)
    usage_percent = (disk.used / disk.total) * 100
    logger.info(f'Disk free: {free_mb:.1f} MB ({usage_percent:.1f}% used)')

    if usage_percent > thresholds['disk_percent']:
        logger.error(f'Disk usage too high: {usage_percent:.1f}%')
        healthy = False

    if free_mb < thresholds['min_disk_space_mb']:
        logger.error(f'Not enough free disk space: {free_mb:.1f} MB')
        healthy = False
    
    ###########################################################################
                            ### FILESYSTEM PERMISSIONS ###
    ###########################################################################
    test_path = '/tmp/system_test_write.txt'
    logger.info('Checking filesystem write permissions...')
    try:
        # Check if we have write permissions to a test file
        with open(test_path, 'w') as f:
            f.write('write_test')
        os.remove(test_path)
        logger.info('Filesystem write test successful')
    except Exception as e:
        logger.error(f'Filesystem write failed: {e}')
        healthy = False
    
    ###########################################################################
                            ### NETWORK CONNECTIVITY ###
    ###########################################################################
    '''
    host = thresholds['ping_host']
    logger.info(f'Checking network connectivity to {host}')

    try:
        subprocess.run(
            ['ping', '-c', '1', '-W', '1', host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        logger.info('Ping successful')
    except subprocess.CalledProcessError:
        logger.error('Unable to reach network host (ping failed)')
        healthy = False
    '''

    ###########################################################################
                              ### CLOCK DRIFT CHECK ###
    ###########################################################################
    logger.info('Checking system time...')
    local_time = time.time()
    logger.info(f'Local timestamp: {local_time}')

    # (Optional: add NTP compare or RTC check here)

    ###########################################################################
                           ### FILESYSTEM PERMISSIONS ###
    ###########################################################################
    test_path = '/tmp/system_test_write.txt'
    logger.info('Checking filesystem write permissions...')

    try:
        with open(test_path, 'w') as f:
            f.write('write_test')
        os.remove(test_path)
        logger.info('Filesystem write test successful')
    except Exception as e:
        logger.error(f'Filesystem write failed: {e}')
        healthy = False

    ###########################################################################
                        ### PYTHON ENVIRONMENT CHECK ###
    ###########################################################################
    logger.info('Checking Python environment...')
    try:
        import sys
        logger.info(f'Python version: {sys.version}')
    except Exception as e:
        logger.error(f'Python environment error: {e}')
        healthy = False

    ###########################################################################
                              ### RESULTS ###
    ###########################################################################
    if healthy:
        logger.info('###### System health OK: all checks passed ######')
    else:
        logger.critical('###### System health FAILED: see errors above ######')

    return healthy

def sensor_performance_check(logger,thresholds=None):
    # Runs a series of tests on validity of data streaming from sensor and logs status.
    # Returns True if sensor is behaiving, False otherwise.
    
    if thresholds is None:
        thresholds = {
            'cpu_percent': 85,
            'ram_percent': 90,
            'disk_percent': 90,
            'min_disk_space_mb': 200,
            'ping_host': '8.8.8.8'
        }

    logger.info('###### Running Sensor Performance Checks ######')
    goodData = True
    ###########################################################################
                             ### Init Datastream ###
    ###########################################################################

    ###########################################################################
                                ### Read Data ###
    ###########################################################################

    ###########################################################################
                                ### Plot Data ###
    ###########################################################################

    ###########################################################################
                                ### Test Data ###
    ###########################################################################

    return goodData