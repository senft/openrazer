"""
A class that writes persistence data to disk when device state is updated.

Due to the architecture of the daemon, it's not as simple to know when
something has changed, so for now, an interval will periodically check for
changes in memory and write them to disk.

This is essential because many desktop environments actually kill off
the daemon upon logout/shutdown, thereby persistence isn't retained across
sessions.

A known issue is that this doesn't monitor DPI changes via hardware buttons,
so this isn't saved unless the data is set via the API.
"""
import time

class PersistenceAutoSave(object):
    def __init__(self, persistence, persistence_file, logger, interval, persistence_save_fn):
        self.persistence = persistence
        self.persistence_file = persistence_file
        self.persistence_save_fn = persistence_save_fn
        self.logger = logger
        self.interval = interval

        self.last_data = persistence._sections.copy()

    def watch(self):
        while True:
            if self.persistence._sections != self.last_data:
                self.logger.debug("State changed, writing to disk")
                self.persistence_save_fn(self.persistence_file)
                self.last_data = persistence._sections.copy()
            time.sleep(self.interval)

            print("Changed? " + str(self.persistence._sections != self.last_data))
