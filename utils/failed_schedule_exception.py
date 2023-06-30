class FailedScheduleException(Exception):

    def __init__(self, time, job):
        message = f'job {job.id} with period {job.deadline-job.start} failed at {time} time'
        super(FailedScheduleException, self).__init__(message)
