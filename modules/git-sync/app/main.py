import git
import os
import time
import sched
import hashlib
import logging

import git_interface

default_local_path = "./git"
default_scheduler_interval = 5

# env can have multiple git repos
# each repo synced to specific folder with uuid (one-to-one hashing of url)


def event_loop(sc, instances):

    logging.info("Performing Sync with %s", str(instances[0].git_remote_url))
    
    # if not os.path.exists(instances[0].git_local_path) or len(os.listdir(instances[0].git_local_path)) == 0:
        # logging.info("Cloned ew Repo Instance")
        # instances[0].clone_git_repo()    

    if not instances[0].check_integrity():
        logging.info("Recovered Repo Integrity")
        instances[0].recover_git_repo()

    if instances[0].is_git_repo():
        logging.info("Synced Repo with Latest")
        instances[0].update_git_repo()

    sc.enter(scheduler_interval, 1, event_loop, (sc,instances,))


if __name__ == '__main__':

    log_level = os.environ['LOG_LEVEL']
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        datefmt='%Y-%m-%d %H:%M:%S')

    scheduler_interval = os.environ['SCHEDULER_INTERVAL']
    git_remote_url = os.environ['GIT_REMOTE_URL']

    if scheduler_interval is None or \
            not isinstance(os.environ['SCHEDULER_INTERVAL'], int) or \
            int(os.environ['SCHEDULER_INTERVAL']) <= 0:
        scheduler_interval = default_scheduler_interval
    else:
        scheduler_interval = int(scheduler_interval)

    # Check each Remote
    logging.info("Checking Remotes")
    sha = hashlib.sha256()
    sha.update(git_remote_url.encode())
    _hash = sha.hexdigest()[0:8]

    git_instances = [git_interface.GitInterface(default_local_path, git_remote_url, _hash)]

    print(git_instances[0].git_local_path, git_instances[0].git_remote_url)

    # Start Syncing
    logging.info("Starting Git Sync")
    s = sched.scheduler(time.time, time.sleep)
    s.enter(scheduler_interval, 1, event_loop, (s,git_instances,))
    s.run()

