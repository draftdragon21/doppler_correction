#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip



class basic_receiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "basic_receiver")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.taps_trans = taps_trans = 10e6
        self.taps_cutoff = taps_cutoff = 10e6
        self.samp_rate = samp_rate = 20e6
        self.lowpass_custom_taps = lowpass_custom_taps = firdes.low_pass(1.0, samp_rate, taps_cutoff,taps_trans, window.WIN_HAMMING, 6.76)
        self.gain = gain = 20
        self.freq = freq = 850e6
        self.bandwidth_rec = bandwidth_rec = 10e6

        ##################################################
        # Blocks
        ##################################################

        self._bandwidth_rec_range = qtgui.Range(0, 50e6, 1, 10e6, 200)
        self._bandwidth_rec_win = qtgui.RangeWidget(self._bandwidth_rec_range, self.set_bandwidth_rec, "'bandwidth_rec'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bandwidth_rec_win)
        self._taps_trans_range = qtgui.Range(1e6, 20e6, 1e6, 10e6, 200)
        self._taps_trans_win = qtgui.RangeWidget(self._taps_trans_range, self.set_taps_trans, "'taps_trans'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._taps_trans_win)
        self._taps_cutoff_range = qtgui.Range(1e6, 30e6, 1e6, 10e6, 200)
        self._taps_cutoff_win = qtgui.RangeWidget(self._taps_cutoff_range, self.set_taps_cutoff, "'taps_cutoff'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._taps_cutoff_win)
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, bandwidth_rec)
        self.soapy_limesdr_source_0.set_frequency(0, freq)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(gain, -12.0), 61.0))
        self.qtgui_sink_x_0_0_1_0_1_1_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            20e6, #bw
            'Raw_Receiver', #name
            True, #plotfreq
            False, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0_1_0_1_1_0.set_update_time(1.0/500)
        self._qtgui_sink_x_0_0_1_0_1_1_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_1_0_1_1_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0_1_0_1_1_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_1_0_1_1_0_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.soapy_limesdr_source_0, 0), (self.qtgui_sink_x_0_0_1_0_1_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "basic_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_taps_trans(self):
        return self.taps_trans

    def set_taps_trans(self, taps_trans):
        self.taps_trans = taps_trans
        self.set_lowpass_custom_taps(firdes.low_pass(1.0, self.samp_rate, self.taps_cutoff, self.taps_trans, window.WIN_HAMMING, 6.76))

    def get_taps_cutoff(self):
        return self.taps_cutoff

    def set_taps_cutoff(self, taps_cutoff):
        self.taps_cutoff = taps_cutoff
        self.set_lowpass_custom_taps(firdes.low_pass(1.0, self.samp_rate, self.taps_cutoff, self.taps_trans, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_lowpass_custom_taps(firdes.low_pass(1.0, self.samp_rate, self.taps_cutoff, self.taps_trans, window.WIN_HAMMING, 6.76))
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_lowpass_custom_taps(self):
        return self.lowpass_custom_taps

    def set_lowpass_custom_taps(self, lowpass_custom_taps):
        self.lowpass_custom_taps = lowpass_custom_taps

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_limesdr_source_0.set_gain(0, min(max(self.gain, -12.0), 61.0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_sink_x_0_0_1_0_1_1_0.set_frequency_range(self.freq, 20e6)
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)

    def get_bandwidth_rec(self):
        return self.bandwidth_rec

    def set_bandwidth_rec(self, bandwidth_rec):
        self.bandwidth_rec = bandwidth_rec
        self.soapy_limesdr_source_0.set_bandwidth(0, self.bandwidth_rec)




def main(top_block_cls=basic_receiver, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
