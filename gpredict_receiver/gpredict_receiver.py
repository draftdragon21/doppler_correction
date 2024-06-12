#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: gpredict_receiver
# Author: Burkhardt, Tinker
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
import gpredict
import sip



class gpredict_receiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "gpredict_receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("gpredict_receiver")
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

        self.settings = Qt.QSettings("GNU Radio", "gpredict_receiver")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 300e3
        self.gain = gain = 20
        self.freq = freq = 850e6
        self.corrected_freq = corrected_freq = 850e6
        self.bandwidth_rec = bandwidth_rec = 10e6

        ##################################################
        # Blocks
        ##################################################

        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("Sample Rate" + ": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.editingFinished.connect(
            lambda: self.set_samp_rate(eng_notation.str_to_num(str(self._samp_rate_line_edit.text()))))
        self.top_grid_layout.addWidget(self._samp_rate_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_tool_bar = Qt.QToolBar(self)
        self._gain_tool_bar.addWidget(Qt.QLabel("RX Gain" + ": "))
        self._gain_line_edit = Qt.QLineEdit(str(self.gain))
        self._gain_tool_bar.addWidget(self._gain_line_edit)
        self._gain_line_edit.editingFinished.connect(
            lambda: self.set_gain(eng_notation.str_to_num(str(self._gain_line_edit.text()))))
        self.top_grid_layout.addWidget(self._gain_tool_bar, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("Carrier Frequency" + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.editingFinished.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._corrected_freq_tool_bar = Qt.QToolBar(self)
        self._corrected_freq_tool_bar.addWidget(Qt.QLabel("Carrier Frequency - Corrected" + ": "))
        self._corrected_freq_line_edit = Qt.QLineEdit(str(self.corrected_freq))
        self._corrected_freq_tool_bar.addWidget(self._corrected_freq_line_edit)
        self._corrected_freq_line_edit.editingFinished.connect(
            lambda: self.set_corrected_freq(eng_notation.str_to_num(str(self._corrected_freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._corrected_freq_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.qtgui_freq_sink_x_0_1_1_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            corrected_freq, #fc
            samp_rate, #bw
            "rx_corrected", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_1_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0_1_1_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_1_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1_1_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_1_1_0_win, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_1_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "rx_not-corrected", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_1.set_update_time(0.01)
        self.qtgui_freq_sink_x_0_1_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_1_1_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.gpredict_doppler_0 = gpredict.doppler('127.0.0.1', 4532, True)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_corrected_freq)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gpredict_doppler_0, 'freq'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.gpredict_doppler_0, 'freq'), (self.qtgui_freq_sink_x_0_1_1_0, 'freq'))
        self.connect((self.soapy_limesdr_source_0, 0), (self.qtgui_freq_sink_x_0_1_1, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.qtgui_freq_sink_x_0_1_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gpredict_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.samp_rate)))
        self.qtgui_freq_sink_x_0_1_1.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_freq_sink_x_0_1_1_0.set_frequency_range(self.corrected_freq, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        Qt.QMetaObject.invokeMethod(self._gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.gain)))
        self.soapy_limesdr_source_0.set_gain(0, min(max(self.gain, -12.0), 61.0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.qtgui_freq_sink_x_0_1_1.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)

    def get_corrected_freq(self):
        return self.corrected_freq

    def set_corrected_freq(self, corrected_freq):
        self.corrected_freq = corrected_freq
        Qt.QMetaObject.invokeMethod(self._corrected_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.corrected_freq)))
        self.qtgui_freq_sink_x_0_1_1_0.set_frequency_range(self.corrected_freq, self.samp_rate)

    def get_bandwidth_rec(self):
        return self.bandwidth_rec

    def set_bandwidth_rec(self, bandwidth_rec):
        self.bandwidth_rec = bandwidth_rec
        self.soapy_limesdr_source_0.set_bandwidth(0, self.bandwidth_rec)




def main(top_block_cls=gpredict_receiver, options=None):

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
