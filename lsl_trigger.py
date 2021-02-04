from pylsl import StreamInfo, StreamOutlet
import time
import psutil

from parameters.trigger_dict import trigger_dict, trigger_string_dict

class LSLTriggerHandler(object):
    def __init__(self, stream_name="default_stream", logger=None):
        self.info = StreamInfo(name=stream_name, type='Markers', channel_count=1,
                  channel_format='int32', source_id='1321')
        self.trigger_mapping = trigger_dict
        self.boot_time = psutil.boot_time()
        self.str_trigger_mapping = trigger_string_dict
        if logger:
            self.logger = logger
        else:
            self.logger = None
        self.outlet = StreamOutlet(self.info)
        print("Trigger Handler Created.")


    def send_int_trigger(self, trigger_int):

        msg = f"Pushing trigger: {trigger_int} to stream. ({self.trigger_mapping[trigger_int]})"
        print(msg)
        self.outlet.push_sample(x=[trigger_int])
        if self.logger:
            self.logger.write_row([time.time(), self.boot_time, time.time()-self.boot_time, trigger_int, self.trigger_mapping[trigger_int]])


    def send_string_trigger(self, trigger_string):

        trigger_int = self.str_trigger_mapping[trigger_string]
        msg = f"Pushing trigger: {trigger_int} to stream. ({trigger_string})"
        print(msg)
        self.outlet.push_sample(x=[trigger_int])
        if self.logger:
            self.logger.write_row([time.time(), self.boot_time, time.time()-self.boot_time, trigger_int, self.trigger_mapping[trigger_int]])
