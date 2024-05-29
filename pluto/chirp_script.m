clear; close all; clc;

% configurePlutoRadio('AD9364'); 

fs = 5e6;

chirp = dsp.Chirp;
chirp.InitialFrequency = 1e6;
chirp.TargetFrequency = 5e6;
chirp.TargetTime = 2.0;
chirp.SweepTime = 2.0;
chirp.SampleRate = fs;
chirp.SamplesPerFrame = 10e6;

txWaveform = complex(chirp(),0);

pause(5);
tx = sdrtx('Pluto'); 
tx.CenterFrequency = 840e6;
tx.BasebandSampleRate = fs;
tx.Gain = 0;
 
rx = sdrrx('Pluto');
rx.SamplesPerFrame = 40000;
rx.CenterFrequency = 840e6;
rx.BasebandSampleRate = fs;

sa = dsp.SpectrumAnalyzer;
sa.SampleRate = rx.BasebandSampleRate;

tx.transmitRepeat(txWaveform);

for k=1:1:10000
     sa(rx());
end
data = rx();

release(tx);
release(rx);
release(sa);
 