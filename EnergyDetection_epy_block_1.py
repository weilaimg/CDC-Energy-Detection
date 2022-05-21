"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, n_samples=128, threshold=1, send_samples=4096):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Selector Control',   # will show up in GRC
            in_sig=[np.complex64,np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.n_samples = n_samples
        self.threshold = threshold
        self.send_samples = send_samples
        
        self.portName = 'messageOutput'
        self.message_port_register_out(pmt.intern(self.portName))
        self.lastMsg = False
        self.counter = 0
        

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        print(self.counter,self.lastMsg)
        if self.lastMsg:
            in1 = input_items[1]
            nin = len(in1)
        
            x = np.abs(in1)**2
            i_samp = 0
        
            while i_samp + self.n_samples < nin:
                z = x[i_samp : i_samp + self.n_samples].mean()
                i_samp += self.n_samples
                if(z > self.threshold):
                    self.lastMsg = True
                    PMT_msg = pmt.from_bool(True)
                    self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                else:
                    self.lastMsg = False
                    PMT_msg = pmt.from_bool(False)
                    self.message_port_pub(pmt.intern(self.portName), PMT_msg)

        else:
            self.counter = self.counter + len(output_items[0])
            if (self.counter > self.send_samples):
                self.lastMsg = True
                PMT_msg = pmt.from_bool(True)
                self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                self.counter = 0
        
        
        #self.counter = self.counter + len(output_items[0])
        
        #if (self.counter > self.Num_Samples_To_Count):
        #    PMT_msg = pmt.from_bool(self.state)
        #    self.message_port_pub(pmt.intern(self.portName), PMT_msg)
        #    self.state = not(self.state)
        #    self.counter = 0
        
        output_items[0][:] = input_items[0]
        return len(output_items[0])
        
        
        
        
        
