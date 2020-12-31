from pylsl import StreamInfo, StreamOutlet
import time

from parameters.trigger_dict import trigger_dict

class LSLTriggerHandler(object):
    def __init__(self, stream_name="default_stream", logger=None):
        self.info = StreamInfo(name=stream_name, type='Markers', channel_count=1,
                  channel_format='int32', source_id='1321')
        self.trigger_mapping = trigger_dict
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
            self.logger.write_to_log_file(msg)
