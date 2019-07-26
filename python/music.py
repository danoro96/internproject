#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Run Music Lin Array X310 Twinrx
# Generated: Tue Jul 16 09:28:18 2019
##################################################

def struct(data): return type('Struct', (object,), data)()
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import doa
import os


class run_MUSIC_lin_array_X310_TwinRX(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Run Music Lin Array X310 Twinrx")

        ##################################################
        # Variables
        ##################################################
        self.input_variables = input_variables = struct({"NumArrayElements": 2, "NormSpacing": 0.33, "SnapshotSize": 2**11, "OverlapSize": 2**9, "NumTargets": 1, "PSpectrumLength": 2**10, "DirectoryConfigFiles": "/home/donnie", "RelativePhaseOffsets": "measure_X310_TwinRX_relative_phase_offsets_245.cfg", })
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name = os.path.join(input_variables.DirectoryConfigFiles, input_variables.RelativePhaseOffsets)

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pull_source_0_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://192.168.1.20:9998", 100, False, -1)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_gr_complex, 1, "tcp://192.168.1.20:9999", 100, False, -1)
        self.phase_correct_hier_1 = doa.phase_correct_hier(
            num_ports=input_variables.NumArrayElements,
            config_filename=rel_phase_offsets_file_name,
        )
        self.doa_find_local_max_0 = doa.find_local_max(input_variables.NumTargets, input_variables.PSpectrumLength, 0.0, 180.0)
        self.doa_average_and_save_0 = doa.average_and_save(5000, input_variables.NumTargets, "/home/donnie/daniel/PyProj/data.cfg")
        self.doa_autocorrelate_0 = doa.autocorrelate(input_variables.NumArrayElements, input_variables.SnapshotSize, input_variables.OverlapSize, 1)
        self.doa_MUSIC_lin_array_0 = doa.MUSIC_lin_array(input_variables.NormSpacing, input_variables.NumTargets, input_variables.NumArrayElements, input_variables.PSpectrumLength)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*input_variables.NumTargets)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.doa_MUSIC_lin_array_0, 0), (self.doa_find_local_max_0, 0))    
        self.connect((self.doa_autocorrelate_0, 0), (self.doa_MUSIC_lin_array_0, 0))    
        self.connect((self.doa_find_local_max_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.doa_find_local_max_0, 1), (self.doa_average_and_save_0, 0))    
        self.connect((self.phase_correct_hier_1, 0), (self.doa_autocorrelate_0, 0))    
        self.connect((self.phase_correct_hier_1, 1), (self.doa_autocorrelate_0, 1))    
        self.connect((self.zeromq_pull_source_0, 0), (self.phase_correct_hier_1, 0))    
        self.connect((self.zeromq_pull_source_0_0, 0), (self.phase_correct_hier_1, 1))    

    def get_input_variables(self):
        return self.input_variables

    def set_input_variables(self, input_variables):
        self.input_variables = input_variables
        self.set_rel_phase_offsets_file_name(os.path.join(self.input_variables.DirectoryConfigFiles, self.input_variables.RelativePhaseOffsets))

    def get_rel_phase_offsets_file_name(self):
        return self.rel_phase_offsets_file_name

    def set_rel_phase_offsets_file_name(self, rel_phase_offsets_file_name):
        self.rel_phase_offsets_file_name = rel_phase_offsets_file_name


def main(top_block_cls=run_MUSIC_lin_array_X310_TwinRX, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
